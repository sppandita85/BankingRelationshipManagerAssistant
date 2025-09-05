"""
Test script for PostgreSQL Authentication Agent functionality.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from banking_rm_agent import BankingRMAgent
import json

def test_postgresql_authentication():
    """Test the PostgreSQL authentication functionality."""
    print("🗄️ Banking RM Agent - PostgreSQL Authentication Test")
    print("=" * 60)
    
    # Initialize the agent
    agent = BankingRMAgent()
    
    # Test 1: Successful Authentication
    print("\n📝 Test 1: Successful Authentication")
    print("-" * 30)
    
    auth_result = agent.authenticate_customer("CUST001", "password123")
    print(f"Authentication Result: {auth_result['is_authenticated']}")
    if auth_result['is_authenticated']:
        print(f"Customer: {auth_result['customer_profile'].name}")
        print(f"Tier: {auth_result['customer_profile'].tier.value}")
        print(f"Status: {auth_result['customer_profile'].account_status.value}")
        session_token = auth_result['session_token']
        print(f"Session Token: {session_token[:20]}...")
    else:
        print(f"Error: {auth_result['error_message']}")
    
    # Test 2: Failed Authentication
    print("\n📝 Test 2: Failed Authentication")
    print("-" * 30)
    
    auth_result = agent.authenticate_customer("CUST001", "wrongpassword")
    print(f"Authentication Result: {auth_result['is_authenticated']}")
    if not auth_result['is_authenticated']:
        print(f"Error: {auth_result['error_message']}")
    
    # Test 3: Non-existent Customer
    print("\n📝 Test 3: Non-existent Customer")
    print("-" * 30)
    
    auth_result = agent.authenticate_customer("CUST999", "password123")
    print(f"Authentication Result: {auth_result['is_authenticated']}")
    if not auth_result['is_authenticated']:
        print(f"Error: {auth_result['error_message']}")
    
    # Test 4: Authenticated Query Processing
    print("\n📝 Test 4: Authenticated Query Processing")
    print("-" * 30)
    
    # First authenticate
    auth_result = agent.authenticate_customer("CUST001", "password123")
    if auth_result['is_authenticated']:
        session_token = auth_result['session_token']
        
        # Process query with session token
        result = agent.process_customer_query(
            customer_query="What is my account balance?",
            customer_id="CUST001",
            session_token=session_token
        )
        
        print(f"Query: What is my account balance?")
        print(f"Intent: {result['intent']}")
        print(f"Supported: {result['supported']}")
        print(f"Response: {result['response'][:100]}...")
        if result.get('customer_profile'):
            print(f"Customer Tier: {result['customer_profile'].tier.value}")
    
    # Test 5: Permission-based Access Control
    print("\n📝 Test 5: Permission-based Access Control")
    print("-" * 30)
    
    # Test with different customer tiers
    customers = [
        ("CUST003", "password123", "REGULAR"),  # Regular customer
        ("CUST002", "password123", "PREMIUM"),   # Premium customer
        ("CUST001", "password123", "HNI"),       # HNI customer
        ("CUST004", "password123", "VIP")        # VIP customer
    ]
    
    for customer_id, password, tier in customers:
        auth_result = agent.authenticate_customer(customer_id, password)
        if auth_result['is_authenticated']:
            session_token = auth_result['session_token']
            
            # Try to access remittance status (HNI+ only)
            result = agent.process_customer_query(
                customer_query="What is the status of my remittance?",
                customer_id=customer_id,
                session_token=session_token
            )
            
            print(f"\nCustomer {customer_id} ({tier}):")
            print(f"  Query: Remittance status")
            print(f"  Intent: {result['intent']}")
            print(f"  Supported: {result['supported']}")
            if result.get('error'):
                print(f"  Error: {result['error']}")
    
    # Test 6: Customer Profile Retrieval
    print("\n📝 Test 6: Customer Profile Retrieval")
    print("-" * 30)
    
    profile = agent.get_customer_profile("CUST001")
    if profile:
        print(f"Customer Profile:")
        print(f"  Name: {profile['name']}")
        print(f"  Email: {profile['email']}")
        print(f"  Phone: {profile['phone']}")
        print(f"  Tier: {profile['tier']}")
        print(f"  Status: {profile['account_status']}")
        print(f"  Last Login: {profile['last_login']}")
    
    # Test 7: Database Operations
    print("\n📝 Test 7: Database Operations")
    print("-" * 30)
    
    # Test getting all customers
    all_customers = agent.auth_agent.get_all_customers()
    print(f"Total customers in database: {len(all_customers)}")
    
    for customer in all_customers[:3]:  # Show first 3
        print(f"  {customer['customer_id']}: {customer['name']} ({customer['tier']})")
    
    # Test 8: Account Locking Mechanism
    print("\n📝 Test 8: Account Locking Mechanism")
    print("-" * 30)
    
    # Try wrong password multiple times for CUST002
    print("Testing account locking for CUST002...")
    for attempt in range(1, 4):
        auth_result = agent.authenticate_customer("CUST002", "wrongpassword")
        print(f"  Attempt {attempt}: {auth_result['is_authenticated']}")
        if not auth_result['is_authenticated']:
            print(f"    Error: {auth_result['error_message']}")
    
    # Try correct password after locking
    print("  Trying correct password after locking...")
    auth_result = agent.authenticate_customer("CUST002", "password123")
    print(f"  Result: {auth_result['is_authenticated']}")
    if not auth_result['is_authenticated']:
        print(f"    Error: {auth_result['error_message']}")
    
    print("\n🏁 PostgreSQL Authentication Tests Completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_postgresql_authentication()
