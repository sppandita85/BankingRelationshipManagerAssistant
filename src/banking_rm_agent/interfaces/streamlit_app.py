"""
Streamlit Web Interface for Banking RM Agent.
"""
import streamlit as st
import pandas as pd
import json
from datetime import datetime
import logging
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from banking_rm_agent.core.banking_rm_agent import BankingRMAgent

# Configure page
st.set_page_config(
    page_title="Banking RM Agent",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = BankingRMAgent()

if 'conversations' not in st.session_state:
    st.session_state.conversations = []

def main():
    """Main Streamlit application."""
    
    # Header
    st.title("🏦 Banking Relationship Manager Agent")
    st.markdown("**AI-powered assistant to help RMs serve HNI customers more effectively**")
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Agent Statistics")
        
        # Get agent statistics
        stats = st.session_state.agent.get_agent_statistics()
        
        st.metric("Total Queries", stats['total_queries'])
        st.metric("Supported Queries", stats['supported_queries'])
        st.metric("Support Rate", f"{stats['support_rate']:.1%}")
        
        # Intent distribution
        st.subheader("Intent Distribution")
        intent_df = pd.DataFrame(
            list(stats['intent_distribution'].items()),
            columns=['Intent', 'Count']
        )
        st.bar_chart(intent_df.set_index('Intent'))
        
        # Reset button
        if st.button("🔄 Reset Conversations"):
            st.session_state.agent.reset_conversation_history()
            st.session_state.conversations = []
            st.success("Conversation history reset!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Customer Query Interface")
        
        # Customer information
        customer_id = st.text_input("Customer ID", placeholder="Enter customer ID (optional)")
        customer_name = st.text_input("Customer Name", placeholder="Enter customer name (optional)")
        
        # Query input
        customer_query = st.text_area(
            "Customer Query",
            placeholder="Enter the customer's query here...",
            height=100
        )
        
        # Process button
        if st.button("🚀 Process Query", type="primary"):
            if customer_query.strip():
                with st.spinner("Processing query..."):
                    # Process the query
                    result = st.session_state.agent.process_customer_query(
                        customer_query=customer_query,
                        customer_id=customer_id if customer_id else None,
                        customer_name=customer_name if customer_name else None
                    )
                    
                    # Store in session state
                    st.session_state.conversations.append(result)
                    
                    # Display result
                    st.success("Query processed successfully!")
                    
                    # Show response
                    st.subheader("🤖 Agent Response")
                    st.write(result['response'])
                    
                    # Show metadata
                    with st.expander("📋 Query Details"):
                        st.json({
                            "Intent": result['intent'],
                            "Supported": result.get('supported', False),
                            "Customer ID": result['customer_id'],
                            "Customer Name": result['customer_name'],
                            "Timestamp": result['timestamp']
                        })
            else:
                st.error("Please enter a customer query.")
    
    with col2:
        st.header("📈 Recent Conversations")
        
        if st.session_state.conversations:
            # Display recent conversations
            for i, conv in enumerate(reversed(st.session_state.conversations[-5:])):
                with st.expander(f"Query {len(st.session_state.conversations) - i}: {conv['intent']}"):
                    st.write(f"**Customer:** {conv.get('customer_name', 'N/A')} ({conv.get('customer_id', 'N/A')})")
                    st.write(f"**Query:** {conv['query']}")
                    st.write(f"**Response:** {conv['response']}")
                    st.write(f"**Intent:** {conv['intent']} ({'✅ Supported' if conv['is_supported'] else '❌ Out of Scope'})")
                    st.write(f"**Time:** {conv['timestamp']}")
        else:
            st.info("No conversations yet. Process a query to see results here.")
    
    # Footer
    st.markdown("---")
    st.markdown("**Banking RM Agent** - Powered by CrewAI | Built for HNI Customer Service Excellence")

if __name__ == "__main__":
    main()
