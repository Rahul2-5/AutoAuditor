"""
Test script for the Financial Auditor
Demonstrates complete audit workflow with sample data
"""

import json
from services.auditor import auditor


# Sample audit data - realistic enterprise scenario
sample_audit_data = {
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
            "is_high_value": False,
            "risk_flag": False,
            "inferred_department": "Sales",
            "employee_level": "Manager",
            "behavioral_tags": ["frequent_traveler"]
        },
        {
            "date": "2024-01-06",
            "employee": "Jane Doe",
            "amount": 3500.00,
            "category": "Travel",
            "vendor": "Marriott Hotels",
            "description": "Hotel stay - 5 nights",
            "spending_level": "High",
            "is_high_value": True,
            "risk_flag": True,
            "inferred_department": "Engineering",
            "employee_level": "Senior",
            "behavioral_tags": ["rare_high_spend"]
        },
        {
            "date": "2024-01-07",
            "employee": "John Smith",
            "amount": 450.00,
            "category": "Meals & Entertainment",
            "vendor": "Restaurant X",
            "description": "Client dinner",
            "spending_level": "Medium",
            "is_high_value": False,
            "risk_flag": False,
            "inferred_department": "Sales",
            "employee_level": "Manager",
            "behavioral_tags": ["business_meal"]
        },
        {
            "date": "2024-01-08",
            "employee": "Mike Johnson",
            "amount": 5000.00,
            "category": "Software",
            "vendor": "Adobe Inc",
            "description": "Software license renewal",
            "spending_level": "High",
            "is_high_value": True,
            "risk_flag": False,
            "inferred_department": "Marketing",
            "employee_level": "Manager",
            "behavioral_tags": ["legitimate_purchase"]
        },
        {
            "date": "2024-01-09",
            "employee": "Sarah Wilson",
            "amount": 2200.00,
            "category": "Travel",
            "vendor": "United Airlines",
            "description": "Flight to LA",
            "spending_level": "High",
            "is_high_value": True,
            "risk_flag": True,
            "inferred_department": "Sales",
            "employee_level": "Senior",
            "behavioral_tags": ["high_travel_frequency"]
        },
        {
            "date": "2024-01-10",
            "employee": "Tom Brown",
            "amount": 800.00,
            "category": "Meals & Entertainment",
            "vendor": "Restaurant Y",
            "description": "Team lunch",
            "spending_level": "Low",
            "is_high_value": False,
            "risk_flag": False,
            "inferred_department": "Operations",
            "employee_level": "Junior",
            "behavioral_tags": ["team_event"]
        },
        {
            "date": "2024-01-11",
            "employee": "John Smith",
            "amount": 3200.00,
            "category": "Travel",
            "vendor": "Marriott Hotels",
            "description": "Hotel stay - 4 nights",
            "spending_level": "High",
            "is_high_value": True,
            "risk_flag": False,
            "inferred_department": "Sales",
            "employee_level": "Manager",
            "behavioral_tags": ["business_travel"]
        },
        {
            "date": "2024-01-12",
            "employee": "Jane Doe",
            "amount": 450.00,
            "category": "Office Supplies",
            "vendor": "Office Depot",
            "description": "Office supplies",
            "spending_level": "Low",
            "is_high_value": False,
            "risk_flag": False,
            "inferred_department": "Engineering",
            "employee_level": "Senior",
            "behavioral_tags": []
        },
        {
            "date": "2024-01-13",
            "employee": "Mike Johnson",
            "amount": 2800.00,
            "category": "Travel",
            "vendor": "Hilton Hotels",
            "description": "Hotel stay - 3 nights",
            "spending_level": "High",
            "is_high_value": True,
            "risk_flag": True,
            "inferred_department": "Marketing",
            "employee_level": "Manager",
            "behavioral_tags": ["conference_travel"]
        },
        {
            "date": "2024-01-14",
            "employee": "Sarah Wilson",
            "amount": 1500.00,
            "category": "Meals & Entertainment",
            "vendor": "Restaurant Z",
            "description": "Client entertainment",
            "spending_level": "Medium",
            "is_high_value": False,
            "risk_flag": False,
            "inferred_department": "Sales",
            "employee_level": "Senior",
            "behavioral_tags": ["client_event"]
        },
        {
            "date": "2024-01-15",
            "employee": "Tom Brown",
            "amount": 1800.00,
            "category": "Travel",
            "vendor": "Budget Hotels",
            "description": "Hotel stay - 2 nights",
            "spending_level": "Medium",
            "is_high_value": False,
            "risk_flag": False,
            "inferred_department": "Operations",
            "employee_level": "Junior",
            "behavioral_tags": []
        },
        {
            "date": "2024-01-16",
            "employee": "John Smith",
            "amount": 600.00,
            "category": "Meals & Entertainment",
            "vendor": "Restaurant X",
            "description": "Client dinner",
            "spending_level": "Medium",
            "is_high_value": False,
            "risk_flag": False,
            "inferred_department": "Sales",
            "employee_level": "Manager",
            "behavioral_tags": ["business_meal"]
        },
        {
            "date": "2024-01-17",
            "employee": "Jane Doe",
            "amount": 3800.00,
            "category": "Travel",
            "vendor": "United Airlines",
            "description": "Flight + Hotel package",
            "spending_level": "High",
            "is_high_value": True,
            "risk_flag": True,
            "inferred_department": "Engineering",
            "employee_level": "Senior",
            "behavioral_tags": ["high_spend_pattern"]
        },
        {
            "date": "2024-01-18",
            "employee": "Mike Johnson",
            "amount": 950.00,
            "category": "Software",
            "vendor": "Salesforce",
            "description": "Monthly subscription",
            "spending_level": "Medium",
            "is_high_value": False,
            "risk_flag": False,
            "inferred_department": "Marketing",
            "employee_level": "Manager",
            "behavioral_tags": []
        },
        {
            "date": "2024-01-19",
            "employee": "Sarah Wilson",
            "amount": 2100.00,
            "category": "Travel",
            "vendor": "United Airlines",
            "description": "Flight to Chicago",
            "spending_level": "High",
            "is_high_value": True,
            "risk_flag": True,
            "inferred_department": "Sales",
            "employee_level": "Senior",
            "behavioral_tags": ["frequent_flyer"]
        }
    ],
    "policy_violations": [
        {
            "employee": "Jane Doe",
            "amount": 3500.00,
            "category": "Travel",
            "date": "2024-01-06",
            "violation_type": "budget_exceeded",
            "description": "Hotel expense exceeds approved per-diem by 40%"
        },
        {
            "employee": "Mike Johnson",
            "amount": 2800.00,
            "category": "Travel",
            "date": "2024-01-13",
            "violation_type": "high_value_alert",
            "description": "High-value transaction requires additional approval"
        },
        {
            "employee": "Sarah Wilson",
            "amount": 2200.00,
            "category": "Travel",
            "date": "2024-01-09",
            "violation_type": "frequency_violation",
            "description": "Excessive travel frequency - 5 trips in 30 days"
        },
        {
            "employee": "John Smith",
            "amount": 1200.00,
            "category": "Travel",
            "date": "2024-01-05",
            "violation_type": "missing_documentation",
            "description": "Missing business purpose documentation"
        },
        {
            "employee": "Jane Doe",
            "amount": 3800.00,
            "category": "Travel",
            "date": "2024-01-17",
            "violation_type": "budget_exceeded",
            "description": "Travel package exceeds quarterly limit"
        },
        {
            "employee": "Sarah Wilson",
            "amount": 2100.00,
            "category": "Travel",
            "date": "2024-01-19",
            "violation_type": "frequency_violation",
            "description": "Excessive travel frequency - 6 trips in 30 days"
        }
    ],
    "flagged_transactions": {
        "high_value_transactions": [
            {
                "date": "2024-01-06",
                "employee": "Jane Doe",
                "amount": 3500.00,
                "category": "Travel",
                "reason": "Exceeds high-value threshold"
            },
            {
                "date": "2024-01-08",
                "employee": "Mike Johnson",
                "amount": 5000.00,
                "category": "Software",
                "reason": "High-value legitimate purchase"
            },
            {
                "date": "2024-01-09",
                "employee": "Sarah Wilson",
                "amount": 2200.00,
                "category": "Travel",
                "reason": "High-value transaction"
            },
            {
                "date": "2024-01-13",
                "employee": "Mike Johnson",
                "amount": 2800.00,
                "category": "Travel",
                "reason": "High-value transaction"
            },
            {
                "date": "2024-01-17",
                "employee": "Jane Doe",
                "amount": 3800.00,
                "category": "Travel",
                "reason": "High-value transaction"
            },
            {
                "date": "2024-01-19",
                "employee": "Sarah Wilson",
                "amount": 2100.00,
                "category": "Travel",
                "reason": "High-value transaction"
            }
        ],
        "potential_duplicates": [
            {
                "transaction_pair": ["Jane Doe - Hotel 01/06 - $3500", "Jane Doe - Travel 01/17 - $3800"],
                "similarity_score": 0.85,
                "reason": "Same employee, similar dates, similar amounts, similar vendors"
            }
        ],
        "risk_transactions": [
            {
                "date": "2024-01-06",
                "employee": "Jane Doe",
                "amount": 3500.00,
                "risk_score": 0.82,
                "reason": "High-value + violation combination"
            },
            {
                "date": "2024-01-09",
                "employee": "Sarah Wilson",
                "amount": 2200.00,
                "risk_score": 0.78,
                "reason": "Frequent traveler with high spending"
            },
            {
                "date": "2024-01-17",
                "employee": "Jane Doe",
                "amount": 3800.00,
                "risk_score": 0.75,
                "reason": "Repeat high-value violator"
            }
        ]
    },
    "transactions": [
        {"date": "2024-01-05", "amount": 1200.00, "employee": "John Smith"},
        {"date": "2024-01-06", "amount": 3500.00, "employee": "Jane Doe"},
        {"date": "2024-01-07", "amount": 450.00, "employee": "John Smith"},
        {"date": "2024-01-08", "amount": 5000.00, "employee": "Mike Johnson"},
        {"date": "2024-01-09", "amount": 2200.00, "employee": "Sarah Wilson"},
        {"date": "2024-01-10", "amount": 800.00, "employee": "Tom Brown"},
        {"date": "2024-01-11", "amount": 3200.00, "employee": "John Smith"},
        {"date": "2024-01-12", "amount": 450.00, "employee": "Jane Doe"},
        {"date": "2024-01-13", "amount": 2800.00, "employee": "Mike Johnson"},
        {"date": "2024-01-14", "amount": 1500.00, "employee": "Sarah Wilson"},
        {"date": "2024-01-15", "amount": 1800.00, "employee": "Tom Brown"},
        {"date": "2024-01-16", "amount": 600.00, "employee": "John Smith"},
        {"date": "2024-01-17", "amount": 3800.00, "employee": "Jane Doe"},
        {"date": "2024-01-18", "amount": 950.00, "employee": "Mike Johnson"},
        {"date": "2024-01-19", "amount": 2100.00, "employee": "Sarah Wilson"}
    ]
}


def test_auditor():
    """Test the auditor with sample data and display results"""
    print("\n" + "="*80)
    print("FINANCIAL AUDITOR - TEST EXECUTION")
    print("="*80 + "\n")
    
    # Run audit analysis
    print("Running comprehensive audit analysis...\n")
    audit_report = auditor.analyze(sample_audit_data)
    
    # Display results
    print("AUDIT REPORT (JSON FORMAT):")
    print("-" * 80)
    print(json.dumps(audit_report, indent=2))
    print("-" * 80)
    
    # Save to file
    output_file = "audit_report_output.json"
    with open(output_file, 'w') as f:
        json.dump(audit_report, f, indent=2)
    
    print(f"\n✓ Audit report saved to: {output_file}")
    print("\n" + "="*80)
    print("AUDIT ANALYSIS COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    test_auditor()
