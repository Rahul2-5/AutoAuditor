"""
Feature Enricher Service
Adds business intelligence to expense data
"""

from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
from datetime import datetime


class FeatureEnricher:
    """Enriches expense data with business intelligence features"""
    
    # Risk keywords for flagging suspicious transactions
    RISK_KEYWORDS = {
        'high_risk': ['casino', 'alcohol', 'bar', 'nightclub', 'luxury', 'casino', 'vip'],
        'medium_risk': ['personal', 'entertainment', 'spa', 'golf', 'country club']
    }
    
    # Department mapping based on category/vendor patterns
    DEPARTMENT_MAPPING = {
        'travel': ['operations', 'travel'],
        'software': ['it', 'technology', 'tech', 'software'],
        'hardware': ['it', 'technology', 'equipment'],
        'meals': ['hr', 'human resources', 'employee welfare'],
        'office': ['admin', 'administration', 'facilities'],
        'professional': ['hr', 'training', 'development'],
        'marketing': ['sales', 'marketing', 'business development'],
        'utilities': ['operations', 'facilities', 'admin']
    }
    
    def __init__(self):
        self.enrichment_report = {
            'high_value_transactions': 0,
            'risk_transactions': 0,
            'frequent_spenders': 0,
            'policy_violation_candidates': 0
        }
    
    def calculate_spending_levels(self, df: pd.DataFrame) -> pd.DataFrame:
        """Classify spending as low/medium/high using dynamic thresholds"""
        df = df.copy()
        
        # Calculate dynamic thresholds
        Q1 = df['amount'].quantile(0.33)
        Q2 = df['amount'].quantile(0.67)
        
        def classify_spending(amount):
            if amount <= Q1:
                return 'low'
            elif amount <= Q2:
                return 'medium'
            else:
                return 'high'
        
        df['spending_level'] = df['amount'].apply(classify_spending)
        
        # Flag high-value transactions (top 10%)
        high_value_threshold = df['amount'].quantile(0.90)
        df['is_high_value'] = df['amount'] > high_value_threshold
        self.enrichment_report['high_value_transactions'] = df['is_high_value'].sum()
        
        return df
    
    def detect_risk_flags(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detect risky transactions based on keywords and patterns"""
        df = df.copy()
        
        df['risk_flag'] = 'low'
        df['risk_keywords'] = ''
        
        # Check description and vendor for risk keywords
        for idx, row in df.iterrows():
            text = f"{row['description']} {row['vendor']}".lower()
            
            # High risk keywords
            high_risk_found = [kw for kw in self.RISK_KEYWORDS['high_risk'] if kw in text]
            if high_risk_found:
                df.at[idx, 'risk_flag'] = 'high'
                df.at[idx, 'risk_keywords'] = ', '.join(high_risk_found)
                continue
            
            # Medium risk keywords
            medium_risk_found = [kw for kw in self.RISK_KEYWORDS['medium_risk'] if kw in text]
            if medium_risk_found:
                df.at[idx, 'risk_flag'] = 'medium'
                df.at[idx, 'risk_keywords'] = ', '.join(medium_risk_found)
        
        self.enrichment_report['risk_transactions'] = (df['risk_flag'] != 'low').sum()
        
        return df
    
    def classify_department(self, df: pd.DataFrame) -> pd.DataFrame:
        """Infer department from category, vendor, or description"""
        df = df.copy()
        df['inferred_department'] = 'unknown'
        
        for idx, row in df.iterrows():
            category = row['category'].lower()
            vendor = row['vendor'].lower()
            description = row['description'].lower()
            
            text = f"{category} {vendor} {description}"
            
            # Try to match department keywords
            for dept, keywords in self.DEPARTMENT_MAPPING.items():
                if any(kw in text for kw in keywords):
                    # Map to standard departments
                    if 'it' in keywords or 'tech' in keywords:
                        df.at[idx, 'inferred_department'] = 'IT'
                    elif 'hr' in keywords or 'human' in keywords:
                        df.at[idx, 'inferred_department'] = 'HR'
                    elif 'sales' in keywords or 'marketing' in keywords:
                        df.at[idx, 'inferred_department'] = 'Sales & Marketing'
                    elif 'operations' in keywords or 'travel' in keywords:
                        df.at[idx, 'inferred_department'] = 'Operations'
                    elif 'admin' in keywords or 'facilities' in keywords:
                        df.at[idx, 'inferred_department'] = 'Administration'
                    break
        
        return df
    
    def classify_employee_level(self, df: pd.DataFrame) -> pd.DataFrame:
        """Infer employee level based on spending patterns and vendor types"""
        df = df.copy()
        df['employee_level'] = 'Mid-level'  # Default
        
        # Calculate spending statistics per employee
        employee_stats = df.groupby('employee').agg({
            'amount': ['sum', 'mean', 'max', 'count']
        }).round(2)
        
        # Define thresholds (percentile-based)
        high_spend_threshold = df['amount'].quantile(0.75)
        avg_spend_threshold = df['amount'].mean()
        
        for idx, row in df.iterrows():
            emp = row['employee']
            amount = row['amount']
            
            # Heuristics for employee level
            if amount > high_spend_threshold:
                # High spenders likely senior
                df.at[idx, 'employee_level'] = 'Senior'
            elif amount < avg_spend_threshold * 0.5:
                # Low spenders likely junior
                df.at[idx, 'employee_level'] = 'Junior'
            else:
                df.at[idx, 'employee_level'] = 'Mid-level'
            
            # Check for executive indicators (specific vendors)
            vendor = row['vendor'].lower()
            if any(exec_vendor in vendor for exec_vendor in ['private', 'executive', 'first class', 'suite']):
                df.at[idx, 'employee_level'] = 'Executive'
        
        return df
    
    def add_behavioral_tags(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add behavioral tags for compliance and analysis"""
        df = df.copy()
        df['behavioral_tags'] = ''
        
        # Identify frequent spenders
        employee_counts = df.groupby('employee').size()
        frequent_threshold = employee_counts.quantile(0.75)
        frequent_employees = employee_counts[employee_counts > frequent_threshold].index
        
        # Calculate totals per employee
        employee_totals = df.groupby('employee')['amount'].sum()
        high_total_threshold = employee_totals.quantile(0.75)
        high_total_employees = employee_totals[employee_totals > high_total_threshold].index
        
        tags_list = []
        
        for idx, row in df.iterrows():
            tags = []
            
            # Tag frequent spenders
            if row['employee'] in frequent_employees:
                tags.append('frequent_spender')
                self.enrichment_report['frequent_spenders'] = \
                    df[df['employee'].isin(frequent_employees)]['employee'].nunique()
            
            # Tag high-risk transactions
            if row['risk_flag'] != 'low':
                tags.append('high_risk_transaction')
            
            # Tag policy violation candidates
            if row['is_high_value'] and row['risk_flag'] != 'low':
                tags.append('policy_violation_candidate')
                self.enrichment_report['policy_violation_candidates'] += 1
            
            # Tag potential duplicate vendors (same employee, same vendor, same day)
            same_vendor_same_day = (
                (df['employee'] == row['employee']) &
                (df['vendor'] == row['vendor']) &
                (df['date'] == row['date'])
            )
            if same_vendor_same_day.sum() > 1:
                tags.append('potential_duplicate')
            
            df.at[idx, 'behavioral_tags'] = '; '.join(tags) if tags else 'clean'
        
        return df
    
    def enrich(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        Execute full feature enrichment
        Returns: (enriched_df, report)
        """
        self.enrichment_report = {
            'high_value_transactions': 0,
            'risk_transactions': 0,
            'frequent_spenders': 0,
            'policy_violation_candidates': 0
        }
        
        df = self.calculate_spending_levels(df)
        df = self.detect_risk_flags(df)
        df = self.classify_department(df)
        df = self.classify_employee_level(df)
        df = self.add_behavioral_tags(df)
        
        return df, self.enrichment_report


# Singleton instance
enricher = FeatureEnricher()
