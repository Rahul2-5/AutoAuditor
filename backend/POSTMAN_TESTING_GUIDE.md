# Postman Testing Guide - Financial Auditor API

## ✅ Server Status

**Server is running on:** `http://localhost:8000`

## 📋 Quick Start (3 Steps)

### Step 1: Import Collection into Postman

1. Open **Postman**
2. Click **"File" → "Import"** (or use Ctrl+O)
3. Select **"Postman_Auditor_Collection.json"** from the backend folder
4. Click **"Import"**

The collection will appear with all test requests ready to use!

---

## 🧪 Testing the API Manually

### Method 1: Using the Imported Collection (Easiest)

1. **Open Postman**
2. **Go to Collections** (left sidebar)
3. **Find "Expensify Financial Auditor API"**
4. **Expand** and click any request:
   - "Analyze Expenses (Full Report)" 
   - "Analyze - High Risk Scenario"
   - "Analyze - Low Risk Scenario"
5. Click **"Send"**
6. View response in the **"Response"** tab below

✅ **That's it!** The JSON request body is already configured.

---

### Method 2: Manual Request Setup (If not using collection)

#### Request Details

- **Method:** POST
- **URL:** `http://localhost:8000/api/analyze`
- **Headers:**
  ```
  Content-Type: application/json
  ```

#### Steps

1. **Open Postman** 
2. **Create New Request**
3. **Change method to POST**
4. **Enter URL:** `http://localhost:8000/api/analyze`
5. **Go to Headers tab**, add:
   - Key: `Content-Type`
   - Value: `application/json`
6. **Go to Body tab**
7. **Select "raw"** and **"JSON"** from dropdown
8. **Paste the request JSON** (see below)
9. **Click "Send"**
10. **View response** in Response tab

---

## 📤 Request Body Examples

### Test Case 1: Full Realistic Scenario (RECOMMENDED)

Copy this entire JSON into Postman Body (raw, JSON format):

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
    },
    {
      "date": "2024-01-06",
      "employee": "Jane Doe",
      "amount": 3500.00,
      "category": "Travel",
      "vendor": "Marriott Hotels",
      "description": "Hotel stay - 5 nights",
      "spending_level": "High",
      "is_high_value": true,
      "risk_flag": true,
      "inferred_department": "Engineering",
      "employee_level": "Senior",
      "behavioral_tags": ["rare_high_spend"]
    },
    {
      "date": "2024-01-09",
      "employee": "Sarah Wilson",
      "amount": 2200.00,
      "category": "Travel",
      "vendor": "United Airlines",
      "description": "Flight to LA",
      "spending_level": "High",
      "is_high_value": true,
      "risk_flag": true,
      "inferred_department": "Sales",
      "employee_level": "Senior",
      "behavioral_tags": ["high_travel_frequency"]
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
      "employee": "Sarah Wilson",
      "amount": 2200.00,
      "category": "Travel",
      "date": "2024-01-09",
      "violation_type": "frequency_violation",
      "description": "Excessive travel frequency"
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
        "date": "2024-01-09",
        "employee": "Sarah Wilson",
        "amount": 2200.00,
        "category": "Travel",
        "reason": "High-value transaction"
      }
    ],
    "potential_duplicates": [],
    "risk_transactions": [
      {
        "date": "2024-01-06",
        "employee": "Jane Doe",
        "amount": 3500.00,
        "risk_score": 0.82,
        "reason": "High-value + violation"
      }
    ]
  },
  "transactions": [
    {"date": "2024-01-05", "amount": 1200.00, "employee": "John Smith"},
    {"date": "2024-01-06", "amount": 3500.00, "employee": "Jane Doe"},
    {"date": "2024-01-09", "amount": 2200.00, "employee": "Sarah Wilson"}
  ]
}
```

---

### Test Case 2: Minimal Request (Simplest Test)

```json
{
  "summary_statistics": {
    "total_expense": 10000.00,
    "category_breakdown": {"Travel": 6000, "Food": 4000},
    "department_distribution": {"Sales": 10000},
    "employee_level_distribution": {"Manager": 10000},
    "spending_level_distribution": {"Medium": 10000}
  },
  "enriched_features": [
    {
      "date": "2024-01-01",
      "employee": "John",
      "amount": 500.00,
      "category": "Travel",
      "vendor": "Airline",
      "description": "Flight",
      "spending_level": "Medium",
      "is_high_value": false,
      "risk_flag": false,
      "inferred_department": "Sales",
      "employee_level": "Manager",
      "behavioral_tags": []
    }
  ],
  "policy_violations": [],
  "flagged_transactions": {
    "high_value_transactions": [],
    "potential_duplicates": [],
    "risk_transactions": []
  },
  "transactions": [
    {"date": "2024-01-01", "amount": 500.00, "employee": "John"}
  ]
}
```

---

## 📥 Expected Response Format

The API returns a comprehensive JSON audit report:

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
    "critical": [...],
    "moderate": [...],
    "minor": [...],
    "repeat_offenders": [...]
  },
  "anomalies": [...],
  "fraud_signals": [...],
  "financial_insights": [...],
  "recommendations": [
    {
      "title": "Resolve Critical Policy Violations",
      "description": "...",
      "priority": "high"
    }
  ],
  "cost_optimization_tips": [...],
  "visualization": {
    "category_distribution": [...],
    "department_distribution": [...],
    "spending_trend": [...],
    "top_spenders": [...],
    "violation_breakdown": [...]
  },
  "final_audit_summary": "..."
}
```

---

## 🎯 What to Look For in Response

### Risk Assessment
- ✓ `overall_risk`: Should be "low", "medium", or "high"
- ✓ `confidence_score`: Between 0.0 and 1.0
- ✓ `key_risks`: List of identified risk factors

### Violations
- ✓ `critical`: Severe violations (must address immediately)
- ✓ `moderate`: Medium severity
- ✓ `minor`: Low severity
- ✓ `repeat_offenders`: Employees with multiple violations

### Insights
- ✓ Spending patterns by category and department
- ✓ High-value transaction analysis
- ✓ Violation cost impact

### Recommendations
- ✓ Prioritized by severity (high → medium → low)
- ✓ Actionable descriptions
- ✓ Based on actual findings

---

## 🧪 Test Scenarios

### Scenario A: Full Complex Dataset
**What to expect:**
- ✓ HIGH risk (many violations and high-value transactions)
- ✓ Multiple critical violations
- ✓ Fraud signals detected
- ✓ Cost optimization tips

**Use:** Postman collection → "Analyze Expenses (Full Report)"

---

### Scenario B: High-Risk Focused
**What to expect:**
- ✓ HIGH risk with 100% confidence
- ✓ Multiple violations from same employee
- ✓ Potential duplicates detected
- ✓ Repeated risky vendors

**Use:** Postman collection → "Analyze - High Risk Scenario"

---

### Scenario C: Clean, Compliant
**What to expect:**
- ✓ LOW risk (no violations)
- ✓ Clean spending patterns
- ✓ No fraud signals
- ✓ Efficiency recommendations

**Use:** Postman collection → "Analyze - Low Risk Scenario"

---

## 🔄 Testing Workflow

### Full Testing Sequence

1. **Test Health Check**
   ```
   GET http://localhost:8000/
   Expected: {"message": "AI Expense Auditor API is running"}
   ```

2. **Test High-Risk Scenario**
   - Request: Full complex dataset
   - Verify: HIGH risk detected
   - Check: Violations properly categorized

3. **Test Low-Risk Scenario**
   - Request: Clean data
   - Verify: LOW risk
   - Check: No false positives

4. **Test Visualization Data**
   - Expand "visualization" in response
   - Verify: category_distribution has data
   - Verify: department_distribution has data
   - Verify: spending_trend has time-series data
   - Verify: top_spenders has employee rankings
   - Verify: violation_breakdown has counts

5. **Test Recommendations**
   - Check: At least 1 recommendation for high-risk
   - Check: Each has title, description, priority
   - Check: Priority is "high", "medium", or "low"

---

## 💡 Tips & Tricks

### Save Requests for Reuse
1. After sending a request, click **"Save as..."**
2. Name it (e.g., "Test - Full Analysis")
3. Next time, just modify and re-send

### Pretty Print Response
1. Response appears as raw JSON
2. Click **"Pretty"** button (or auto-formats)
3. Makes it easier to read

### Copy Response
1. Click **"Copy"** icon on response tab
2. Paste into text editor or another tool
3. Great for documentation

### Send to New Tab
1. Right-click on request
2. Select **"Send request and open new tab"**
3. Compares multiple responses side-by-side

### Save Response as File
1. Click **"Save Response"** button
2. Choose filename
3. Saves JSON to disk for analysis

---

## 🐛 Troubleshooting

### Issue: Connection Refused
**Solution:**
- Verify server is running: `http://localhost:8000/`
- Terminal should show "Application startup complete"
- If not, restart server: `python -m uvicorn main:app --reload`

### Issue: 400 Bad Request
**Solution:**
- Check JSON syntax (use formatter if unsure)
- Verify all required fields are present
- Check Content-Type header is "application/json"

### Issue: Response is Empty
**Solution:**
- Check "Body" tab, not "Headers" tab
- Ensure request has raw JSON
- Click "Send" again

### Issue: "No Mock Server"
**Solution:**
- Make sure server is running
- Use actual URL, not mock server
- Check port is 8000

---

## 📊 Response Analysis

### Look for These Key Indicators

**High Risk 🚨**
- `confidence_score` > 0.7
- Multiple `critical` violations
- `fraud_signals` detected
- `repeat_offenders` > 0

**Medium Risk ⚠️**
- `confidence_score` 0.4 - 0.7
- Some moderate violations
- Few fraud signals
- Limited repeat offenders

**Low Risk ✅**
- `confidence_score` < 0.4
- Minimal violations
- No fraud signals
- No repeat offenders

---

## 🎓 Learning Resources

- Check `AUDITOR_API_DOCS.md` for detailed API reference
- Review `AUDITOR_README.md` for complete feature overview
- See `test_auditor.py` for Python integration examples

---

## 🚀 Next Steps

After testing:
1. ✅ Verify all response fields are present
2. ✅ Test with your own data
3. ✅ Integrate responses into frontend
4. ✅ Set up alerts for high-risk findings
5. ✅ Schedule regular audit runs

---

**Happy Testing! 🎉**
