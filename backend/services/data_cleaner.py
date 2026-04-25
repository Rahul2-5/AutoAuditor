"""
Data Cleaner Service
Validates and cleans data according to business rules
"""

from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
from datetime import datetime


class DataCleaner:
    """Production-grade data cleaning engine"""
    
    def __init__(self):
        self.cleaning_report = {
            'duplicates_removed': 0,
            'rows_with_nulls_dropped': 0,
            'invalid_dates': 0,
            'invalid_amounts': 0,
            'invalid_employees': 0,
            'warnings': []
        }
    
    def validate_schema(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate that all required columns exist"""
        required_cols = ['date', 'employee', 'amount', 'category', 'vendor', 'description']
        missing = [col for col in required_cols if col not in df.columns]
        
        errors = []
        if missing:
            errors.append(f"Missing required columns: {missing}")
        
        if df.empty:
            errors.append("Dataset is empty")
        
        return len(errors) == 0, errors
    
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows"""
        initial_count = len(df)
        df_clean = df.drop_duplicates()
        self.cleaning_report['duplicates_removed'] = initial_count - len(df_clean)
        return df_clean
    
    def clean_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert dates to datetime, handle errors"""
        df = df.copy()
        invalid_count = 0
        
        try:
            # Try to convert with inferred format
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            invalid_count = df['date'].isna().sum()
            self.cleaning_report['invalid_dates'] = invalid_count
            
            # Drop rows with invalid dates
            df = df[df['date'].notna()]
            
        except Exception as e:
            self.cleaning_report['warnings'].append(f"Date cleaning error: {str(e)}")
        
        return df
    
    def clean_amounts(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert amounts to float, validate ranges"""
        df = df.copy()
        initial_count = len(df)
        
        try:
            # Convert to numeric
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            
            # Flag invalid conversions
            invalid_count = df['amount'].isna().sum()
            self.cleaning_report['invalid_amounts'] = invalid_count
            
            # Remove rows with null amounts
            df = df[df['amount'].notna()]
            
            # Remove negative amounts (data error)
            negative_count = (df['amount'] < 0).sum()
            if negative_count > 0:
                self.cleaning_report['warnings'].append(
                    f"Removed {negative_count} rows with negative amounts"
                )
                df = df[df['amount'] >= 0]
            
            # Cap extreme outliers as warnings (don't remove)
            max_amount = df['amount'].quantile(0.999)
            extreme_count = (df['amount'] > max_amount * 2).sum()
            if extreme_count > 0:
                self.cleaning_report['warnings'].append(
                    f"Flagged {extreme_count} extreme outlier amounts for review"
                )
            
        except Exception as e:
            self.cleaning_report['warnings'].append(f"Amount cleaning error: {str(e)}")
        
        return df
    
    def clean_text_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize text fields: trim, lowercase, remove extra spaces"""
        df = df.copy()
        text_cols = ['employee', 'category', 'vendor', 'description']
        
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.lower()
                
                # Remove multiple spaces
                df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
                
                # Remove rows with empty text (except description which can be empty)
                if col != 'description':
                    initial = len(df)
                    df = df[df[col].str.len() > 0]
                    removed = initial - len(df)
                    if removed > 0 and col == 'employee':
                        self.cleaning_report['invalid_employees'] = removed
        
        return df
    
    def handle_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle null values intelligently"""
        df = df.copy()
        initial_count = len(df)
        
        # Required fields: no nulls allowed
        required_cols = ['date', 'employee', 'amount', 'category', 'vendor']
        
        for col in required_cols:
            if col in df.columns:
                df = df[df[col].notna()]
        
        # Optional field: description can be null (fill with "No description")
        if 'description' in df.columns:
            df['description'] = df['description'].fillna('No description')
        
        rows_dropped = initial_count - len(df)
        self.cleaning_report['rows_with_nulls_dropped'] = rows_dropped
        
        return df
    
    def clean(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        Execute full cleaning pipeline
        Returns: (cleaned_df, report)
        """
        self.cleaning_report = {
            'duplicates_removed': 0,
            'rows_with_nulls_dropped': 0,
            'invalid_dates': 0,
            'invalid_amounts': 0,
            'invalid_employees': 0,
            'warnings': []
        }
        
        # Step 1: Validate schema
        valid, errors = self.validate_schema(df)
        if not valid:
            self.cleaning_report['warnings'].extend(errors)
            return pd.DataFrame(), self.cleaning_report
        
        # Step 2: Remove duplicates
        df = self.remove_duplicates(df)
        
        # Step 3: Clean individual fields
        df = self.clean_dates(df)
        df = self.clean_amounts(df)
        df = self.clean_text_fields(df)
        
        # Step 4: Handle nulls
        df = self.handle_nulls(df)
        
        # Step 5: Reset index
        df = df.reset_index(drop=True)
        
        return df, self.cleaning_report


# Singleton instance
cleaner = DataCleaner()
