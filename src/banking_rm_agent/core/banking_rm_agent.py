"""
Main Banking RM Agent - Orchestrates the entire customer query handling process.
"""
from ..agents.intent_classifier_agent import IntentClassifierAgent
from ..agents.query_handler_agent import QueryHandlerAgent
from ..agents.postgresql_auth_agent import PostgreSQLAuthenticationAgent
from .config import Config
import logging
from typing import Dict, Any, Optional
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class BankingRMAgent:
    """Main Banking Relationship Manager Agent."""
    
    def __init__(self):
        """Initialize the Banking RM Agent."""
        self.intent_classifier = IntentClassifierAgent()
        self.query_handler = QueryHandlerAgent()
        self.auth_agent = PostgreSQLAuthenticationAgent()
        self.conversation_history = []
        
        logger.info("Banking RM Agent initialized successfully")
    
    def process_customer_query(self, customer_query: str, customer_id: str = None, 
                             customer_name: str = None, auth_token: str = None,
                             session_token: str = None) -> Dict[str, Any]:
        """
        Process a customer query through the complete pipeline with authentication.
        
        Args:
            customer_query: The customer's query text
            customer_id: Customer ID for account-specific queries
            customer_name: Customer name for personalization
            auth_token: Authentication token for customer verification
            session_token: Session token for authenticated requests
            
        Returns:
            Dictionary containing response, intent, and metadata
        """
        try:
            logger.info(f"Processing query from customer {customer_id}: {customer_query}")
            
            # Step 0: Authenticate customer (if authentication is required)
            customer_profile = None
            if customer_id and (auth_token or session_token):
                if session_token:
                    # Verify existing session
                    customer_profile = self.auth_agent.verify_session_token(session_token)
                    if not customer_profile:
                        return {
                            "response": "Session expired. Please authenticate again.",
                            "intent": "AUTHENTICATION_REQUIRED",
                            "supported": False,
                            "customer_profile": None,
                            "error": "Invalid or expired session token"
                        }
                elif auth_token:
                    # Authenticate with token
                    auth_result = self.auth_agent.authenticate_customer(customer_id, auth_token)
                    if not auth_result.is_authenticated:
                        return {
                            "response": f"Authentication failed: {auth_result.error_message}",
                            "intent": "AUTHENTICATION_FAILED",
                            "supported": False,
                            "customer_profile": None,
                            "error": auth_result.error_message
                        }
                    customer_profile = auth_result.customer_profile
            
            # Step 1: Classify the intent
            intent = self.intent_classifier.classify_intent(customer_query)
            logger.info(f"Intent classified as: {intent}")
            
            # Step 2: Check if intent is supported
            is_supported = self.intent_classifier.is_supported_intent(intent)
            
            # Step 2.5: Check permissions (if customer is authenticated)
            if customer_profile and is_supported:
                has_permission = self.auth_agent.check_permissions(customer_profile, intent)
                if not has_permission:
                    return {
                        "response": f"Access denied. Your account tier ({customer_profile.tier.value}) does not have permission to access this service.",
                        "intent": intent,
                        "supported": False,
                        "customer_profile": customer_profile,
                        "error": "Insufficient permissions"
                    }
            
            # Step 3: Handle the query based on intent
            if is_supported:
                response = self.query_handler.handle_query(
                    customer_query=customer_query,
                    intent=intent,
                    customer_id=customer_id
                )
            else:
                response = Config.APOLOGY_MESSAGE
            
            # Step 4: Create response metadata
            response_data = {
                "response": response,
                "intent": intent,
                "supported": is_supported,
                "customer_id": customer_id,
                "customer_name": customer_name,
                "customer_profile": customer_profile,
                "timestamp": datetime.now().isoformat(),
                "query": customer_query
            }
            
            # Step 5: Store in conversation history
            self.conversation_history.append(response_data)
            
            logger.info(f"Query processed successfully. Intent: {intent}, Supported: {is_supported}")
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error processing customer query: {str(e)}")
            return {
                "response": Config.APOLOGY_MESSAGE,
                "intent": "ERROR",
                "is_supported": False,
                "customer_id": customer_id,
                "customer_name": customer_name,
                "timestamp": datetime.now().isoformat(),
                "query": customer_query,
                "error": str(e)
            }
    
    def get_conversation_history(self, customer_id: str = None) -> list:
        """
        Get conversation history for a specific customer or all customers.
        
        Args:
            customer_id: Optional customer ID to filter history
            
        Returns:
            List of conversation entries
        """
        if customer_id:
            return [entry for entry in self.conversation_history 
                   if entry.get("customer_id") == customer_id]
        return self.conversation_history
    
    def authenticate_customer(self, customer_id: str, auth_token: str) -> Dict[str, Any]:
        """
        Authenticate a customer and return session information.
        
        Args:
            customer_id: Customer ID
            auth_token: Authentication token
            
        Returns:
            Dictionary containing authentication result
        """
        try:
            auth_result = self.auth_agent.authenticate_customer(customer_id, auth_token)
            return {
                "is_authenticated": auth_result.is_authenticated,
                "customer_profile": auth_result.customer_profile,
                "session_token": auth_result.session_token,
                "error_message": auth_result.error_message
            }
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return {
                "is_authenticated": False,
                "customer_profile": None,
                "session_token": None,
                "error_message": str(e)
            }
    
    def logout_customer(self, session_token: str) -> bool:
        """
        Logout a customer by invalidating their session.
        
        Args:
            session_token: Session token to invalidate
            
        Returns:
            True if logout successful, False otherwise
        """
        try:
            return self.auth_agent.logout(session_token)
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return False
    
    def get_customer_profile(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """
        Get customer profile information.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Customer profile dictionary or None
        """
        try:
            profile = self.auth_agent.get_customer_profile(customer_id)
            if profile:
                return {
                    "customer_id": profile.customer_id,
                    "name": profile.name,
                    "email": profile.email,
                    "phone": profile.phone,
                    "tier": profile.tier.value,
                    "account_status": profile.account_status.value,
                    "last_login": profile.last_login.isoformat() if profile.last_login else None
                }
            return None
        except Exception as e:
            logger.error(f"Error getting customer profile: {e}")
            return None

    def get_agent_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about agent performance.
        
        Returns:
            Dictionary containing agent statistics
        """
        total_queries = len(self.conversation_history)
        supported_queries = len([q for q in self.conversation_history if q.get("is_supported")])
        out_of_scope_queries = len([q for q in self.conversation_history if q.get("intent") == "OUT_OF_SCOPE"])
        
        intent_counts = {}
        for entry in self.conversation_history:
            intent = entry.get("intent", "UNKNOWN")
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        return {
            "total_queries": total_queries,
            "supported_queries": supported_queries,
            "out_of_scope_queries": out_of_scope_queries,
            "support_rate": supported_queries / total_queries if total_queries > 0 else 0,
            "intent_distribution": intent_counts,
            "last_updated": datetime.now().isoformat()
        }
    
    def reset_conversation_history(self):
        """Reset the conversation history."""
        self.conversation_history = []
        logger.info("Conversation history reset")
