"""
Dynamic Column Mapper
Maps arbitrary CSV columns to canonical schema with intelligent fallback strategies
"""

from typing import Dict, Tuple, Optional
import pandas as pd


class ColumnMapper:
    """Intelligently maps input columns to required canonical schema"""
    
    # Define all possible aliases for each canonical field
    FIELD_ALIASES = {
        'date': [
            'date', 'transaction_date', 'expense_date', 'dt', 'txdate',
            'posted_date', 'transaction_dt', 'entry_date'
        ],
        'employee': [
            'employee', 'emp', 'user', 'name', 'staff', 'submitter',
            'expense_by', 'submitted_by', 'employee_name'
        ],
        'amount': [
            'amount', 'amt', 'price', 'value', 'cost', 'expense',
            'total', 'expense_amount', 'transaction_amount'
        ],
        'category': [
            'category', 'type', 'expense_type', 'cat', 'expensetype',
            'expense_category', 'classification'
        ],
        'vendor': [
            'vendor', 'merchant', 'shop', 'company', 'supplier',
            'merchant_name', 'vendor_name', 'store'
        ],
        'description': [
            'description', 'desc', 'details', 'memo', 'note', 'notes',
            'purpose', 'expense_description', 'remarks', 'comment'
        ]
    }
    
    REQUIRED_FIELDS = ['date', 'employee', 'amount', 'category', 'vendor', 'description']
    
    def __init__(self):
        self.input_columns = []
        self.mapping = {}
        self.unmapped_columns = []
    
    def normalize_column_name(self, col: str) -> str:
        """Normalize column name: strip, lowercase, remove special chars"""
        return col.strip().lower().replace('_', '').replace('-', '').replace(' ', '')
    
    def find_best_match(self, input_col: str, field_aliases: list) -> Optional[str]:
        """Find best match using exact and fuzzy matching"""
        normalized_input = self.normalize_column_name(input_col)
        
        # Exact match
        for alias in field_aliases:
            if self.normalize_column_name(alias) == normalized_input:
                return input_col
        
        # Substring match (for cases like "transaction_date" → "date")
        for alias in field_aliases:
            normalized_alias = self.normalize_column_name(alias)
            if normalized_alias in normalized_input or normalized_input in normalized_alias:
                return input_col
        
        return None
    
    def map_columns(self, df: pd.DataFrame) -> Tuple[bool, Dict, list]:
        """
        Map input columns to canonical schema
        Returns: (success, mapping_dict, error_messages)
        """
        self.input_columns = list(df.columns)
        self.mapping = {}
        errors = []
        
        # Try to map each required field
        for canonical_field in self.REQUIRED_FIELDS:
            field_aliases = self.FIELD_ALIASES[canonical_field]
            matched_column = None
            
            # Find matching input column
            for input_col in self.input_columns:
                if self.find_best_match(input_col, field_aliases):
                    matched_column = input_col
                    break
            
            if matched_column:
                self.mapping[canonical_field] = matched_column
            else:
                errors.append(
                    f"Cannot map '{canonical_field}'. Looked for: {', '.join(field_aliases[:3])}..."
                )
        
        # Track unmapped input columns (informational)
        mapped_input_cols = set(self.mapping.values())
        self.unmapped_columns = [col for col in self.input_columns if col not in mapped_input_cols]
        
        success = len(self.mapping) == len(self.REQUIRED_FIELDS)
        return success, self.mapping, errors
    
    def apply_mapping(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, list]:
        """
        Apply column mapping to dataframe
        Returns: (renamed_df_with_additional_features, warnings)
        
        Keeps both canonical columns AND unmapped columns as additional features for ML
        """
        warnings = []
        
        # Rename canonical columns according to mapping
        rename_dict = {v: k for k, v in self.mapping.items()}
        df_mapped = df.rename(columns=rename_dict)
        
        # Keep canonical columns
        keep_cols = list(self.mapping.keys())
        df_mapped = df_mapped[keep_cols + self.unmapped_columns]
        
        # Log additional features found
        if self.unmapped_columns:
            warnings.append(
                f"Kept as additional features: {', '.join(self.unmapped_columns)}"
            )
        
        return df_mapped, warnings


# Singleton instance
mapper = ColumnMapper()
