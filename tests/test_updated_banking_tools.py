"""
Test script for Updated Banking Tools with Real Remittance Service.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from banking_rm_agent.tools.banking_tools import RemittanceStatusTool
import json

def test_updated_banking_tools():
    """Test the updated banking tools with real remittance service."""
    print("🔧 Banking RM Agent - Updated Banking Tools Test")
    print("=" * 60)
    
    # Initialize the remittance status tool
    remittance_tool = RemittanceStatusTool()
    
    # Test 1: Get specific remittance by reference ID
    print("\n📝 Test 1: Get Specific Remittance by Reference ID")
    print("-" * 40)
    
    result = remittance_tool._run("CUST001", "RF998C")
    print("Remittance Details:")
    print(result)
    
    # Test 2: Get all remittances for a customer
    print("\n📝 Test 2: Get All Remittances for Customer")
    print("-" * 40)
    
    result = remittance_tool._run("CUST001")
    print("Customer Remittances:")
    print(result)
    
    # Test 3: Test with different customers
    print("\n📝 Test 3: Test Different Customers")
    print("-" * 40)
    
    customers = ["CUST002", "CUST004", "CUST006"]
    
    for customer_id in customers:
        print(f"\n--- {customer_id} ---")
        result = remittance_tool._run(customer_id)
        print(result[:200] + "..." if len(result) > 200 else result)
    
    # Test 4: Test non-existent reference
    print("\n📝 Test 4: Test Non-existent Reference")
    print("-" * 40)
    
    result = remittance_tool._run("CUST001", "NONEXISTENT")
    print(result)
    
    # Test 5: Test security (customer can't access other customer's remittances)
    print("\n📝 Test 5: Test Security")
    print("-" * 40)
    
    # Try to access CUST002's remittance with CUST001's ID
    result = remittance_tool._run("CUST001", "RF100A")
    print(result)
    
    # Test 6: Test with a customer who has no remittances
    print("\n📝 Test 6: Test Customer with No Remittances")
    print("-" * 40)
    
    result = remittance_tool._run("CUST003")  # CUST003 has no remittances
    print(result)
    
    print("\n🏁 Updated Banking Tools Tests Completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_updated_banking_tools()
