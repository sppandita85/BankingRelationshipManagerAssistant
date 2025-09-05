"""
Banking-specific tools for the RM Agent system.
"""
import requests
import json
from typing import Dict, Any, Optional
from crewai.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
import logging
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from banking_rm_agent.services.remittance_service import RemittanceService

logger = logging.getLogger(__name__)

class BankingToolInput(BaseModel):
    """Input schema for banking tools."""
    customer_id: str = Field(description="Customer ID or account number")
    query_type: str = Field(description="Type of banking query")

class RemittanceStatusTool(BaseTool):
    """Tool to check remittance status for customers."""
    
    name: str = "remittance_status_checker"
    description: str = "Check the status of remittance transactions for customers"
    
    def _run(self, customer_id: str, transaction_id: Optional[str] = None) -> str:
        """
        Check remittance status for a customer.
        
        Args:
            customer_id: Customer ID or account number
            transaction_id: Optional transaction ID to check specific remittance
            
        Returns:
            Status information about remittance transactions
        """
        try:
            # Mock implementation - replace with actual banking API calls
            mock_data = {
                "customer_id": customer_id,
                "transactions": [
                    {
                        "transaction_id": "TXN001",
                        "amount": "$10,000",
                        "currency": "USD",
                        "status": "Completed",
                        "date": "2024-01-15",
                        "recipient": "John Doe",
                        "country": "USA"
                    },
                    {
                        "transaction_id": "TXN002", 
                        "amount": "$5,000",
                        "currency": "EUR",
                        "status": "In Progress",
                        "date": "2024-01-16",
                        "recipient": "Jane Smith",
                        "country": "Germany"
                    }
                ]
            }
            
            if transaction_id:
                # Filter for specific transaction
                transactions = [t for t in mock_data["transactions"] if t["transaction_id"] == transaction_id]
                if transactions:
                    return f"Transaction {transaction_id} Status: {transactions[0]['status']} - Amount: {transactions[0]['amount']} {transactions[0]['currency']} to {transactions[0]['recipient']} on {transactions[0]['date']}"
                else:
                    return f"Transaction {transaction_id} not found for customer {customer_id}"
            
            # Return all transactions
            status_summary = f"Remittance Status for Customer {customer_id}:\n"
            for txn in mock_data["transactions"]:
                status_summary += f"- {txn['transaction_id']}: {txn['status']} - {txn['amount']} {txn['currency']} to {txn['recipient']} ({txn['country']}) on {txn['date']}\n"
            
            return status_summary
            
        except Exception as e:
            logger.error(f"Error checking remittance status: {str(e)}")
            return f"Unable to retrieve remittance status for customer {customer_id}. Please contact support."

class AccountBalanceTool(BaseTool):
    """Tool to check account balance for customers."""
    
    name: str = "account_balance_checker"
    description: str = "Check account balance and financial summary for customers"
    
    def _run(self, customer_id: str) -> str:
        """
        Check account balance for a customer.
        
        Args:
            customer_id: Customer ID or account number
            
        Returns:
            Account balance and financial summary
        """
        try:
            # Mock implementation - replace with actual banking API calls
            mock_data = {
                "customer_id": customer_id,
                "accounts": [
                    {
                        "account_type": "Savings",
                        "account_number": "****1234",
                        "balance": "$125,000.00",
                        "currency": "USD"
                    },
                    {
                        "account_type": "Checking", 
                        "account_number": "****5678",
                        "balance": "$45,000.00",
                        "currency": "USD"
                    },
                    {
                        "account_type": "Investment",
                        "account_number": "****9012",
                        "balance": "$500,000.00",
                        "currency": "USD"
                    }
                ],
                "total_balance": "$670,000.00"
            }
            
            balance_summary = f"Account Summary for Customer {customer_id}:\n"
            balance_summary += f"Total Balance: {mock_data['total_balance']}\n\n"
            
            for account in mock_data["accounts"]:
                balance_summary += f"- {account['account_type']} ({account['account_number']}): {account['balance']} {account['currency']}\n"
            
            return balance_summary
            
        except Exception as e:
            logger.error(f"Error checking account balance: {str(e)}")
            return f"Unable to retrieve account balance for customer {customer_id}. Please contact support."

class TransactionHistoryTool(BaseTool):
    """Tool to retrieve transaction history for customers."""
    
    name: str = "transaction_history_checker"
    description: str = "Retrieve recent transaction history for customers"
    
    def _run(self, customer_id: str, days: int = 30) -> str:
        """
        Retrieve transaction history for a customer.
        
        Args:
            customer_id: Customer ID or account number
            days: Number of days to look back (default 30)
            
        Returns:
            Recent transaction history
        """
        try:
            # Mock implementation - replace with actual banking API calls
            mock_data = {
                "customer_id": customer_id,
                "transactions": [
                    {
                        "date": "2024-01-15",
                        "description": "Wire Transfer Out",
                        "amount": "-$10,000.00",
                        "balance": "$125,000.00"
                    },
                    {
                        "date": "2024-01-14", 
                        "description": "Salary Deposit",
                        "amount": "+$15,000.00",
                        "balance": "$135,000.00"
                    },
                    {
                        "date": "2024-01-13",
                        "description": "Investment Transfer",
                        "amount": "-$5,000.00",
                        "balance": "$120,000.00"
                    }
                ]
            }
            
            history_summary = f"Transaction History for Customer {customer_id} (Last {days} days):\n"
            for txn in mock_data["transactions"]:
                history_summary += f"- {txn['date']}: {txn['description']} - {txn['amount']} (Balance: {txn['balance']})\n"
            
            return history_summary
            
        except Exception as e:
            logger.error(f"Error retrieving transaction history: {str(e)}")
            return f"Unable to retrieve transaction history for customer {customer_id}. Please contact support."

class GeneralBankingTool(BaseTool):
    """Tool to handle general banking queries."""
    
    name: str = "general_banking_helper"
    description: str = "Provide general banking information and assistance"
    
    def _run(self, query: str) -> str:
        """
        Handle general banking queries.
        
        Args:
            query: Customer's banking query
            
        Returns:
            General banking information or guidance
        """
        try:
            # Mock implementation for general banking queries
            general_responses = {
                "hours": "Our banking hours are Monday-Friday 9:00 AM - 5:00 PM, Saturday 9:00 AM - 1:00 PM",
                "contact": "You can reach our customer service at 1-800-BANK-HELP or visit any branch",
                "services": "We offer savings accounts, checking accounts, investment services, loans, and credit cards",
                "security": "Your accounts are protected by advanced encryption and fraud monitoring systems"
            }
            
            query_lower = query.lower()
            
            if "hours" in query_lower or "time" in query_lower:
                return general_responses["hours"]
            elif "contact" in query_lower or "phone" in query_lower:
                return general_responses["contact"]
            elif "services" in query_lower or "products" in query_lower:
                return general_responses["services"]
            elif "security" in query_lower or "safe" in query_lower:
                return general_responses["security"]
            else:
                return "I can help you with account balances, transaction history, remittance status, and general banking information. Please let me know what specific information you need."
                
        except Exception as e:
            logger.error(f"Error handling general banking query: {str(e)}")
            return "I'm having trouble processing your request. Please contact our customer service for assistance."
