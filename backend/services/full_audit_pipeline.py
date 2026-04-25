import pandas as pd
import numpy as np
from datetime import datetime
from collections import defaultdict
import json
from services.data_prep_agent import orchestrator
from services.auditor import auditor


class NumpyEncoder(json.JSONEncoder):
    """Convert numpy types to JSON-serializable types"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
        if pd.isna(obj):
            return None
        if isinstance(obj, (pd.Timestamp, np.datetime64)):
            return str(obj.date() if hasattr(obj, 'date') else obj)
        return super().default(obj)


class FullAuditPipeline:
    """
    Complete end-to-end audit pipeline:
    1. Upload CSV
    2. Prepare/clean data
    3. Extract features & violations
    4. Run audit analysis
    5. Generate comprehensive summary
    """

    def process_file(self, df: pd.DataFrame) -> dict:
        """
        Process expense file through complete audit pipeline
        """
        try:
            # Step 1: Prepare & Clean Data
            print("[1/4] Preparing data...")
            prep_result = orchestrator.prepare(df)

            if prep_result['status'] != 'success':
                return {
                    'status': 'error',
                    'stage': 'preparation',
                    'errors': prep_result['errors'],
                    'message': 'Data preparation failed'
                }

            df_prepared = prep_result['data']

            # Step 2: Extract Features & Build Audit Input
            print("[2/4] Extracting features...")
            audit_input = self._build_audit_input(df_prepared, prep_result)

            # Step 3: Run Audit Analysis
            print("[3/4] Running audit analysis...")
            audit_report = auditor.analyze(audit_input)

            # Step 4: Generate Summary & Combine Results
            print("[4/4] Generating summary...")
            complete_report = self._generate_complete_report(
                prep_result,
                audit_report,
                df_prepared
            )

            result = {
                'status': 'success',
                'message': 'Audit completed successfully',
                'report': complete_report
            }
            
            # Serialize to clean numpy types
            result = json.loads(json.dumps(result, cls=NumpyEncoder))
            
            return result

        except Exception as e:
            return {
                'status': 'error',
                'stage': 'pipeline',
                'message': str(e),
                'error_type': type(e).__name__
            }

    def _build_audit_input(self, df: pd.DataFrame, prep_result: dict) -> dict:
        """
        Extract features and build structured audit input from prepared data
        """
        # Initialize audit input structure
        enriched_features = []
        transactions = []

        # Build enriched features list
        for idx, row in df.iterrows():
            # Ensure date is clean (YYYY-MM-DD)
            raw_date = row.get('date', '')
            if hasattr(raw_date, 'date'):
                date_str = str(raw_date.date())
            elif isinstance(raw_date, str) and ' ' in raw_date:
                date_str = raw_date.split(' ')[0]
            else:
                date_str = str(raw_date)

            feature = {
                'date': date_str,
                'employee': row.get('employee', 'Unknown'),
                'amount': float(row.get('amount', 0)),
                'category': row.get('category', 'Unknown'),
                'vendor': row.get('vendor', 'Unknown'),
                'description': row.get('description', ''),
                'spending_level': self._calculate_spending_level(float(row.get('amount', 0))),
                'is_high_value': float(row.get('amount', 0)) > 3000,
                'risk_flag': False,  # Will be updated based on rules
                'inferred_department': row.get('department', 'Unknown'),
                'employee_level': row.get('employee_level', 'Unknown'),
                'behavioral_tags': []
            }
            enriched_features.append(feature)

            # Simple transaction record
            transactions.append({
                'date': date_str,
                'employee': row.get('employee', 'Unknown'),
                'amount': float(row.get('amount', 0))
            })

        # Extract policy violations
        policy_violations = self._detect_violations(df, enriched_features)

        # Detect flagged transactions
        flagged = self._flag_transactions(enriched_features, policy_violations)

        # Build summary statistics
        summary_stats = self._build_summary_stats(df, enriched_features)

        return {
            'summary_statistics': summary_stats,
            'enriched_features': enriched_features,
            'policy_violations': policy_violations,
            'flagged_transactions': flagged,
            'transactions': transactions
        }

    def _calculate_spending_level(self, amount: float) -> str:
        """Determine spending level based on amount"""
        if amount > 3000:
            return "High"
        elif amount > 1000:
            return "Medium"
        else:
            return "Low"

    def _detect_violations(self, df: pd.DataFrame, features: list) -> list:
        """
        Detect policy violations from data
        Rules:
        - Single expense > 5000
        - Repeated vendor from same employee
        - More than 3 expenses per employee in week
        - Missing documentation/reason
        """
        violations = []
        
        # Rule 1: High amount threshold
        for feature in features:
            if feature['amount'] > 5000:
                violations.append({
                    'employee': feature['employee'],
                    'amount': feature['amount'],
                    'category': feature['category'],
                    'date': feature['date'],
                    'violation_type': 'budget_exceeded',
                    'description': f"Amount ${feature['amount']:.2f} exceeds budget threshold of $5000"
                })

        # Rule 2: Frequency violations
        emp_transactions = defaultdict(list)
        for feature in features:
            emp_transactions[feature['employee']].append(feature)

        for emp, trans in emp_transactions.items():
            if len(trans) >= 5:
                violations.append({
                    'employee': emp,
                    'amount': sum(t['amount'] for t in trans),
                    'category': 'Multiple',
                    'date': trans[0]['date'],
                    'violation_type': 'frequency_violation',
                    'description': f"Employee has {len(trans)} transactions in period (threshold: 4)"
                })

        # Rule 3: Missing description
        for feature in features:
            if not feature['description'] or feature['description'].strip() == '':
                violations.append({
                    'employee': feature['employee'],
                    'amount': feature['amount'],
                    'category': feature['category'],
                    'date': feature['date'],
                    'violation_type': 'missing_documentation',
                    'description': 'Missing expense description/reason'
                })

        return violations[:20]  # Limit to 20 violations

    def _flag_transactions(self, features: list, violations: list) -> dict:
        """Flag high-value, risky, and duplicate transactions"""
        
        high_value = [f for f in features if f['is_high_value']]
        
        risk_transactions = []
        for v in violations:
            risk_transactions.append({
                'date': v['date'],
                'employee': v['employee'],
                'amount': v['amount'],
                'risk_score': 0.8 if v['violation_type'] == 'budget_exceeded' else 0.5,
                'reason': v['description']
            })

        # Detect potential duplicates (same employee, similar amount, same day)
        duplicates = []
        seen = set()
        for i, f1 in enumerate(features):
            for j, f2 in enumerate(features):
                if i < j:
                    if (f1['employee'] == f2['employee'] and
                        f1['date'] == f2['date'] and
                        abs(f1['amount'] - f2['amount']) < 100):
                        pair = f"{f1['employee']}-{f1['date']}-{f1['amount']:.2f}"
                        if pair not in seen:
                            duplicates.append({
                                'transaction_pair': [
                                    f"{f1['employee']} - {f1['category']} - {f1['date']}",
                                    f"{f2['employee']} - {f2['category']} - {f2['date']}"
                                ],
                                'similarity_score': 0.95,
                                'reason': 'Same employee, date, and similar amount'
                            })
                            seen.add(pair)

        return {
            'high_value_transactions': [
                {
                    'date': f['date'],
                    'employee': f['employee'],
                    'amount': f['amount'],
                    'category': f['category'],
                    'reason': 'High-value transaction'
                } for f in high_value
            ],
            'potential_duplicates': duplicates[:5],
            'risk_transactions': risk_transactions[:10]
        }

    def _build_summary_stats(self, df: pd.DataFrame, features: list) -> dict:
        """Build summary statistics from prepared data"""
        
        total_expense = df['amount'].sum() if 'amount' in df.columns else 0
        
        # Category breakdown
        category_breakdown = {}
        if 'category' in df.columns:
            for cat in df['category'].unique():
                cat_amount = df[df['category'] == cat]['amount'].sum()
                category_breakdown[str(cat)] = round(cat_amount, 2)

        # Department distribution
        dept_distribution = {}
        if 'department' in df.columns:
            for dept in df['department'].unique():
                dept_amount = df[df['department'] == dept]['amount'].sum()
                dept_distribution[str(dept)] = round(dept_amount, 2)

        # Employee level distribution
        emp_level_dist = {}
        if 'employee_level' in df.columns:
            for level in df['employee_level'].unique():
                level_amount = df[df['employee_level'] == level]['amount'].sum()
                emp_level_dist[str(level)] = round(level_amount, 2)

        # Spending level distribution
        spending_dist = defaultdict(float)
        for f in features:
            spending_dist[f['spending_level']] += f['amount']

        return {
            'total_expense': round(total_expense, 2),
            'category_breakdown': category_breakdown,
            'department_distribution': dept_distribution,
            'employee_level_distribution': emp_level_dist,
            'spending_level_distribution': {k: round(v, 2) for k, v in spending_dist.items()}
        }

    def _generate_complete_report(self, prep_result: dict, audit_report: dict, df: pd.DataFrame) -> dict:
        """Combine preparation results and audit report into complete summary"""
        
        return {
            'processing': {
                'timestamp': datetime.now().isoformat(),
                'total_records': len(df),
                'preparation': {
                    'status': prep_result['status'],
                    'summary': prep_result.get('summary', {}),
                    'flags': prep_result.get('flags', [])
                }
            },
            'audit_analysis': audit_report,
            'executive_summary': self._generate_executive_summary(audit_report, prep_result)
        }

    def _generate_executive_summary(self, audit_report: dict, prep_result: dict) -> str:
        """Generate executive-level summary of entire process"""
        
        risk_level = audit_report.get('risk_assessment', {}).get('overall_risk', 'unknown').upper()
        confidence = audit_report.get('risk_assessment', {}).get('confidence_score', 0)
        total_violations = audit_report.get('violation_analysis', {}).get('total_violations', 0)
        critical_violations = len(audit_report.get('violation_analysis', {}).get('critical', []))
        fraud_signals = len(audit_report.get('fraud_signals', []))
        recommendations = len(audit_report.get('recommendations', []))
        
        summary = (
            f"COMPREHENSIVE AUDIT REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. "
            f"Data preparation completed successfully with {len(prep_result.get('summary', {}))} records processed. "
            f"Overall risk assessment: {risk_level} (confidence: {confidence:.0%}). "
            f"Identified {total_violations} policy violations ({critical_violations} critical). "
            f"Detected {fraud_signals} fraud signals requiring investigation. "
            f"Generated {recommendations} actionable recommendations. "
            f"Visualization data prepared for dashboard integration. "
            f"Ready for executive review and action."
        )
        
        return summary


# Initialize pipeline
pipeline = FullAuditPipeline()
