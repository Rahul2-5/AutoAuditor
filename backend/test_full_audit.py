"""
Test script for complete automated audit workflow
Tests the /api/full-audit endpoint
"""

import json
import pandas as pd
from services.full_audit_pipeline import pipeline, NumpyEncoder


def test_full_audit_workflow():
    """Test complete audit workflow with CSV file"""
    
    print("\n" + "="*80)
    print("FULL AUDIT WORKFLOW TEST")
    print("="*80 + "\n")
    
    # Load sample CSV
    csv_path = "data/samples/test_expenses.csv"
    print(f"[1/3] Loading CSV file: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} expense records\n")
    
    # Process through pipeline
    print(f"[2/3] Processing through audit pipeline...")
    result = pipeline.process_file(df)
    
    if result['status'] != 'success':
        print("Audit Pipeline Failed!")
        return
    
    print("Audit Pipeline Success!")
    
    # Display results
    print(f"[3/3] Generating report...\n")
    
    report = result['report']
    
    # Processing info
    proc = report['processing']
    print(f"PROCESSING SUMMARY:")
    print(f"  Timestamp: {proc['timestamp']}")
    print(f"  Total Records: {proc['total_records']}")
    print(f"  Data Preparation: {proc['preparation']['status']}")
    print()
    
    # Audit results
    audit = report['audit_analysis']
    risk = audit['risk_assessment']
    print(f"RISK ASSESSMENT:")
    print(f"  Overall Risk: {risk['overall_risk'].upper()}")
    print(f"  Confidence Score: {risk['confidence_score']:.0%}")
    print(f"  Key Risks: {len(risk['key_risks'])} identified")
    print()
    
    # Violations
    violations = audit['violation_analysis']
    print(f"VIOLATION ANALYSIS:")
    print(f"  Total Violations: {violations['total_violations']}")
    print(f"  Critical: {len(violations['critical'])}")
    print(f"  Moderate: {len(violations['moderate'])}")
    print(f"  Minor: {len(violations['minor'])}")
    print()
    
    # Anomalies
    anomalies = audit['anomalies']
    print(f"ANOMALIES DETECTED: {len(anomalies)}")
    for i, anom in enumerate(anomalies[:3], 1):
        print(f"  {i}. {anom.get('type')}: {anom.get('description')}")
    if len(anomalies) > 3:
        print(f"  ... and {len(anomalies) - 3} more")
    print()
    
    # Fraud signals
    fraud = audit['fraud_signals']
    print(f"FRAUD SIGNALS DETECTED: {len(fraud)}")
    for i, sig in enumerate(fraud[:3], 1):
        print(f"  {i}. {sig.get('type')} ({sig.get('severity')}): {sig.get('description')}")
    if len(fraud) > 3:
        print(f"  ... and {len(fraud) - 3} more")
    print()
    
    # Insights
    insights = audit['financial_insights']
    print(f"FINANCIAL INSIGHTS: {len(insights)}")
    for i, insight in enumerate(insights[:3], 1):
        print(f"  {i}. {insight.get('type')}: {insight.get('description')}")
    print()
    
    # Recommendations
    recs = audit['recommendations']
    print(f"RECOMMENDATIONS: {len(recs)}")
    for i, rec in enumerate(recs[:3], 1):
        print(f"  {i}. [{rec.get('priority').upper()}] {rec.get('title')}")
    if len(recs) > 3:
        print(f"  ... and {len(recs) - 3} more")
    print()
    
    # Cost optimization
    tips = audit['cost_optimization_tips']
    print(f"COST OPTIMIZATION TIPS: {len(tips)}")
    for i, tip in enumerate(tips[:3], 1):
        print(f"  {i}. {tip.get('tip')} (Impact: {tip.get('impact')})")
    print()
    
    # Visualization
    viz = audit['visualization']
    print(f"VISUALIZATION DATA:")
    print(f"  Categories: {len(viz.get('category_distribution', []))} types")
    print(f"  Departments: {len(viz.get('department_distribution', []))} departments")
    print(f"  Spending Trend: {len(viz.get('spending_trend', []))} data points")
    print(f"  Top Spenders: {len(viz.get('top_spenders', []))} employees")
    print()
    
    # Executive summary
    print(f"Report Summary: {report.get('executive_summary', 'No summary generated')}")
    print()
    
    # Save output
    with open('full_audit_report.json', 'w') as f:
        json.dump(result, f, indent=2, cls=NumpyEncoder)
    print("\nFull report saved to: full_audit_report.json")
    print("\n" + "="*80)
    print("TEST COMPLETED SUCCESSFULLY")
    print("="*80 + "\n")


if __name__ == "__main__":
    test_full_audit_workflow()
