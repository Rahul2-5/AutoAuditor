# Postman Quick Reference - Financial Auditor API

## 🚀 One-Minute Setup

### Import Collection
1. **Postman** → **File** → **Import**
2. Select **`Postman_Auditor_Collection.json`**
3. Click **Import**
4. Done! ✅

---

## 📋 Quick Links

| What | URL |
|------|-----|
| **API Endpoint** | `http://localhost:8000/api/analyze` |
| **Health Check** | `http://localhost:8000/` |
| **Method** | `POST` |
| **Content-Type** | `application/json` |

---

## ⚡ Fastest Testing Path

### Step 1: Import Collection
```
File → Import → Postman_Auditor_Collection.json
```

### Step 2: Select Test
Collections → Expensify Financial Auditor API → Select one:
- "Analyze Expenses (Full Report)" ← **START HERE**
- "Analyze - High Risk Scenario"
- "Analyze - Low Risk Scenario"

### Step 3: Send
Click **"Send"** button ➤

### Step 4: View Response
See JSON response below ⬇️

---

## 📤 Minimal Working Request

```json
{
  "summary_statistics": {
    "total_expense": 10000,
    "category_breakdown": {"Travel": 10000},
    "department_distribution": {"Sales": 10000},
    "employee_level_distribution": {"Manager": 10000},
    "spending_level_distribution": {"Medium": 10000}
  },
  "enriched_features": [{
    "date": "2024-01-01",
    "employee": "John",
    "amount": 1000,
    "category": "Travel",
    "vendor": "Airline",
    "description": "Flight",
    "spending_level": "Medium",
    "is_high_value": false,
    "risk_flag": false,
    "inferred_department": "Sales",
    "employee_level": "Manager",
    "behavioral_tags": []
  }],
  "policy_violations": [],
  "flagged_transactions": {
    "high_value_transactions": [],
    "potential_duplicates": [],
    "risk_transactions": []
  },
  "transactions": [{"date": "2024-01-01", "amount": 1000, "employee": "John"}]
}
```

---

## 📊 Response Preview

Every response includes:

```
✓ risk_assessment (overall risk + confidence)
✓ violation_analysis (critical/moderate/minor)
✓ anomalies (patterns detected)
✓ fraud_signals (suspicious activity)
✓ financial_insights (spending analysis)
✓ recommendations (actionable fixes)
✓ cost_optimization_tips (savings ideas)
✓ visualization (chart-ready data)
✓ final_audit_summary (executive summary)
```

---

## 🎯 Test Results Interpretation

| Response | Meaning |
|----------|---------|
| `"overall_risk": "high"` | ⚠️ Immediate action needed |
| `"overall_risk": "medium"` | ⏱️ Review and monitor |
| `"overall_risk": "low"` | ✅ Compliant and clean |
| `"confidence_score": 0.95` | 🔒 Highly reliable result |
| `"confidence_score": 0.50` | ⚡ Moderate confidence |
| `"critical": [...]` | 🚨 Severe violations found |
| `"fraud_signals": [...]` | 🔍 Investigate immediately |

---

## 🔧 Postman Environment Variables (Optional)

Create variables for reuse:

1. **Postman** → **Environments** → **New**
2. Add variables:
   ```
   base_url = http://localhost:8000
   api_endpoint = /api/analyze
   ```
3. Use in requests:
   - URL: `{{base_url}}{{api_endpoint}}`

---

## 💾 Save & Reuse Requests

### Save Current Request
1. Click **"Save"** or **Ctrl+S**
2. Name: "Test Case - [Scenario]"
3. Collection: "Expensify Financial Auditor API"
4. Click **"Save"**

### Reuse Saved Request
1. Go to Collections
2. Find saved request
3. Click to load
4. Modify if needed
5. Send

---

## 📋 Body Template

Always use this structure:

```json
{
  "summary_statistics": {...},
  "enriched_features": [...],
  "policy_violations": [...],
  "flagged_transactions": {
    "high_value_transactions": [...],
    "potential_duplicates": [...],
    "risk_transactions": [...]
  },
  "transactions": [...]
}
```

---

## ✅ Pre-Send Checklist

- [ ] Method is **POST**
- [ ] URL is **http://localhost:8000/api/analyze**
- [ ] Body is **raw** and **JSON**
- [ ] Content-Type header: **application/json**
- [ ] JSON is **valid** (no syntax errors)
- [ ] All required fields present
- [ ] Server running (check http://localhost:8000/)

---

## 🎓 Test Scenarios

### Scenario 1: Low Risk (5 sec)
```
Use: "Analyze - Low Risk Scenario"
Expect: overall_risk = "low"
Check: confidence_score > 0.5
```

### Scenario 2: High Risk (5 sec)
```
Use: "Analyze - High Risk Scenario"
Expect: overall_risk = "high"
Check: critical violations present
```

### Scenario 3: Full Analysis (10 sec)
```
Use: "Analyze Expenses (Full Report)"
Expect: Comprehensive report
Check: All 9 sections populated
```

---

## 🔍 Response Navigation

**In Postman Response Tab:**

| Click | To See |
|-------|--------|
| **Pretty** | Formatted JSON |
| **Raw** | Raw response |
| **Preview** | Rendered data |
| **Copy** | Copy entire response |
| **Save Response** | Save to file |

---

## 🆘 Common Issues & Quick Fixes

| Problem | Fix |
|---------|-----|
| 404 Error | Check URL: `http://localhost:8000/api/analyze` |
| 400 Error | Validate JSON syntax, check required fields |
| Connection refused | Start server: `python -m uvicorn main:app --reload` |
| Empty response | Ensure you're in Body tab, not Headers |
| Timeout | Server may be slow, wait 10 seconds, retry |

---

## 📞 Debug Mode

### Enable Request/Response Details
1. **Postman** → **Preferences** → **General**
2. Toggle "Show console on error"
3. Open **Console** (bottom left)
4. Send request
5. See detailed logs

---

## 🚀 Pro Tips

✓ **Duplicate request:** Right-click → Duplicate  
✓ **Compare responses:** Send to new tab side-by-side  
✓ **Format JSON:** Postman auto-formats  
✓ **History:** Ctrl+H to see all sent requests  
✓ **Collections:** Organize tests by feature  

---

## 📝 Response Checklist

For each response, verify:

- [ ] `risk_assessment` object exists
- [ ] `overall_risk` is "low", "medium", or "high"
- [ ] `confidence_score` is 0.0-1.0
- [ ] `violation_analysis` has 4 categories
- [ ] `recommendations` has at least 1 item
- [ ] `visualization` has all 5 chart types
- [ ] `final_audit_summary` is populated
- [ ] All values are JSON-serializable

---

## 🎯 Next Level

After testing basics:

1. **Create test cases** for your data
2. **Save responses** for comparison
3. **Set up monitors** for automated testing
4. **Use scripts** to validate responses
5. **Integrate with** frontend

---

## 📖 Documentation

| File | Purpose |
|------|---------|
| `POSTMAN_TESTING_GUIDE.md` | Detailed testing instructions |
| `AUDITOR_API_DOCS.md` | Complete API documentation |
| `AUDITOR_README.md` | Feature overview |
| `Postman_Auditor_Collection.json` | Importable collection |

---

## ✨ You're All Set!

1. ✅ Server running on `localhost:8000`
2. ✅ Collection ready in `Postman_Auditor_Collection.json`
3. ✅ Full documentation available
4. ✅ Sample test cases included

**Next: Open Postman and test! 🚀**

---

**Last Updated:** April 24, 2026  
**Status:** ✅ Complete and ready to test
