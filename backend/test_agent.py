"""
Test Data Preparation Agent
Demonstrates the complete pipeline
"""

import pandas as pd
import json
from services.data_prep_agent import orchestrator


def test_prepare_agent():
    """Test the data preparation agent"""
    
    print("=" * 80)
    print("DATA PREPARATION AGENT - TEST RUN")
    print("=" * 80)
    
    # Load sample data
    print("\n[1] Loading sample expense data...")
    df = pd.read_csv('data/samples/business_expenses.csv')
    print(f"✓ Loaded {len(df)} expense records")
    print(f"✓ Columns: {list(df.columns)}")
    
    # Run preparation pipeline
    print("\n[2] Running data preparation pipeline...")
    result = orchestrator.prepare(df)
    
    # Check result
    if result['status'] != 'success':
        print(f"✗ Pipeline failed: {result['errors']}")
        return
    
    print(f"✓ Pipeline completed successfully")
    
    # Display execution log
    print("\n[3] Pipeline Execution Stages:")
    for log in result['execution_log']:
        status_symbol = "✓" if log['status'] == 'success' else "✗"
        print(f"   {status_symbol} {log['stage']}: {log['details']}")
    
    # Display summary
    print("\n[4] Data Summary:")
    summary = result['summary']
    print(f"   Total Records: {summary['total_records']}")
    print(f"   Total Expense: ${summary['total_expense']:.2f}")
    print(f"   Average Expense: ${summary['average_expense']:.2f}")
    print(f"   Max Expense: ${summary['max_expense']:.2f}")
    print(f"   Date Range: {summary['date_range']['start']} to {summary['date_range']['end']}")
    print(f"   Unique Employees: {summary['unique_employees']}")
    print(f"   Unique Vendors: {summary['unique_vendors']}")
    print(f"   Unique Categories: {summary['unique_categories']}")
    
    # Category breakdown
    print("\n[5] Category Breakdown:")
    for category, stats in summary['category_breakdown'].items():
        print(f"   {category.upper()}: ${stats['total']:.2f} ({stats['count']} txns, {stats['percentage']:.1f}%)")
    
    # Department breakdown
    print("\n[6] Department Breakdown:")
    for dept, stats in summary['department_breakdown'].items():
        print(f"   {dept}: ${stats['total']:.2f} ({stats['count']} txns)")
    
    # Employee level distribution
    print("\n[7] Employee Level Distribution:")
    for level, stats in summary['employee_level_distribution'].items():
        print(f"   {level}: {stats['count']} transactions, ${stats['total']:.2f} total")
    
    # High-value transactions
    print("\n[8] High-Value Transactions (Flagged):")
    flags = result['flags']
    for txn in flags['high_value_transactions'][:3]:
        print(f"   {txn['employee']}: ${txn['amount']:.2f} at {txn['vendor']} ({txn['date']})")
    
    # Risk transactions
    print("\n[9] Risk Transactions (Flagged):")
    for txn in flags['risk_transactions'][:3]:
        print(f"   {txn['employee']}: {txn['vendor']} ({txn['risk_level']} risk)")
        if txn['keywords']:
            print(f"      Keywords: {txn['keywords']}")
    
    # Policy violations
    print("\n[10] Policy Violation Candidates:")
    for txn in flags['policy_violation_candidates'][:3]:
        print(f"   {txn['employee']}: ${txn['amount']:.2f} - {txn['reason']}")
    
    # Frequent spenders
    print("\n[11] Frequent Spenders:")
    for emp in flags['frequent_spenders'][:3]:
        print(f"   {emp['employee']}: ${emp['total_expenses']:.2f} ({emp['transaction_count']} txns)")
    
    # Prepared data sample
    print("\n[12] Prepared Data Sample (First 3 records):")
    df_prepared = result['data']
    
    print(f"\n    Columns: {list(df_prepared.columns)}")
    print("\n    Records:")
    for idx, row in df_prepared.head(3).iterrows():
        print(f"\n    [{idx + 1}] Employee: {row['employee']}")
        print(f"        Amount: ${row['amount']:.2f}")
        print(f"        Category: {row['category']}")
        print(f"        Spending Level: {row['spending_level']}")
        print(f"        Risk Flag: {row['risk_flag']}")
        print(f"        Employee Level: {row['employee_level']}")
        print(f"        Department: {row['inferred_department']}")
        print(f"        Tags: {row['behavioral_tags']}")
    
    # Cleaning statistics
    print("\n[13] Cleaning Statistics:")
    clean_report = summary['cleaning_statistics']
    print(f"   Duplicates Removed: {clean_report['duplicates_removed']}")
    print(f"   Rows with Nulls Dropped: {clean_report['rows_with_nulls_dropped']}")
    print(f"   Invalid Dates: {clean_report['invalid_dates']}")
    print(f"   Invalid Amounts: {clean_report['invalid_amounts']}")
    
    # Enrichment statistics
    print("\n[14] Enrichment Statistics:")
    enrich_report = summary['enrichment_statistics']
    print(f"   High-Value Transactions: {enrich_report['high_value_transactions']}")
    print(f"   Risk Transactions: {enrich_report['risk_transactions']}")
    print(f"   Frequent Spenders: {enrich_report['frequent_spenders']}")
    print(f"   Policy Violations: {enrich_report['policy_violation_candidates']}")
    
    # Export prepared data
    print("\n[15] Exporting prepared data...")
    output_file = 'data/outputs/prepared_expenses.csv'
    df_prepared.to_csv(output_file, index=False)
    print(f"✓ Exported to: {output_file}")
    
    print("\n" + "=" * 80)
    print("✓ TEST COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    test_prepare_agent()
