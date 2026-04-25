# Financial Auditor API Documentation

## Overview
The Financial Auditor is an advanced AI-powered enterprise expense auditing system that provides:
- Risk assessment and scoring
- Policy violation analysis
- Anomaly detection
- Fraud signal identification
- Financial insights
- Actionable recommendations
- Cost optimization suggestions
- Visualization data for frontend display

## API Endpoint

### POST `/api/analyze`

Analyzes expense data and returns comprehensive audit report in JSON format.

## Request Format

```json
{
  "summary_statistics": {
    "total_expense": 250000.00,
    "category_breakdown": {
      "Travel": 85000,
      "Meals & Entertainment": 45000,
      "Software": 65000,
      "Office Supplies": 28000,
      "Miscellaneous": 27000
    },
    "department_distribution": {
      "Sales": 95000,
      "Engineering": 85000,
      "Marketing": 45000,
      "Operations": 25000
    },
    "employee_level_distribution": {
      "Manager": 120000,
      "Senior": 85000,
      "Junior": 45000
    },
    "spending_level_distribution": {
      "Low": 120000,
      "Medium": 80000,
      "High": 50000
    }
  },
  "enriched_features": [
    {
      "date": "2024-01-05",
      "employee": "John Smith",
      "amount": 1200.00,
      "category": "Travel",
      "vendor": "United Airlines",
      "description": "Flight to NYC",
      "spending_level": "Medium",
      "is_high_value": false,
      "risk_flag": false,
      "inferred_department": "Sales",
      "employee_level": "Manager",
      "behavioral_tags": ["frequent_traveler"]
    }
    // ... more transactions
  ],
  "policy_violations": [
    {
      "employee": "Jane Doe",
      "amount": 3500.00,
      "category": "Travel",
      "date": "2024-01-06",
      "violation_type": "budget_exceeded",
      "description": "Hotel expense exceeds approved per-diem by 40%"
    }
    // ... more violations
  ],
  "flagged_transactions": {
    "high_value_transactions": [
      {
        "date": "2024-01-06",
        "employee": "Jane Doe",
        "amount": 3500.00,
        "category": "Travel",
        "reason": "Exceeds high-value threshold"
      }
    ],
    "potential_duplicates": [
      {
        "transaction_pair": ["...", "..."],
        "similarity_score": 0.85,
        "reason": "..."
      }
    ],
    "risk_transactions": [
      {
        "date": "2024-01-06",
        "employee": "Jane Doe",
        "amount": 3500.00,
        "risk_score": 0.82,
        "reason": "High-value + violation combination"
      }
    ]
  },
  "transactions": [
    {
      "date": "2024-01-05",
      "amount": 1200.00,
      "employee": "John Smith"
    }
    // ... more transactions
  ]
}
```

## Response Format

```json
{
  "risk_assessment": {
    "overall_risk": "high",
    "confidence_score": 1.0,
    "key_risks": [
      "High violation frequency: 40.0% of transactions",
      "High concentration of high-value transactions: 46.7%"
    ]
  },
  "violation_analysis": {
    "total_violations": 6,
    "critical": [
      {
        "employee": "Jane Doe",
        "amount": 3500.0,
        "category": "Travel",
        "date": "2024-01-06",
        "violation_type": "budget_exceeded",
        "description": "Hotel expense exceeds approved per-diem by 40%"
      }
    ],
    "moderate": [...],
    "minor": [...],
    "repeat_offenders": [
      {
        "employee": "Jane Doe",
        "violation_count": 3,
        "total_amount": 10000.0,
        "violations": [...]
      }
    ]
  },
  "anomalies": [
    {
      "type": "category_dominance",
      "category": "Travel",
      "concentration": 0.68,
      "amount": 20600.0,
      "description": "Category 'Travel' represents 67.9% of total spending"
    }
  ],
  "fraud_signals": [
    {
      "type": "high_value_violation",
      "severity": "critical",
      "count": 5,
      "description": "5 high-value transactions with policy violations detected"
    }
  ],
  "financial_insights": [
    {
      "type": "spending_distribution",
      "description": "Top spending categories: Travel ($85,000.00)",
      "details": [...]
    }
  ],
  "recommendations": [
    {
      "title": "Resolve Critical Policy Violations",
      "description": "Found 2 critical violations. Immediately review and take corrective action with involved employees.",
      "priority": "high"
    }
  ],
  "cost_optimization_tips": [
    {
      "tip": "Negotiate volume discounts with top vendors",
      "impact": "high",
      "description": "Given high spending levels, negotiate better rates with frequent vendors"
    }
  ],
  "visualization": {
    "category_distribution": [
      {"name": "Travel", "value": 85000},
      {"name": "Software", "value": 65000}
    ],
    "department_distribution": [
      {"name": "Sales", "value": 95000},
      {"name": "Engineering", "value": 85000}
    ],
    "spending_trend": [
      {"date": "2024-01-05", "amount": 1200.0},
      {"date": "2024-01-06", "amount": 3500.0}
    ],
    "top_spenders": [
      {"employee": "Mike Johnson", "amount": 8750.0},
      {"employee": "Jane Doe", "amount": 7750.0}
    ],
    "violation_breakdown": [
      {"type": "critical", "count": 2},
      {"type": "moderate", "count": 2},
      {"type": "minor", "count": 2}
    ]
  },
  "final_audit_summary": "AUDIT REPORT SUMMARY: Overall Risk Assessment is HIGH (Confidence: 100%). Identified 6 total policy violations, including 2 critical cases..."
}
```

## Using the Auditor

### Example Python Usage

```python
from services.auditor import auditor

audit_data = {
    "summary_statistics": {...},
    "enriched_features": [...],
    "policy_violations": [...],
    "flagged_transactions": {...},
    "transactions": [...]
}

# Run audit analysis
report = auditor.analyze(audit_data)

# Access specific components
risk = report['risk_assessment']
violations = report['violation_analysis']
fraud = report['fraud_signals']
viz_data = report['visualization']
```

### Example API Call (cURL)

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d @audit_data.json
```

### Example API Call (Python Requests)

```python
import requests
import json

with open('audit_data.json', 'r') as f:
    audit_data = json.load(f)

response = requests.post(
    'http://localhost:8000/api/analyze',
    json=audit_data
)

report = response.json()
print(json.dumps(report, indent=2))
```

## Output Components

### 1. Risk Assessment
- **overall_risk**: Low, Medium, or High
- **confidence_score**: 0.0 - 1.0
- **key_risks**: List of identified risk factors

### 2. Violation Analysis
- **total_violations**: Count of all violations
- **critical**: Severe policy breaches
- **moderate**: Medium-severity violations
- **minor**: Low-severity violations
- **repeat_offenders**: Employees with 3+ violations

### 3. Anomalies
Detects:
- Category dominance (>40%)
- Unusual spending spikes (statistical outliers)
- Abnormal employee behavior patterns

### 4. Fraud Signals
Identifies:
- High-value + violation combinations
- Potential duplicate transactions
- Repeated risky vendors
- Inconsistent behavior patterns

### 5. Financial Insights
- Spending distribution by category
- Department efficiency metrics
- Violation cost impact
- Employee level analysis
- High-value transaction review

### 6. Recommendations
Actionable items with:
- Title
- Description
- Priority (high, medium, low)

### 7. Cost Optimization Tips
Smart suggestions with:
- Tip description
- Impact level (high, medium, low)
- Implementation guidance

### 8. Visualization Data
Ready for frontend charts:
- Category distribution (pie chart)
- Department distribution (bar chart)
- Spending trend (line chart)
- Top spenders (bar chart)
- Violation breakdown (pie chart)

## Key Features

✓ **Dynamic Risk Scoring** - Multi-factor risk assessment (violation frequency, high-value density, risk flags, duplicates, spending concentration)

✓ **Intelligent Violation Categorization** - Automatic severity classification based on violation type

✓ **Repeat Offender Detection** - Identifies employees with 3+ violations

✓ **Statistical Anomaly Detection** - Uses standard deviation analysis for spending spikes

✓ **Fraud Pattern Recognition** - Correlates violations with high-value transactions and vendor patterns

✓ **Actionable Insights** - Generates business-focused recommendations based on analysis

✓ **Cost Optimization** - Smart cost-cutting strategies based on spending levels and violation patterns

✓ **Frontend-Ready Visualization** - Pre-formatted data for immediate chart rendering

## Testing

Run the test script:

```bash
python test_auditor.py
```

This generates a comprehensive report with sample data and saves it to `audit_report_output.json`.

## Integration Steps

1. The auditor service is already integrated in the FastAPI application
2. Use the `/api/analyze` endpoint to submit audit data
3. Receive pure JSON response suitable for frontend display
4. Use the visualization data for dashboard charts
5. Display recommendations and insights in the UI

## Notes

- All output is **pure JSON**, suitable for immediate frontend consumption
- No raw data repetition - focuses on insights and analysis
- Confidence scores indicate reliability of assessments
- Recommendations are prioritized by severity
- All financial amounts are properly rounded to 2 decimal places
