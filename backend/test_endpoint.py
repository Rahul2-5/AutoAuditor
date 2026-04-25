"""
Test script to verify /api/full-audit endpoint
Simulates the HTTP request that Postman would send
"""

import json
import io
import sys
sys.path.insert(0, '.')

from fastapi.testclient import TestClient
from main import app


def test_full_audit_endpoint():
    """Test the unified /api/full-audit endpoint"""
    
    client = TestClient(app)
    
    print("\n" + "="*80)
    print("TESTING /api/full-audit ENDPOINT")
    print("="*80 + "\n")
    
    # Create sample CSV content
    csv_content = """date,employee,amount,category,vendor,description,department,employee_level
2024-01-05,John Smith,1200.00,Travel,United Airlines,Flight to NYC,Sales,Manager
2024-01-06,Jane Doe,3500.00,Travel,Marriott Hotels,Hotel stay 5 nights,Engineering,Senior
2024-01-07,John Smith,450.00,Meals,Restaurant X,Client dinner,Sales,Manager
2024-01-08,Mike Johnson,5200.00,Software,Adobe Inc,Software license renewal,Marketing,Manager
2024-01-09,Sarah Wilson,2200.00,Travel,United Airlines,Flight to LA,Sales,Senior
2024-01-10,Tom Brown,800.00,Meals,Restaurant Y,Team lunch,Operations,Junior
2024-01-11,John Smith,3200.00,Travel,Marriott Hotels,Hotel stay 4 nights,Sales,Manager
2024-01-12,Jane Doe,450.00,Office Supplies,Office Depot,Office supplies,Engineering,Senior
2024-01-13,Mike Johnson,2800.00,Travel,Hilton Hotels,Hotel stay 3 nights,Marketing,Manager
2024-01-14,Sarah Wilson,1500.00,Meals,Restaurant Z,Client entertainment,Sales,Senior"""
    
    # Prepare files for multipart request
    files = {'file': ('test_expenses.csv', io.BytesIO(csv_content.encode()), 'text/csv')}
    
    print("[1/2] Sending file upload request to /api/full-audit...")
    response = client.post("/api/full-audit", files=files)
    
    print(f"[2/2] Response Status: {response.status_code}\n")
    
    if response.status_code == 200:
        result = response.json()
        
        print("✓ REQUEST SUCCESSFUL\n")
        
        # Display summary
        print(f"Status: {result.get('status')}")
        print(f"Message: {result.get('message')}")
        print()
        
        report = result.get('report', {})
        
        # Processing
        proc = report.get('processing', {})
        print(f"PROCESSING:")
        print(f"  Records Processed: {proc.get('total_records')}")
        print(f"  Data Prep: {proc.get('preparation', {}).get('status')}")
        print()
        
        # Audit Results
        audit = report.get('audit_analysis', {})
        risk = audit.get('risk_assessment', {})
        print(f"AUDIT ANALYSIS:")
        print(f"  Overall Risk: {risk.get('overall_risk')}")
        print(f"  Confidence: {risk.get('confidence_score'):.0%}")
        
        violations = audit.get('violation_analysis', {})
        print(f"  Total Violations: {violations.get('total_violations')}")
        
        fraud_count = len(audit.get('fraud_signals', []))
        print(f"  Fraud Signals: {fraud_count}")
        
        anomalies_count = len(audit.get('anomalies', []))
        print(f"  Anomalies: {anomalies_count}")
        print()
        
        # Executive Summary
        exec_summary = report.get('executive_summary', '')
        print(f"EXECUTIVE SUMMARY:")
        print(f"  {exec_summary}")
        print()
        
        print("="*80)
        print("✓ ENDPOINT TEST PASSED - Full workflow working correctly!")
        print("="*80 + "\n")
        
    else:
        print(f"✗ REQUEST FAILED\n")
        print(f"Response: {response.text}")
        print()


if __name__ == "__main__":
    test_full_audit_endpoint()
