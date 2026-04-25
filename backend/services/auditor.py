import json
from typing import List, Dict, Any, Tuple
from datetime import datetime
from collections import defaultdict, Counter
import statistics


class FinancialAuditor:
    """
    Advanced AI Financial Auditor for enterprise expense auditing,
    fraud detection, and compliance analysis.
    """

    def __init__(self):
        self.violations_severity = {
            'budget_exceeded': 'critical',
            'policy_violation': 'moderate',
            'duplicate_transaction': 'critical',
            'missing_documentation': 'moderate',
            'unauthorized_category': 'moderate',
            'high_value_alert': 'moderate',
            'frequency_violation': 'minor'
        }

    def analyze(self, audit_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main audit analysis function that processes expense data
        and generates comprehensive audit report.
        """
        try:
            # Extract data
            summary_stats = audit_data.get('summary_statistics', {})
            enriched_features = audit_data.get('enriched_features', [])
            policy_violations = audit_data.get('policy_violations', [])
            flagged_transactions = audit_data.get('flagged_transactions', {})
            raw_transactions = audit_data.get('transactions', [])

            # Run analysis modules
            risk_assessment = self._assess_risk(
                summary_stats, enriched_features, policy_violations, flagged_transactions
            )
            violation_analysis = self._analyze_violations(policy_violations, enriched_features)
            anomalies = self._detect_anomalies(enriched_features, raw_transactions, summary_stats)
            fraud_signals = self._detect_fraud_signals(
                enriched_features, policy_violations, flagged_transactions, raw_transactions
            )
            financial_insights = self._generate_financial_insights(
                summary_stats, enriched_features, violation_analysis
            )
            recommendations = self._generate_recommendations(
                risk_assessment, violation_analysis, anomalies, financial_insights
            )
            cost_optimization_tips = self._generate_cost_optimization_tips(
                summary_stats, enriched_features, violation_analysis
            )
            visualization_data = self._prepare_visualization_data(
                summary_stats, enriched_features, violation_analysis, raw_transactions
            )
            final_summary = self._generate_audit_summary(
                risk_assessment, violation_analysis, fraud_signals, recommendations
            )

            # Compile final report
            report = {
                "risk_assessment": risk_assessment,
                "violation_analysis": violation_analysis,
                "anomalies": anomalies,
                "fraud_signals": fraud_signals,
                "financial_insights": financial_insights,
                "recommendations": recommendations,
                "cost_optimization_tips": cost_optimization_tips,
                "visualization": visualization_data,
                "summary_statistics": summary_stats,
                "final_audit_summary": final_summary
            }

            return report

        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "message": "Audit analysis failed"
            }

    def _assess_risk(self, summary_stats: Dict, enriched_features: List[Dict],
                     policy_violations: List[Dict], flagged_transactions: Dict) -> Dict[str, Any]:
        """
        Re-evaluate overall risk level considering multiple factors.
        """
        risk_score = 0.0
        key_risks = []

        total_amount = summary_stats.get('total_expense', 0)
        num_transactions = len(enriched_features)

        # Factor 1: Violation frequency
        violation_count = len(policy_violations)
        violation_rate = violation_count / max(num_transactions, 1)
        if violation_rate > 0.3:
            risk_score += 0.4
            key_risks.append(f"High violation frequency: {violation_rate:.1%} of transactions")
        elif violation_rate > 0.1:
            risk_score += 0.2
            key_risks.append(f"Moderate violation frequency: {violation_rate:.1%} of transactions")

        # Factor 2: High-value transaction density
        high_value_count = len([f for f in enriched_features if f.get('is_high_value')])
        high_value_rate = high_value_count / max(num_transactions, 1)
        if high_value_rate > 0.4:
            risk_score += 0.3
            key_risks.append(f"High concentration of high-value transactions: {high_value_rate:.1%}")

        # Factor 3: Risk-flagged transactions
        risk_flagged = len([f for f in enriched_features if f.get('risk_flag')])
        if risk_flagged > 0:
            risk_percentage = risk_flagged / max(num_transactions, 1)
            risk_score += min(0.25, risk_percentage * 0.5)
            key_risks.append(f"{risk_flagged} transactions flagged as risky")

        # Factor 4: Duplicate flagging
        duplicates = flagged_transactions.get('potential_duplicates', [])
        if duplicates:
            risk_score += 0.15
            key_risks.append(f"Found {len(duplicates)} potential duplicate transactions")

        # Factor 5: Spending concentration
        categories = summary_stats.get('category_breakdown', {})
        if categories:
            total_cat = sum(categories.values())
            for cat, amount in categories.items():
                concentration = amount / total_cat
                if concentration > 0.4:
                    risk_score += 0.2
                    key_risks.append(f"High spending concentration in {cat}: {concentration:.1%}")

        # Normalize score
        confidence_score = min(1.0, risk_score)

        # Determine risk level
        if confidence_score >= 0.7:
            overall_risk = "high"
        elif confidence_score >= 0.4:
            overall_risk = "medium"
        else:
            overall_risk = "low"

        return {
            "overall_risk": overall_risk,
            "confidence_score": round(confidence_score, 2),
            "key_risks": key_risks[:5]  # Top 5 risks
        }

    def _analyze_violations(self, policy_violations: List[Dict],
                           enriched_features: List[Dict]) -> Dict[str, Any]:
        """
        Analyze and categorize violations, identify repeat offenders.
        """
        critical = []
        moderate = []
        minor = []
        repeat_offenders_dict = defaultdict(list)

        for violation in policy_violations:
            violation_info = {
                "employee": violation.get('employee'),
                "amount": violation.get('amount'),
                "category": violation.get('category'),
                "date": violation.get('date'),
                "violation_type": violation.get('violation_type', 'unknown'),
                "description": violation.get('description', '')
            }

            # Categorize by severity
            violation_type = violation.get('violation_type', 'unknown').lower()
            severity = self.violations_severity.get(violation_type, 'minor')

            if severity == 'critical':
                critical.append(violation_info)
            elif severity == 'moderate':
                moderate.append(violation_info)
            else:
                minor.append(violation_info)

            # Track repeat offenders
            employee = violation.get('employee')
            if employee:
                repeat_offenders_dict[employee].append(violation_info)

        # Identify repeat offenders (3+ violations)
        repeat_offenders = [
            {
                "employee": emp,
                "violation_count": len(violations),
                "total_amount": sum(v.get('amount', 0) for v in violations),
                "violations": violations
            }
            for emp, violations in repeat_offenders_dict.items()
            if len(violations) >= 3
        ]

        # Sort by violation count
        repeat_offenders.sort(key=lambda x: x['violation_count'], reverse=True)

        return {
            "total_violations": len(policy_violations),
            "critical": critical,
            "moderate": moderate,
            "minor": minor,
            "repeat_offenders": repeat_offenders
        }

    def _detect_anomalies(self, enriched_features: List[Dict],
                         raw_transactions: List[Dict],
                         summary_stats: Dict) -> List[Dict[str, Any]]:
        """
        Detect hidden anomalies not explicitly flagged.
        """
        anomalies = []

        if not enriched_features:
            return anomalies

        # Anomaly 1: Category dominance (>40%)
        categories = defaultdict(float)
        total = 0
        for feature in enriched_features:
            cat = feature.get('category', 'unknown')
            amount = feature.get('amount', 0)
            categories[cat] += amount
            total += amount

        if total > 0:
            for cat, amount in categories.items():
                concentration = amount / total
                if concentration > 0.4:
                    anomalies.append({
                        "type": "category_dominance",
                        "category": cat,
                        "concentration": round(concentration, 2),
                        "amount": round(amount, 2),
                        "description": f"Category '{cat}' represents {concentration:.1%} of total spending"
                    })

        # Anomaly 2: Unusual spending spikes
        if raw_transactions:
            amounts = sorted([t.get('amount', 0) for t in raw_transactions if t.get('amount')])
            if len(amounts) >= 3:
                mean_amount = statistics.mean(amounts)
                stdev = statistics.stdev(amounts) if len(amounts) > 1 else 0
                threshold = mean_amount + (2 * stdev)

                spike_transactions = [
                    t for t in raw_transactions
                    if t.get('amount', 0) > threshold
                ]

                if spike_transactions:
                    anomalies.append({
                        "type": "spending_spike",
                        "threshold": round(threshold, 2),
                        "spike_count": len(spike_transactions),
                        "description": f"Detected {len(spike_transactions)} transactions exceeding normal spending patterns"
                    })

        # Anomaly 3: Abnormal employee behavior
        employee_stats = defaultdict(list)
        for feature in enriched_features:
            emp = feature.get('employee')
            amount = feature.get('amount', 0)
            if emp:
                employee_stats[emp].append(amount)

        for emp, amounts in employee_stats.items():
            if len(amounts) >= 2:
                emp_mean = statistics.mean(amounts)
                emp_stdev = statistics.stdev(amounts) if len(amounts) > 1 else 0
                high_var_threshold = emp_stdev / max(emp_mean, 1)

                if high_var_threshold > 1.0:  # High variance
                    anomalies.append({
                        "type": "behavioral_anomaly",
                        "employee": emp,
                        "variance_ratio": round(high_var_threshold, 2),
                        "description": f"Employee '{emp}' shows inconsistent spending patterns"
                    })

        return anomalies

    def _detect_fraud_signals(self, enriched_features: List[Dict],
                             policy_violations: List[Dict],
                             flagged_transactions: Dict,
                             raw_transactions: List[Dict]) -> List[Dict[str, Any]]:
        """
        Identify suspicious patterns indicating potential fraud.
        """
        fraud_signals = []

        # Signal 1: High-value + violation combination
        high_value_violations = [
            v for v in policy_violations
            if any(f.get('amount') == v.get('amount') and f.get('is_high_value')
                   for f in enriched_features)
        ]

        if high_value_violations:
            fraud_signals.append({
                "type": "high_value_violation",
                "severity": "critical",
                "count": len(high_value_violations),
                "description": f"{len(high_value_violations)} high-value transactions with policy violations detected",
                "transactions": high_value_violations[:5]
            })

        # Signal 2: Potential duplicates
        duplicates = flagged_transactions.get('potential_duplicates', [])
        if duplicates:
            fraud_signals.append({
                "type": "potential_duplicate",
                "severity": "critical",
                "count": len(duplicates),
                "description": f"{len(duplicates)} potential duplicate transactions detected"
            })

        # Signal 3: Repeated vendor usage in risky context
        vendor_usage = defaultdict(int)
        for feature in enriched_features:
            if feature.get('risk_flag'):
                vendor = feature.get('vendor', 'unknown')
                vendor_usage[vendor] += 1

        repeated_risky_vendors = [
            (vendor, count) for vendor, count in vendor_usage.items() if count >= 3
        ]

        if repeated_risky_vendors:
            fraud_signals.append({
                "type": "repeated_risky_vendor",
                "severity": "high",
                "count": len(repeated_risky_vendors),
                "description": f"Multiple risky transactions from same vendors",
                "vendors": [{"vendor": v[0], "risky_count": v[1]} for v in repeated_risky_vendors]
            })

        # Signal 4: Inconsistent behavior pattern
        high_value_txns = flagged_transactions.get('high_value_transactions', [])
        if high_value_txns and len(enriched_features) > 0:
            violation_ratio = len(policy_violations) / len(enriched_features)
            high_value_ratio = len(high_value_txns) / len(enriched_features)

            if violation_ratio > 0.2 and high_value_ratio > 0.2:
                fraud_signals.append({
                    "type": "inconsistent_behavior",
                    "severity": "high",
                    "violation_ratio": round(violation_ratio, 2),
                    "high_value_ratio": round(high_value_ratio, 2),
                    "description": "Unusual pattern combining high violations and high-value transactions"
                })

        return fraud_signals

    def _generate_financial_insights(self, summary_stats: Dict,
                                     enriched_features: List[Dict],
                                     violation_analysis: Dict) -> List[Dict[str, Any]]:
        """
        Generate actionable financial insights.
        """
        insights = []

        # Insight 1: Top spending categories
        categories = summary_stats.get('category_breakdown', {})
        if categories:
            sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
            insights.append({
                "type": "spending_distribution",
                "description": f"Top spending categories: {sorted_cats[0][0]} (${sorted_cats[0][1]:,.2f})",
                "details": sorted_cats
            })

        # Insight 2: Department efficiency
        depts = summary_stats.get('department_distribution', {})
        if depts:
            sorted_depts = sorted(depts.items(), key=lambda x: x[1], reverse=True)
            insights.append({
                "type": "department_spending",
                "description": f"Highest spending department: {sorted_depts[0][0]} (${sorted_depts[0][1]:,.2f})",
                "details": sorted_depts
            })

        # Insight 3: Violation cost impact
        total_violation_amount = sum(
            v.get('amount', 0) for violations in [
                violation_analysis.get('critical', []),
                violation_analysis.get('moderate', []),
                violation_analysis.get('minor', [])
            ] for v in violations
        )

        if total_violation_amount > 0:
            total_expense = summary_stats.get('total_expense', 1)
            violation_percentage = (total_violation_amount / total_expense) * 100
            insights.append({
                "type": "violation_cost_impact",
                "description": f"Violations account for ${total_violation_amount:,.2f} ({violation_percentage:.1f}%) of total spending",
                "amount": round(total_violation_amount, 2),
                "percentage": round(violation_percentage, 2)
            })

        # Insight 4: Employee level analysis
        emp_levels = summary_stats.get('employee_level_distribution', {})
        if emp_levels:
            insights.append({
                "type": "employee_level_distribution",
                "description": "Spending by employee level",
                "details": emp_levels
            })

        # Insight 5: High-value transaction analysis
        high_value_count = len([f for f in enriched_features if f.get('is_high_value')])
        if high_value_count > 0:
            insights.append({
                "type": "high_value_transactions",
                "description": f"{high_value_count} high-value transactions detected",
                "count": high_value_count,
                "recommendation": "Review high-value transactions for legitimacy"
            })

        return insights

    def _generate_recommendations(self, risk_assessment: Dict,
                                 violation_analysis: Dict,
                                 anomalies: List[Dict],
                                 financial_insights: List[Dict]) -> List[Dict[str, Any]]:
        """
        Generate actionable recommendations based on analysis.
        """
        recommendations = []

        # Recommendation 1: Address critical violations
        critical_count = len(violation_analysis.get('critical', []))
        if critical_count > 0:
            recommendations.append({
                "title": "Resolve Critical Policy Violations",
                "description": f"Found {critical_count} critical violations. Immediately review and take corrective action with involved employees.",
                "priority": "high"
            })

        # Recommendation 2: Monitor repeat offenders
        repeat_offenders = violation_analysis.get('repeat_offenders', [])
        if repeat_offenders:
            recommendations.append({
                "title": "Enforce Compliance for Repeat Offenders",
                "description": f"{len(repeat_offenders)} employees have multiple violations. Implement mandatory compliance training and monitoring.",
                "priority": "high"
            })

        # Recommendation 3: Investigate fraud signals
        if len(anomalies) >= 2:
            recommendations.append({
                "title": "Investigate Detected Anomalies",
                "description": f"Detected {len(anomalies)} anomalies in spending patterns. Conduct detailed investigation before processing reimbursements.",
                "priority": "high"
            })

        # Recommendation 4: Strengthen approval process
        total_violations = violation_analysis.get('total_violations', 0)
        if total_violations > 10:
            recommendations.append({
                "title": "Strengthen Expense Approval Process",
                "description": "High violation count indicates weak approval controls. Implement stricter pre-approval checks and automated compliance validation.",
                "priority": "medium"
            })

        # Recommendation 5: Category-specific controls
        high_cat_violations = [
            cat for insight in financial_insights
            if insight.get('type') == 'spending_distribution'
            for cat, amount in insight.get('details', [])
        ]

        if high_cat_violations:
            recommendations.append({
                "title": "Implement Category-Specific Controls",
                "description": "Establish spending caps and approval requirements for high-risk categories.",
                "priority": "medium"
            })

        # Recommendation 6: Duplicate prevention
        if len(anomalies) > 0 and any(a.get('type') == 'potential_duplicate' for a in anomalies):
            recommendations.append({
                "title": "Implement Duplicate Detection System",
                "description": "Automate duplicate transaction detection using vendor name, amount, and date matching.",
                "priority": "medium"
            })

        # Recommendation 7: Regular audit cycles
        recommendations.append({
            "title": "Establish Regular Audit Cycles",
            "description": "Schedule weekly audits for high-risk categories and monthly comprehensive reviews of all expenses.",
            "priority": "low"
        })

        return recommendations[:7]  # Top 7 recommendations

    def _generate_cost_optimization_tips(self, summary_stats: Dict,
                                        enriched_features: List[Dict],
                                        violation_analysis: Dict) -> List[Dict[str, Any]]:
        """
        Generate smart cost optimization suggestions.
        """
        tips = []
        total_expense = summary_stats.get('total_expense', 0)

        # Tip 1: High spending → cost-cutting
        if total_expense > 100000:
            tips.append({
                "tip": "Negotiate volume discounts with top vendors",
                "impact": "high",
                "description": "Given high spending levels, negotiate better rates with frequent vendors"
            })

            tips.append({
                "tip": "Implement vendor consolidation strategy",
                "impact": "high",
                "description": "Reduce vendor count to leverage bulk purchasing power"
            })

        # Tip 2: Violation-driven savings
        total_violation_amount = sum(
            v.get('amount', 0) for violations in [
                violation_analysis.get('critical', []),
                violation_analysis.get('moderate', []),
                violation_analysis.get('minor', [])
            ] for v in violations
        )

        if total_violation_amount > 0:
            tips.append({
                "tip": "Eliminate policy violation costs",
                "impact": "high",
                "description": f"Preventing violations can save ${total_violation_amount:,.2f} annually"
            })

        # Tip 3: Category-specific optimization
        categories = summary_stats.get('category_breakdown', {})
        if categories:
            top_category = max(categories.items(), key=lambda x: x[1])
            if top_category[1] > total_expense * 0.3:
                tips.append({
                    "tip": f"Optimize '{top_category[0]}' category spending",
                    "impact": "high",
                    "description": f"This category represents {(top_category[1]/total_expense)*100:.0f}% of expenses. Review for efficiency gains."
                })

        # Tip 4: Low-violation optimization
        violation_rate = violation_analysis.get('total_violations', 0) / max(len(enriched_features), 1)
        if violation_rate < 0.1:
            tips.append({
                "tip": "Invest in efficiency improvements",
                "impact": "medium",
                "description": "Low violation rate shows strong compliance. Focus on process efficiency rather than control tightening."
            })

        # Tip 5: Behavioral insights
        emp_levels = summary_stats.get('employee_level_distribution', {})
        if emp_levels:
            tips.append({
                "tip": "Implement role-based spending policies",
                "impact": "medium",
                "description": "Tailor spending limits and approval requirements by employee level for optimal efficiency"
            })

        # Tip 6: Technology investment
        tips.append({
            "tip": "Automate expense processing and validation",
            "impact": "medium",
            "description": "Reduce manual review time and improve compliance with intelligent automation"
        })

        return tips

    def _prepare_visualization_data(self, summary_stats: Dict,
                                   enriched_features: List[Dict],
                                   violation_analysis: Dict,
                                   raw_transactions: List[Dict]) -> Dict[str, Any]:
        """
        Prepare structured data for frontend visualization.
        """
        visualization = {}

        def _get_value(val):
            """Helper to extract numeric value from potential dictionary result"""
            if isinstance(val, dict):
                return val.get('total', val.get('sum', 0))
            return val

        # 1. Category distribution
        categories = summary_stats.get('category_breakdown', {})
        cat_items = [(cat, _get_value(val)) for cat, val in categories.items()]
        visualization['category_distribution'] = [
            {"name": cat, "value": round(amount, 2)}
            for cat, amount in sorted(cat_items, key=lambda x: x[1], reverse=True)
        ]

        # 2. Department distribution
        # Try both common keys used in the pipeline
        departments = summary_stats.get('department_distribution') or summary_stats.get('department_breakdown', {})
        dept_items = [(dept, _get_value(val)) for dept, val in departments.items()]
        visualization['department_distribution'] = [
            {"name": dept, "value": round(amount, 2)}
            for dept, amount in sorted(dept_items, key=lambda x: x[1], reverse=True)
        ]

        # 3. Employee level distribution
        emp_levels = summary_stats.get('employee_level_distribution', {})
        level_items = [(level, _get_value(val)) for level, val in emp_levels.items()]
        visualization['employee_level_distribution'] = [
            {"name": level, "value": round(amount, 2)}
            for level, amount in sorted(level_items, key=lambda x: x[1], reverse=True)
        ]

        # 4. Spending trend (by date)
        spending_by_date = defaultdict(float)
        for txn in raw_transactions:
            date = txn.get('date', 'unknown')
            # Handle potential empty or nan dates
            if not date or str(date).lower() == 'nan':
                date = 'unknown'
            amount = txn.get('amount', 0)
            spending_by_date[str(date)] += amount

        # Sort dates properly (assuming YYYY-MM-DD or similar sortable string)
        sorted_trend = [
            {"date": date, "amount": round(amount, 2)}
            for date, amount in sorted(spending_by_date.items())
        ]
        
        # Take the LATEST 30 points if we have many
        visualization['spending_trend'] = sorted_trend[-30:] if len(sorted_trend) > 30 else sorted_trend

        # 5. Top spenders
        top_spenders = defaultdict(float)
        for feature in enriched_features:
            emp = feature.get('employee', 'unknown')
            amount = feature.get('amount', 0)
            top_spenders[emp] += amount

        visualization['top_spenders'] = [
            {"employee": emp, "amount": round(amount, 2)}
            for emp, amount in sorted(top_spenders.items(), key=lambda x: x[1], reverse=True)
        ][:10]

        # 5. Violation breakdown
        violation_breakdown = {
            "critical": len(violation_analysis.get('critical', [])),
            "moderate": len(violation_analysis.get('moderate', [])),
            "minor": len(violation_analysis.get('minor', []))
        }
        visualization['violation_breakdown'] = [
            {"type": k, "count": v} for k, v in violation_breakdown.items()
        ]

        return visualization

    def _generate_audit_summary(self, risk_assessment: Dict,
                               violation_analysis: Dict,
                               fraud_signals: List[Dict],
                               recommendations: List[Dict]) -> str:
        """
        Generate final executive audit summary.
        """
        risk_level = risk_assessment.get('overall_risk', 'unknown').upper()
        confidence = risk_assessment.get('confidence_score', 0)
        total_violations = violation_analysis.get('total_violations', 0)
        critical_violations = len(violation_analysis.get('critical', []))
        repeat_offenders = len(violation_analysis.get('repeat_offenders', []))
        fraud_count = len(fraud_signals)

        summary = (
            f"AUDIT REPORT SUMMARY: Overall Risk Assessment is {risk_level} "
            f"(Confidence: {confidence:.0%}). "
            f"Identified {total_violations} total policy violations, including {critical_violations} critical cases. "
            f"Found {repeat_offenders} repeat offenders requiring immediate attention. "
            f"Detected {fraud_count} potential fraud signals warranting investigation. "
            f"Provided {len(recommendations)} actionable recommendations prioritized by severity. "
            f"Immediate action required on critical violations before expense approval."
        )

        return summary


# Initialize auditor instance
auditor = FinancialAuditor()
