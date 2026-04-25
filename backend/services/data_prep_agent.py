"""
Data Preparation Agent Orchestrator
Coordinates the full pipeline: mapping → cleaning → enriching
"""

from typing import Dict, List, Tuple, Any
import pandas as pd
import numpy as np
import json
from datetime import datetime

from services.column_mapper import mapper
from services.data_cleaner import cleaner
from services.data_enricher import enricher


class DataPrepagentOrchestrator:
    """Main orchestrator for the data preparation pipeline"""
    
    def __init__(self):
        self.execution_log = []
        self.pipeline_status = {
            'mapping': 'pending',
            'cleaning': 'pending',
            'enrichment': 'pending'
        }
    
    def _log(self, stage: str, status: str, details: str = ""):
        """Log pipeline execution steps"""
        self.execution_log.append({
            'timestamp': datetime.now().isoformat(),
            'stage': stage,
            'status': status,
            'details': details
        })
    
    def _convert_to_json_serializable(self, obj):
        """Convert numpy/pandas types to JSON-serializable Python types"""
        if pd.isna(obj):
            return None
        if isinstance(obj, (pd.Timestamp, np.datetime64)):
            return str(obj.date()) if hasattr(obj, 'date') else str(obj)
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, (list, tuple)):
            return [self._convert_to_json_serializable(x) for x in obj]
        if isinstance(obj, dict):
            return {k: self._convert_to_json_serializable(v) for k, v in obj.items()}
        return obj
    
    def prepare(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Execute complete data preparation pipeline
        
        Returns:
            {
                'status': 'success' | 'partial' | 'error',
                'data': cleaned_and_enriched_dataframe,
                'summary': {...},
                'flags': {...},
                'execution_log': [...]
            }
        """
        result = {
            'status': 'pending',
            'data': None,
            'summary': {},
            'flags': {},
            'execution_log': [],
            'errors': []
        }
        
        try:
            # ===== STAGE 1: COLUMN MAPPING =====
            self._log('mapping', 'started')
            success, mapping, map_errors = mapper.map_columns(df)
            
            if not success:
                result['status'] = 'error'
                result['errors'].extend(map_errors)
                self._log('mapping', 'failed', str(map_errors))
                result['execution_log'] = self.execution_log
                return result
            
            df_mapped, map_warnings = mapper.apply_mapping(df)
            self.pipeline_status['mapping'] = 'complete'
            self._log('mapping', 'success', f"Mapped {len(mapping)} columns")
            
            if map_warnings:
                result['errors'].extend(map_warnings)
            
            # ===== STAGE 2: DATA CLEANING =====
            self._log('cleaning', 'started')
            df_cleaned, clean_report = cleaner.clean(df_mapped)
            
            if df_cleaned.empty:
                result['status'] = 'error'
                result['errors'].append("No valid data after cleaning")
                self._log('cleaning', 'failed', "Result is empty")
                result['execution_log'] = self.execution_log
                return result
            
            self.pipeline_status['cleaning'] = 'complete'
            self._log('cleaning', 'success', 
                     f"Cleaned {len(df_mapped) - len(df_cleaned)} invalid rows")
            
            # Store cleaning details
            result['cleaning_report'] = clean_report
            
            # ===== STAGE 3: FEATURE ENRICHMENT =====
            self._log('enrichment', 'started')
            df_enriched, enrich_report = enricher.enrich(df_cleaned)
            self.pipeline_status['enrichment'] = 'complete'
            self._log('enrichment', 'success', 
                     f"Added {len(df_enriched.columns) - len(df_cleaned.columns)} features")
            
            # Store enrichment details
            result['enrichment_report'] = enrich_report
            
            # ===== GENERATE SUMMARY =====
            result['status'] = 'success'
            result['data'] = df_enriched
            result['execution_log'] = self.execution_log
            result['summary'] = self._generate_summary(df_enriched, clean_report, enrich_report)
            result['flags'] = self._generate_flags(df_enriched, enrich_report)
            
        except Exception as e:
            result['status'] = 'error'
            result['errors'].append(str(e))
            self._log('orchestration', 'error', str(e))
            result['execution_log'] = self.execution_log
        
        return result
    
    def _generate_summary(self, df: pd.DataFrame, clean_report: Dict, 
                         enrich_report: Dict) -> Dict:
        """Generate comprehensive summary statistics"""
        date_min = df['date'].min()
        date_max = df['date'].max()
        
        summary = {
            'total_records': int(len(df)),
            'total_expense': float(df['amount'].sum()),
            'average_expense': float(df['amount'].mean()),
            'median_expense': float(df['amount'].median()),
            'max_expense': float(df['amount'].max()),
            'min_expense': float(df['amount'].min()),
            'std_deviation': float(df['amount'].std()),
            
            'category_breakdown': self._breakdown_by_column(df, 'category'),
            'department_breakdown': self._breakdown_by_column(df, 'inferred_department'),
            'employee_level_distribution': self._breakdown_by_column(df, 'employee_level'),
            'spending_level_distribution': self._breakdown_by_column(df, 'spending_level'),
            'risk_distribution': self._breakdown_by_column(df, 'risk_flag'),
            
            'unique_employees': int(df['employee'].nunique()),
            'unique_vendors': int(df['vendor'].nunique()),
            'unique_categories': int(df['category'].nunique()),
            
            'date_range': {
                'start': str(date_min.date()),
                'end': str(date_max.date()),
                'days': int((date_max - date_min).days)
            },
            
            'cleaning_statistics': clean_report,
            'enrichment_statistics': enrich_report
        }
        
        return summary
    
    def _breakdown_by_column(self, df: pd.DataFrame, column: str) -> Dict:
        """Calculate breakdown by column (sum, count, percentage)"""
        if column not in df.columns:
            return {}
        
        breakdown = df.groupby(column).agg({
            'amount': ['sum', 'count', 'mean']
        }).round(2)
        
        result = {}
        for idx in breakdown.index:
            total = breakdown.loc[idx, ('amount', 'sum')]
            count = breakdown.loc[idx, ('amount', 'count')]
            average = breakdown.loc[idx, ('amount', 'mean')]
            percentage = (total / df['amount'].sum() * 100) if df['amount'].sum() > 0 else 0
            
            result[str(idx)] = {
                'total': float(total),
                'count': int(count),
                'average': float(average),
                'percentage': float(percentage)
            }
        
        return result
    
    def _generate_flags(self, df: pd.DataFrame, enrich_report: Dict) -> Dict:
        """Generate flagged transactions for review"""
        flags = {
            'high_value_transactions': self._get_high_value_transactions(df),
            'risk_transactions': self._get_risk_transactions(df),
            'policy_violation_candidates': self._get_policy_violations(df),
            'potential_duplicates': self._get_potential_duplicates(df),
            'frequent_spenders': self._get_frequent_spenders(df)
        }
        
        return flags
    
    def _get_high_value_transactions(self, df: pd.DataFrame) -> List[Dict]:
        """Get high-value transactions for review"""
        high_value = df[df['is_high_value']].nlargest(10, 'amount')
        
        return [
            {
                'employee': str(row['employee']),
                'amount': self._convert_to_json_serializable(row['amount']),
                'category': str(row['category']),
                'vendor': str(row['vendor']),
                'date': str(row['date'].date()),
                'level': str(row['employee_level']),
                'risk': str(row['risk_flag'])
            }
            for _, row in high_value.iterrows()
        ]
    
    def _get_risk_transactions(self, df: pd.DataFrame) -> List[Dict]:
        """Get transactions flagged as risky"""
        risky = df[df['risk_flag'] != 'low'].head(20)
        
        return [
            {
                'employee': str(row['employee']),
                'amount': self._convert_to_json_serializable(row['amount']),
                'vendor': str(row['vendor']),
                'description': str(row['description'][:50]),
                'risk_level': str(row['risk_flag']),
                'keywords': str(row['risk_keywords']) if pd.notna(row['risk_keywords']) else '',
                'date': str(row['date'].date())
            }
            for _, row in risky.iterrows()
        ]
    
    def _get_policy_violations(self, df: pd.DataFrame) -> List[Dict]:
        """Get policy violation candidates (high-value + high-risk)"""
        violations = df[
            (df['is_high_value']) & 
            (df['risk_flag'] != 'low')
        ].head(10)
        
        return [
            {
                'employee': str(row['employee']),
                'amount': self._convert_to_json_serializable(row['amount']),
                'reason': f"High-value + {row['risk_flag']} risk",
                'vendor': str(row['vendor']),
                'date': str(row['date'].date()),
                'tags': str(row['behavioral_tags']) if pd.notna(row['behavioral_tags']) else 'none'
            }
            for _, row in violations.iterrows()
        ]
    
    def _get_potential_duplicates(self, df: pd.DataFrame) -> List[Dict]:
        """Get potential duplicate transactions"""
        duplicates = df[df['behavioral_tags'].str.contains('potential_duplicate', na=False)]
        
        return [
            {
                'employee': str(row['employee']),
                'vendor': str(row['vendor']),
                'amount': self._convert_to_json_serializable(row['amount']),
                'date': str(row['date'].date()),
                'description': str(row['description'][:50]) if pd.notna(row['description']) else ''
            }
            for _, row in duplicates.head(10).iterrows()
        ]
    
    def _get_frequent_spenders(self, df: pd.DataFrame) -> List[Dict]:
        """Get employees flagged as frequent spenders"""
        frequent = df[df['behavioral_tags'].str.contains('frequent_spender', na=False)]
        
        summary = frequent.groupby('employee').agg({
            'amount': ['sum', 'count', 'mean']
        }).sort_values(('amount', 'sum'), ascending=False).head(10)
        
        result = []
        for employee in summary.index:
            emp_data = frequent[frequent['employee'] == employee]
            result.append({
                'employee': str(employee),
                'total_expenses': self._convert_to_json_serializable(summary.loc[employee, ('amount', 'sum')]),
                'transaction_count': self._convert_to_json_serializable(summary.loc[employee, ('amount', 'count')]),
                'average_expense': self._convert_to_json_serializable(summary.loc[employee, ('amount', 'mean')]),
                'primary_category': str(emp_data['category'].mode().values[0]) if len(emp_data) > 0 and len(emp_data['category'].mode()) > 0 else 'unknown'
            })
        
        return result


# Singleton instance
orchestrator = DataPrepagentOrchestrator()
