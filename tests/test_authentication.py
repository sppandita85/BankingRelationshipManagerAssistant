"""
Test script for Authentication Agent functionality.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from banking_rm_agent import BankingRMAgent
import json

def test_authentication():
    """Test the authentication functionality."""
    print("🔐 Banking RM Agent - Authentication Test")
    print("=" * 50)
    
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
        ("CUST001", "password123", "HNI"),      # HNI customer
        ("CUST004", "password123", "VIP")       # VIP customer
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
    
    # Test 6: Session Token Verification
    print("\n📝 Test 6: Session Token Verification")
    print("-" * 30)
    
    # Authenticate and get session token
    auth_result = agent.authenticate_customer("CUST002", "password123")
    if auth_result['is_authenticated']:
        session_token = auth_result['session_token']
        
        # Verify session token
        profile = agent.auth_agent.verify_session_token(session_token)
        if profile:
            print(f"Session verified for: {profile.name}")
            print(f"Customer ID: {profile.customer_id}")
            print(f"Tier: {profile.tier.value}")
        else:
            print("Session verification failed")
    
    # Test 7: Customer Profile Retrieval
    print("\n📝 Test 7: Customer Profile Retrieval")
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
    
    # Test 8: Logout Functionality
    print("\n📝 Test 8: Logout Functionality")
    print("-" * 30)
    
    # Authenticate first
    auth_result = agent.authenticate_customer("CUST001", "password123")
    if auth_result['is_authenticated']:
        session_token = auth_result['session_token']
        
        # Logout
        logout_success = agent.logout_customer(session_token)
        print(f"Logout successful: {logout_success}")
        
        # Try to use session token after logout
        profile = agent.auth_agent.verify_session_token(session_token)
        print(f"Session token still valid after logout: {profile is not None}")
    
    print("\n🏁 Authentication Tests Completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_authentication()
