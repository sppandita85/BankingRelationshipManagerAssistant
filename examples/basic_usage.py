"""
Basic usage examples for the Banking RM Agent.
"""
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from banking_rm_agent import BankingRMAgent

def example_remittance_query():
    """Example: Remittance status query."""
    print("🏦 Example 1: Remittance Status Query")
    print("=" * 50)
    
    agent = BankingRMAgent()
    
    result = agent.process_customer_query(
        customer_query="What is the status of my remittance transaction TXN001?",
        customer_id="CUST001",
        customer_name="John Doe"
    )
    
    print(f"Query: {result['query']}")
    print(f"Intent: {result['intent']}")
    print(f"Supported: {'✅ Yes' if result['is_supported'] else '❌ No'}")
    print(f"Response: {result['response']}")
    print()

def example_account_balance_query():
    """Example: Account balance query."""
    print("🏦 Example 2: Account Balance Query")
    print("=" * 50)
    
    agent = BankingRMAgent()
    
    result = agent.process_customer_query(
        customer_query="Can you check my current account balance?",
        customer_id="CUST002",
        customer_name="Jane Smith"
    )
    
    print(f"Query: {result['query']}")
    print(f"Intent: {result['intent']}")
    print(f"Supported: {'✅ Yes' if result['is_supported'] else '❌ No'}")
    print(f"Response: {result['response']}")
    print()

def example_out_of_scope_query():
    """Example: Out-of-scope query."""
    print("🏦 Example 3: Out-of-Scope Query")
    print("=" * 50)
    
    agent = BankingRMAgent()
    
    result = agent.process_customer_query(
        customer_query="I want to invest in cryptocurrency and need advice on portfolio diversification",
        customer_id="CUST003",
        customer_name="Bob Johnson"
    )
    
    print(f"Query: {result['query']}")
    print(f"Intent: {result['intent']}")
    print(f"Supported: {'✅ Yes' if result['is_supported'] else '❌ No'}")
    print(f"Response: {result['response']}")
    print()

def example_conversation_history():
    """Example: Retrieving conversation history."""
    print("🏦 Example 4: Conversation History")
    print("=" * 50)
    
    agent = BankingRMAgent()
    
    # Process a few queries
    agent.process_customer_query(
        customer_query="What's my balance?",
        customer_id="CUST004",
        customer_name="Alice Brown"
    )
    
    agent.process_customer_query(
        customer_query="Show me recent transactions",
        customer_id="CUST004",
        customer_name="Alice Brown"
    )
    
    # Get conversation history
    history = agent.get_conversation_history("CUST004")
    
    print(f"Found {len(history)} conversations for CUST004:")
    for i, conv in enumerate(history, 1):
        print(f"{i}. {conv['intent']}: {conv['query'][:50]}...")
    print()

def example_statistics():
    """Example: Agent statistics."""
    print("🏦 Example 5: Agent Statistics")
    print("=" * 50)
    
    agent = BankingRMAgent()
    
    # Process some queries to generate statistics
    queries = [
        "What's my balance?",
        "Check my remittance status",
        "I need investment advice",
        "What are your hours?",
        "Show transaction history"
    ]
    
    for query in queries:
        agent.process_customer_query(query, customer_id="CUST005")
    
    stats = agent.get_agent_statistics()
    
    print(f"Total Queries: {stats['total_queries']}")
    print(f"Supported Queries: {stats['supported_queries']}")
    print(f"Support Rate: {stats['support_rate']:.1%}")
    print(f"Intent Distribution:")
    for intent, count in stats['intent_distribution'].items():
        print(f"  - {intent}: {count}")
    print()

if __name__ == "__main__":
    print("🚀 Banking RM Agent - Basic Usage Examples")
    print("=" * 60)
    print()
    
    try:
        example_remittance_query()
        example_account_balance_query()
        example_out_of_scope_query()
        example_conversation_history()
        example_statistics()
        
        print("✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("Make sure you have:")
        print("1. Installed dependencies: pip install -r requirements.txt")
        print("2. Set up environment variables: cp config/env_example.txt .env")
        print("3. Added your OpenAI API key to the .env file")
