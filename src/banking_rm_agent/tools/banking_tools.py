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
    
    def _run(self, customer_id: str, reference_id: Optional[str] = None) -> str:
        """
        Check remittance status for a customer.
        
        Args:
            customer_id: Customer ID or account number
            reference_id: Optional reference ID to check specific remittance
            
        Returns:
            Status information about remittance transactions
        """
        try:
            # Initialize the remittance service
            remittance_service = RemittanceService()
            
            if reference_id:
                # Get specific remittance by reference ID
                remittance = remittance_service.get_remittance_by_reference(
                    reference_id, customer_id
                )
                
                if not remittance:
                    return f"Remittance with reference ID {reference_id} not found for customer {customer_id}"
                
                # Format the response
                response = {
                    "reference_id": remittance.reference_id,
                    "amount": f"${remittance.amount:,.2f} {remittance.currency}",
                    "status": remittance.status.value.title(),
                    "transaction_type": remittance.transaction_type.value.replace('_', ' ').title(),
                    "recipient": remittance.recipient_name,
                    "recipient_bank": remittance.recipient_bank,
                    "recipient_country": remittance.recipient_country,
                    "purpose": remittance.purpose,
                    "initiated_date": remittance.initiated_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "processed_date": remittance.processed_date.strftime("%Y-%m-%d %H:%M:%S") if remittance.processed_date else None,
                    "completed_date": remittance.completed_date.strftime("%Y-%m-%d %H:%M:%S") if remittance.completed_date else None,
                    "fees": f"${remittance.fees:.2f}",
                    "net_amount": f"${remittance.net_amount:,.2f}" if remittance.net_amount else None,
                    "failure_reason": remittance.failure_reason
                }
                
                return json.dumps(response, indent=2)
            else:
                # Get recent remittances for the customer
                remittances = remittance_service.get_customer_remittances(customer_id, limit=5)
                
                if not remittances:
                    return f"No remittance transactions found for customer {customer_id}"
                
                # Format the response
                transactions = []
                for remittance in remittances:
                    transactions.append({
                        "reference_id": remittance.reference_id,
                        "amount": f"${remittance.amount:,.2f} {remittance.currency}",
                        "status": remittance.status.value.title(),
                        "transaction_type": remittance.transaction_type.value.replace('_', ' ').title(),
                        "recipient": remittance.recipient_name,
                        "recipient_country": remittance.recipient_country,
                        "initiated_date": remittance.initiated_date.strftime("%Y-%m-%d %H:%M:%S"),
                        "completed_date": remittance.completed_date.strftime("%Y-%m-%d %H:%M:%S") if remittance.completed_date else None
                    })
                
                response = {
                    "customer_id": customer_id,
                    "total_transactions": len(transactions),
                    "transactions": transactions
                }
                
                return json.dumps(response, indent=2)
            
        except Exception as e:
            logger.error(f"Error checking remittance status: {e}")
            return f"Error retrieving remittance status: {str(e)}"

class AccountBalanceTool(BaseTool):
    """Tool to check account balance for customers."""
    
    name: str = "account_balance_checker"
    description: str = "Check account balance for customers"
    
    def _run(self, customer_id: str) -> str:
        """
        Check account balance for a customer.
        
        Args:
            customer_id: Customer ID or account number
            
        Returns:
            Account balance information
        """
        try:
            # Mock implementation - replace with actual banking API calls
            mock_balance = {
                "customer_id": customer_id,
                "account_type": "Savings",
                "balance": "$125,000.00",
                "currency": "USD",
                "last_updated": "2024-01-20 10:30:00",
                "available_balance": "$120,000.00"
            }
            
            return json.dumps(mock_balance, indent=2)
            
        except Exception as e:
            logger.error(f"Error checking account balance: {e}")
            return f"Error retrieving account balance: {str(e)}"

class TransactionHistoryTool(BaseTool):
    """Tool to get transaction history for customers."""
    
    name: str = "transaction_history_checker"
    description: str = "Get transaction history for customers"
    
    def _run(self, customer_id: str, limit: int = 10) -> str:
        """
        Get transaction history for a customer.
        
        Args:
            customer_id: Customer ID or account number
            limit: Number of transactions to retrieve
            
        Returns:
            Transaction history information
        """
        try:
            # Mock implementation - replace with actual banking API calls
            mock_transactions = {
                "customer_id": customer_id,
                "transactions": [
                    {
                        "transaction_id": "TXN001",
                        "date": "2024-01-20",
                        "description": "Salary Deposit",
                        "amount": "+$5,000.00",
                        "balance": "$125,000.00"
                    },
                    {
                        "transaction_id": "TXN002",
                        "date": "2024-01-19",
                        "description": "ATM Withdrawal",
                        "amount": "-$200.00",
                        "balance": "$120,000.00"
                    },
                    {
                        "transaction_id": "TXN003",
                        "date": "2024-01-18",
                        "description": "Online Transfer",
                        "amount": "-$1,500.00",
                        "balance": "$120,200.00"
                    }
                ]
            }
            
            return json.dumps(mock_transactions, indent=2)
            
        except Exception as e:
            logger.error(f"Error retrieving transaction history: {e}")
            return f"Error retrieving transaction history: {str(e)}"

class GeneralBankingTool(BaseTool):
    """Tool to handle general banking inquiries."""
    
    name: str = "general_banking_helper"
    description: str = "Handle general banking inquiries and provide information"
    
    def _run(self, query: str) -> str:
        """
        Handle general banking inquiries.
        
        Args:
            query: General banking query
            
        Returns:
            General banking information
        """
        try:
            # Mock implementation - replace with actual banking API calls
            general_info = {
                "query": query,
                "response": "This is a general banking inquiry response. For specific account information, please use the appropriate tools.",
                "available_services": [
                    "Account Balance Check",
                    "Transaction History",
                    "Remittance Status",
                    "General Banking Information"
                ],
                "contact_info": "For additional assistance, please contact our customer service at 1-800-BANK-HELP"
            }
            
            return json.dumps(general_info, indent=2)
            
        except Exception as e:
            logger.error(f"Error handling general banking inquiry: {e}")
            return f"Error processing general banking inquiry: {str(e)}"
