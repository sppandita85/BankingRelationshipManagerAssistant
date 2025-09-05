"""
Authentication Example for Banking RM Agent
Demonstrates how to use the authentication system with customer queries.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from banking_rm_agent import BankingRMAgent, CustomerTier, AccountStatus
import json

def main():
    """Main example function."""
    print("🏦 Banking RM Agent - Authentication Example")
    print("=" * 60)
    
    # Initialize the agent
    agent = BankingRMAgent()
    
    # Example 1: Customer Authentication Flow
    print("\n🔐 Example 1: Customer Authentication Flow")
    print("-" * 40)
    
    customer_id = "CUST001"
    auth_token = "password123"
    
    # Step 1: Authenticate customer
    print(f"Step 1: Authenticating customer {customer_id}...")
    auth_result = agent.authenticate_customer(customer_id, auth_token)
    
    if auth_result['is_authenticated']:
        print(f"✅ Authentication successful!")
        print(f"   Customer: {auth_result['customer_profile'].name}")
        print(f"   Tier: {auth_result['customer_profile'].tier.value}")
        print(f"   Status: {auth_result['customer_profile'].account_status.value}")
        
        session_token = auth_result['session_token']
        print(f"   Session Token: {session_token[:30]}...")
        
        # Step 2: Process authenticated query
        print(f"\nStep 2: Processing authenticated query...")
        result = agent.process_customer_query(
            customer_query="What is my account balance?",
            customer_id=customer_id,
            session_token=session_token
        )
        
        print(f"   Query: What is my account balance?")
        print(f"   Intent: {result['intent']}")
        print(f"   Supported: {result['supported']}")
        print(f"   Response: {result['response'][:100]}...")
        
    else:
        print(f"❌ Authentication failed: {auth_result['error_message']}")
    
    # Example 2: Permission-based Access Control
    print("\n🔒 Example 2: Permission-based Access Control")
    print("-" * 40)
    
    # Test different customer tiers
    test_customers = [
        ("CUST003", "password123", "REGULAR", "Account balance query"),
        ("CUST002", "password123", "PREMIUM", "Investment query"),
        ("CUST001", "password123", "HNI", "Remittance status query"),
        ("CUST004", "password123", "VIP", "Loan inquiry")
    ]
    
    for customer_id, password, tier, query_type in test_customers:
        print(f"\nTesting {tier} customer ({customer_id}):")
        
        # Authenticate
        auth_result = agent.authenticate_customer(customer_id, password)
        if auth_result['is_authenticated']:
            session_token = auth_result['session_token']
            
            # Test query based on tier
            if tier == "REGULAR":
                query = "What is my account balance?"
            elif tier == "PREMIUM":
                query = "What investment options do I have?"
            elif tier == "HNI":
                query = "What is the status of my remittance?"
            else:  # VIP
                query = "How do I apply for a loan?"
            
            result = agent.process_customer_query(
                customer_query=query,
                customer_id=customer_id,
                session_token=session_token
            )
            
            print(f"   Query: {query}")
            print(f"   Intent: {result['intent']}")
            print(f"   Supported: {result['supported']}")
            if result.get('error'):
                print(f"   Error: {result['error']}")
            else:
                print(f"   Response: {result['response'][:80]}...")
        else:
            print(f"   ❌ Authentication failed: {auth_result['error_message']}")
    
    # Example 3: Session Management
    print("\n🔄 Example 3: Session Management")
    print("-" * 40)
    
    # Authenticate and get session
    auth_result = agent.authenticate_customer("CUST002", "password123")
    if auth_result['is_authenticated']:
        session_token = auth_result['session_token']
        print(f"✅ Session created: {session_token[:30]}...")
        
        # Use session for multiple queries
        queries = [
            "What is my account balance?",
            "Show me my transaction history",
            "What are your banking hours?"
        ]
        
        for i, query in enumerate(queries, 1):
            print(f"\n   Query {i}: {query}")
            result = agent.process_customer_query(
                customer_query=query,
                customer_id="CUST002",
                session_token=session_token
            )
            print(f"   Intent: {result['intent']}")
            print(f"   Supported: {result['supported']}")
        
        # Logout
        print(f"\n   Logging out...")
        logout_success = agent.logout_customer(session_token)
        print(f"   Logout successful: {logout_success}")
        
        # Try to use session after logout
        print(f"   Testing session after logout...")
        result = agent.process_customer_query(
            customer_query="What is my account balance?",
            customer_id="CUST002",
            session_token=session_token
        )
        print(f"   Result: {result.get('error', 'Session still valid')}")
    
    # Example 4: Customer Profile Management
    print("\n👤 Example 4: Customer Profile Management")
    print("-" * 40)
    
    # Get customer profile
    profile = agent.get_customer_profile("CUST001")
    if profile:
        print(f"Customer Profile:")
        print(f"   Name: {profile['name']}")
        print(f"   Email: {profile['email']}")
        print(f"   Phone: {profile['phone']}")
        print(f"   Tier: {profile['tier']}")
        print(f"   Status: {profile['account_status']}")
        print(f"   Last Login: {profile['last_login']}")
    
    # Example 5: Error Handling
    print("\n⚠️  Example 5: Error Handling")
    print("-" * 40)
    
    # Test various error scenarios
    error_scenarios = [
        ("CUST999", "password123", "Non-existent customer"),
        ("CUST001", "wrongpassword", "Invalid password"),
        ("CUST005", "password123", "Suspended account")
    ]
    
    for customer_id, password, scenario in error_scenarios:
        print(f"\n   Testing: {scenario}")
        auth_result = agent.authenticate_customer(customer_id, password)
        print(f"   Result: {auth_result['is_authenticated']}")
        if not auth_result['is_authenticated']:
            print(f"   Error: {auth_result['error_message']}")
    
    # Example 6: Security Features
    print("\n🛡️  Example 6: Security Features")
    print("-" * 40)
    
    # Test account locking after failed attempts
    print("   Testing account locking mechanism...")
    
    # Try wrong password multiple times
    for attempt in range(1, 4):
        auth_result = agent.authenticate_customer("CUST001", "wrongpassword")
        print(f"   Attempt {attempt}: {auth_result['is_authenticated']}")
        if not auth_result['is_authenticated']:
            print(f"   Error: {auth_result['error_message']}")
    
    # Try correct password after locking
    print("   Trying correct password after locking...")
    auth_result = agent.authenticate_customer("CUST001", "password123")
    print(f"   Result: {auth_result['is_authenticated']}")
    if not auth_result['is_authenticated']:
        print(f"   Error: {auth_result['error_message']}")
    
    print("\n🏁 Authentication Examples Completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
