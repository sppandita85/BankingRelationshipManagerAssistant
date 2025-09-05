"""
Test script for Remittance Service functionality.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from banking_rm_agent.services.remittance_service import RemittanceService
import json

def test_remittance_service():
    """Test the remittance service functionality."""
    print("💸 Banking RM Agent - Remittance Service Test")
    print("=" * 60)
    
    # Initialize the service
    service = RemittanceService()
    
    # Test 1: Get remittance by reference ID
    print("\n📝 Test 1: Get Remittance by Reference ID")
    print("-" * 40)
    
    remittance = service.get_remittance_by_reference("RF998C", "CUST001")
    if remittance:
        print(f"Reference ID: {remittance.reference_id}")
        print(f"Amount: ${remittance.amount:,.2f} {remittance.currency}")
        print(f"Status: {remittance.status.value.title()}")
        print(f"Recipient: {remittance.recipient_name}")
        print(f"Country: {remittance.recipient_country}")
        print(f"Initiated: {remittance.initiated_date}")
        print(f"Completed: {remittance.completed_date}")
    else:
        print("Remittance not found")
    
    # Test 2: Get customer remittances
    print("\n📝 Test 2: Get Customer Remittances")
    print("-" * 40)
    
    remittances = service.get_customer_remittances("CUST001", limit=3)
    print(f"Found {len(remittances)} remittances for CUST001:")
    
    for i, remittance in enumerate(remittances, 1):
        print(f"\n  {i}. Reference: {remittance.reference_id}")
        print(f"     Amount: ${remittance.amount:,.2f} {remittance.currency}")
        print(f"     Status: {remittance.status.value.title()}")
        print(f"     Recipient: {remittance.recipient_name}")
        print(f"     Date: {remittance.initiated_date.strftime('%Y-%m-%d')}")
    
    # Test 3: Get remittance status summary
    print("\n📝 Test 3: Get Remittance Status Summary")
    print("-" * 40)
    
    summary = service.get_remittance_status_summary("CUST001")
    if summary:
        print(f"Status Summary for CUST001:")
        print(f"  Total Amount: ${summary.get('total_amount', 0):,.2f}")
        print(f"  Recent Activity (30 days): {summary.get('recent_activity', 0)} transactions")
        
        status_summary = summary.get('status_summary', {})
        for status, data in status_summary.items():
            print(f"  {status.title()}: {data['count']} transactions (${data['total_amount']:,.2f})")
    
    # Test 4: Search remittances
    print("\n📝 Test 4: Search Remittances")
    print("-" * 40)
    
    # Search by reference ID
    search_results = service.search_remittances("CUST001", search_term="RF998")
    print(f"Search results for 'RF998': {len(search_results)} found")
    
    for remittance in search_results:
        print(f"  - {remittance.reference_id}: ${remittance.amount:,.2f} ({remittance.status.value})")
    
    # Test 5: Test with different customers
    print("\n📝 Test 5: Test Different Customers")
    print("-" * 40)
    
    customers = ["CUST001", "CUST002", "CUST004", "CUST006"]
    
    for customer_id in customers:
        remittances = service.get_customer_remittances(customer_id, limit=2)
        print(f"\n{customer_id}: {len(remittances)} remittances")
        
        for remittance in remittances:
            print(f"  - {remittance.reference_id}: ${remittance.amount:,.2f} ({remittance.status.value})")
    
    # Test 6: Test non-existent reference
    print("\n📝 Test 6: Test Non-existent Reference")
    print("-" * 40)
    
    remittance = service.get_remittance_by_reference("NONEXISTENT", "CUST001")
    if remittance:
        print("Unexpected: Found non-existent remittance")
    else:
        print("Correctly returned None for non-existent reference")
    
    # Test 7: Test security (customer can't access other customer's remittances)
    print("\n📝 Test 7: Test Security")
    print("-" * 40)
    
    # Try to access CUST002's remittance with CUST001's ID
    remittance = service.get_remittance_by_reference("RF100A", "CUST001")
    if remittance:
        print("Security issue: CUST001 accessed CUST002's remittance")
    else:
        print("Security working: CUST001 cannot access CUST002's remittance")
    
    print("\n🏁 Remittance Service Tests Completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_remittance_service()
