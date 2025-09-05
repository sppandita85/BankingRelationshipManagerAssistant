"""
Test script for the Banking RM Agent.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from banking_rm_agent import BankingRMAgent
import json

def test_agent():
    """Test the Banking RM Agent with sample queries."""
    
    # Initialize the agent
    agent = BankingRMAgent()
    
    # Test queries
    test_queries = [
        {
            "query": "What is the status of my remittance transaction TXN001?",
            "customer_id": "CUST001",
            "customer_name": "John Doe"
        },
        {
            "query": "Can you check my account balance?",
            "customer_id": "CUST001", 
            "customer_name": "John Doe"
        },
        {
            "query": "Show me my recent transaction history",
            "customer_id": "CUST001",
            "customer_name": "John Doe"
        },
        {
            "query": "What are your banking hours?",
            "customer_id": "CUST002",
            "customer_name": "Jane Smith"
        },
        {
            "query": "I want to invest in cryptocurrency",
            "customer_id": "CUST003",
            "customer_name": "Bob Johnson"
        },
        {
            "query": "How do I apply for a mortgage loan?",
            "customer_id": "CUST004",
            "customer_name": "Alice Brown"
        }
    ]
    
    print("🏦 Banking RM Agent Test Results")
    print("=" * 50)
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n📝 Test Case {i}:")
        print(f"Customer: {test_case['customer_name']} ({test_case['customer_id']})")
        print(f"Query: {test_case['query']}")
        
        # Process the query
        result = agent.process_customer_query(
            customer_query=test_case['query'],
            customer_id=test_case['customer_id'],
            customer_name=test_case['customer_name']
        )
        
        print(f"Intent: {result['intent']}")
        print(f"Supported: {'✅ Yes' if result['is_supported'] else '❌ No'}")
        print(f"Response: {result['response']}")
        print("-" * 30)
    
    # Show statistics
    print("\n📊 Agent Statistics:")
    stats = agent.get_agent_statistics()
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    test_agent()
