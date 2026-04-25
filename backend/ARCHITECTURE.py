"""
Architecture Design: Data Preparation Agent for AI Expense Auditor

LAYERS:

1. COLUMN MAPPER (column_mapper.py)
   - Dynamic field resolution using aliases
   - Fuzzy matching for unknown column names
   - Returns canonical schema: date, employee, amount, category, vendor, description
   
2. DATA CLEANER (data_cleaner.py)
   - Type validation and conversion
   - Null value handling
   - Duplicate removal
   - Business rule validation
   
3. FEATURE ENRICHER (data_enricher.py)
   - Spending classification (low/medium/high)
   - Risk flagging (keywords: luxury, casino, alcohol)
   - Department inference (IT, HR, Sales, Operations, Admin)
   - Employee level classification (Junior, Mid, Senior, Executive)
   - Behavioral tags (frequent_spender, high_risk, policy_violation_candidate)
   
4. ORCHESTRATOR (data_prep_agent.py)
   - Coordinates all layers
   - Generates summary statistics
   - Flags high-priority transactions
   - Returns structured JSON output

EXAMPLE INPUT CSV:
==================
date,employee,amount,category,vendor,description
2024-01-01,john_smith,150.50,travel,Uber,Ride to client
2024-01-02,sarah_jones,2500.00,travel,United Airlines,Flight to NYC

EXAMPLE OUTPUT:
===============
{
  "status": "success",
  "message": "Data prepared successfully",
  
  "summary": {
    "total_records": 20,
    "total_expense": 12500.00,
    "average_expense": 625.00,
    "median_expense": 450.00,
    "category_breakdown": {
      "travel": {"total": 6200, "count": 3, "percentage": 49.6%},
      "meals": {"total": 1500, "count": 5, "percentage": 12%},
      "office": {"total": 800, "count": 4, "percentage": 6.4%}
    },
    "department_breakdown": {
      "Operations": {"total": 6200, "count": 3},
      "HR": {"total": 1500, "count": 5},
      "IT": {"total": 2000, "count": 4}
    },
    "employee_level_distribution": {
      "Executive": {"count": 2, "total": 5500},
      "Senior": {"count": 5, "total": 4000},
      "Mid-level": {"count": 3, "total": 2000},
      "Junior": {"count": 10, "total": 1000}
    }
  },
  
  "flags": {
    "high_value_transactions": [
      {
        "employee": "sarah_jones",
        "amount": 2500.00,
        "category": "travel",
        "vendor": "United Airlines",
        "date": "2024-01-02",
        "level": "Executive",
        "risk": "low"
      }
    ],
    "risk_transactions": [
      {
        "employee": "john_smith",
        "amount": 150.00,
        "vendor": "Casino Royale",
        "description": "Team entertainment",
        "risk_level": "high",
        "keywords": "casino",
        "date": "2024-01-05"
      }
    ],
    "policy_violation_candidates": [
      {
        "employee": "emily_davis",
        "amount": 3500.00,
        "reason": "High-value + high risk",
        "vendor": "Luxury Hotel",
        "date": "2024-01-10",
        "tags": "high_risk_transaction; policy_violation_candidate"
      }
    ],
    "potential_duplicates": [
      {
        "employee": "mike_brown",
        "vendor": "Starbucks",
        "amount": 25.00,
        "date": "2024-01-15",
        "description": "Coffee"
      }
    ],
    "frequent_spenders": [
      {
        "employee": "john_smith",
        "total_expenses": 4500.00,
        "transaction_count": 8,
        "average_expense": 562.50,
        "primary_category": "travel"
      }
    ]
  },
  
  "data_preview": {
    "total_rows": 20,
    "columns": [
      "date", "employee", "amount", "category", "vendor", "description",
      "spending_level", "is_high_value", "risk_flag", "risk_keywords",
      "inferred_department", "employee_level", "behavioral_tags"
    ],
    "first_5_records": [
      {
        "date": "2024-01-01T00:00:00",
        "employee": "john_smith",
        "amount": 150.50,
        "category": "travel",
        "vendor": "uber",
        "description": "ride to client",
        "spending_level": "medium",
        "is_high_value": false,
        "risk_flag": "low",
        "risk_keywords": "",
        "inferred_department": "Operations",
        "employee_level": "Senior",
        "behavioral_tags": "clean"
      }
    ]
  },
  
  "execution_log": [
    {
      "timestamp": "2024-01-01T10:30:45.123456",
      "stage": "mapping",
      "status": "success",
      "details": "Mapped 6 columns"
    },
    {
      "timestamp": "2024-01-01T10:30:45.234567",
      "stage": "cleaning",
      "status": "success",
      "details": "Cleaned 0 invalid rows"
    },
    {
      "timestamp": "2024-01-01T10:30:45.345678",
      "stage": "enrichment",
      "status": "success",
      "details": "Added 6 features"
    }
  ]
}


ENRICHED COLUMNS ADDED:
=======================
- spending_level: 'low' | 'medium' | 'high' (dynamic thresholds)
- is_high_value: boolean (top 10% by amount)
- risk_flag: 'low' | 'medium' | 'high' (keyword-based)
- risk_keywords: string (comma-separated keywords found)
- inferred_department: 'IT' | 'HR' | 'Sales & Marketing' | 'Operations' | 'Administration' | 'unknown'
- employee_level: 'Junior' | 'Mid-level' | 'Senior' | 'Executive'
- behavioral_tags: semicolon-separated tags
  - frequent_spender
  - high_risk_transaction
  - policy_violation_candidate
  - potential_duplicate
  - clean

API ENDPOINTS:
==============
POST /api/prepare
  - Input: CSV file (arbitrary schema)
  - Output: JSON with prepared data + summaries + flags
  
POST /api/export-prepared-data
  - Input: CSV file
  - Output: CSV file (enriched data ready for ML)

EDGE CASES HANDLED:
===================
✓ Unknown column names (dynamic fuzzy matching)
✓ Missing required fields (validation)
✓ Null values (intelligent handling)
✓ Duplicate rows (detection and removal)
✓ Type mismatches (automatic conversion with error tracking)
✓ Extreme outliers (flagged but not removed)
✓ Empty datasets (error handling)
✓ Malformed CSV (error message)

PRODUCTION READY FEATURES:
==========================
✓ Modular architecture (each layer independent)
✓ Error tracking (execution_log)
✓ Comprehensive reporting (summary + flags)
✓ Scalable (handles 1K-100K+ rows)
✓ Debuggable (detailed execution log)
✓ Business-aware (department, level inference)
✓ Compliance-ready (policy violation flags)
✓ ML-ready (structured output, labels)
"""

# API RESPONSE STRUCTURE CONSTANTS
REQUIRED_CANONICAL_FIELDS = {
    'date': 'Transaction date',
    'employee': 'Employee name or ID',
    'amount': 'Expense amount (numeric)',
    'category': 'Expense category',
    'vendor': 'Vendor/merchant name',
    'description': 'Transaction description'
}

ENRICHED_FIELDS = {
    'spending_level': 'low | medium | high',
    'is_high_value': 'boolean (top 10%)',
    'risk_flag': 'low | medium | high',
    'risk_keywords': 'detected keywords',
    'inferred_department': 'inferred dept',
    'employee_level': 'Junior | Mid | Senior | Executive',
    'behavioral_tags': 'comma-separated tags'
}

# DEPARTMENT CLASSIFICATION RULES
DEPARTMENT_KEYWORDS = {
    'IT': ['software', 'hardware', 'technology', 'cloud', 'aws', 'azure', 'license'],
    'HR': ['meals', 'employee', 'training', 'course', 'learning', 'development'],
    'Sales & Marketing': ['marketing', 'ads', 'conference', 'event', 'campaign'],
    'Operations': ['travel', 'transportation', 'logistics', 'vehicle', 'airline'],
    'Administration': ['office', 'admin', 'supplies', 'furniture', 'utilities']
}

# RISK DETECTION KEYWORDS
HIGH_RISK_KEYWORDS = [
    'casino', 'alcohol', 'bar', 'nightclub', 'luxury', 'vip',
    'spa', 'personal', 'entertainment'
]

# SPENDING CLASSIFICATION THRESHOLDS (dynamic percentile-based)
SPENDING_PERCENTILES = {
    'low': 0.33,      # Bottom 33%
    'medium': 0.67,   # Middle 34%
    'high': 1.0       # Top 33%
}

# EMPLOYEE LEVEL HEURISTICS
EXECUTIVE_INDICATORS = [
    'first class', 'private', 'executive', 'suite', 'luxury',
    'premium', 'business class', 'corporate'
]

# Singleton exports
if __name__ == "__main__":
    print(__doc__)
