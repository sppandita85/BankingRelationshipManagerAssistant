"""
Authentication Agent for Banking RM System.
Handles customer identity verification and access control.
"""
import hashlib
import jwt
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class CustomerTier(Enum):
    """Customer tier levels for access control."""
    REGULAR = "regular"
    PREMIUM = "premium"
    HNI = "hni"  # High Net Worth Individual
    VIP = "vip"

class AccountStatus(Enum):
    """Account status levels."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    FROZEN = "frozen"
    CLOSED = "closed"

@dataclass
class CustomerProfile:
    """Customer profile information."""
    customer_id: str
    name: str
    email: str
    phone: str
    tier: CustomerTier
    account_status: AccountStatus
    last_login: Optional[datetime] = None
    failed_attempts: int = 0
    locked_until: Optional[datetime] = None

@dataclass
class AuthResult:
    """Authentication result."""
    is_authenticated: bool
    customer_profile: Optional[CustomerProfile] = None
    error_message: Optional[str] = None
    session_token: Optional[str] = None

class AuthenticationAgent:
    """Agent responsible for customer authentication and authorization."""
    
    def __init__(self, secret_key: str = "banking_secret_key_2024"):
        """
        Initialize the Authentication Agent.
        
        Args:
            secret_key: Secret key for JWT token generation
        """
        self.secret_key = secret_key
        self.customer_database = self._initialize_customer_database()
        self.session_tokens = {}  # In production, use Redis or database
        
    def _initialize_customer_database(self) -> Dict[str, CustomerProfile]:
        """Initialize mock customer database."""
        return {
            "CUST001": CustomerProfile(
                customer_id="CUST001",
                name="John Doe",
                email="john.doe@email.com",
                phone="+1234567890",
                tier=CustomerTier.HNI,
                account_status=AccountStatus.ACTIVE
            ),
            "CUST002": CustomerProfile(
                customer_id="CUST002",
                name="Jane Smith",
                email="jane.smith@email.com",
                phone="+1234567891",
                tier=CustomerTier.PREMIUM,
                account_status=AccountStatus.ACTIVE
            ),
            "CUST003": CustomerProfile(
                customer_id="CUST003",
                name="Bob Johnson",
                email="bob.johnson@email.com",
                phone="+1234567892",
                tier=CustomerTier.REGULAR,
                account_status=AccountStatus.ACTIVE
            ),
            "CUST004": CustomerProfile(
                customer_id="CUST004",
                name="Alice Brown",
                email="alice.brown@email.com",
                phone="+1234567893",
                tier=CustomerTier.VIP,
                account_status=AccountStatus.ACTIVE
            ),
            "CUST005": CustomerProfile(
                customer_id="CUST005",
                name="Charlie Wilson",
                email="charlie.wilson@email.com",
                phone="+1234567894",
                tier=CustomerTier.REGULAR,
                account_status=AccountStatus.SUSPENDED
            )
        }
    
    def authenticate_customer(self, customer_id: str, auth_token: str) -> AuthResult:
        """
        Authenticate a customer using their ID and authentication token.
        
        Args:
            customer_id: Customer's unique identifier
            auth_token: Authentication token (could be password, PIN, etc.)
            
        Returns:
            AuthResult with authentication status and customer profile
        """
        try:
            # Check if customer exists
            if customer_id not in self.customer_database:
                logger.warning(f"Authentication failed: Customer {customer_id} not found")
                return AuthResult(
                    is_authenticated=False,
                    error_message="Customer not found"
                )
            
            customer = self.customer_database[customer_id]
            
            # Check if account is locked
            if customer.locked_until and datetime.now() < customer.locked_until:
                logger.warning(f"Authentication failed: Account {customer_id} is locked")
                return AuthResult(
                    is_authenticated=False,
                    error_message="Account is temporarily locked due to multiple failed attempts"
                )
            
            # Check account status
            if customer.account_status != AccountStatus.ACTIVE:
                logger.warning(f"Authentication failed: Account {customer_id} status is {customer.account_status.value}")
                return AuthResult(
                    is_authenticated=False,
                    error_message=f"Account is {customer.account_status.value}"
                )
            
            # Verify authentication token (simplified - in production, use proper hashing)
            if self._verify_auth_token(customer_id, auth_token):
                # Reset failed attempts on successful login
                customer.failed_attempts = 0
                customer.locked_until = None
                customer.last_login = datetime.now()
                
                # Generate session token
                session_token = self._generate_session_token(customer_id)
                self.session_tokens[session_token] = customer_id
                
                logger.info(f"Authentication successful for customer {customer_id}")
                return AuthResult(
                    is_authenticated=True,
                    customer_profile=customer,
                    session_token=session_token
                )
            else:
                # Increment failed attempts
                customer.failed_attempts += 1
                
                # Lock account after 3 failed attempts
                if customer.failed_attempts >= 3:
                    customer.locked_until = datetime.now() + timedelta(minutes=15)
                    logger.warning(f"Account {customer_id} locked due to multiple failed attempts")
                
                logger.warning(f"Authentication failed: Invalid token for customer {customer_id}")
                return AuthResult(
                    is_authenticated=False,
                    error_message="Invalid authentication credentials"
                )
                
        except Exception as e:
            logger.error(f"Authentication error for customer {customer_id}: {e}")
            return AuthResult(
                is_authenticated=False,
                error_message="Authentication service error"
            )
    
    def verify_session_token(self, session_token: str) -> Optional[CustomerProfile]:
        """
        Verify a session token and return customer profile.
        
        Args:
            session_token: Session token to verify
            
        Returns:
            CustomerProfile if token is valid, None otherwise
        """
        try:
            if session_token in self.session_tokens:
                customer_id = self.session_tokens[session_token]
                return self.customer_database.get(customer_id)
            return None
        except Exception as e:
            logger.error(f"Session token verification error: {e}")
            return None
    
    def check_permissions(self, customer_profile: CustomerProfile, query_type: str) -> bool:
        """
        Check if customer has permission to access specific query type.
        
        Args:
            customer_profile: Customer's profile information
            query_type: Type of query being requested
            
        Returns:
            True if customer has permission, False otherwise
        """
        try:
            # Define permission matrix based on customer tier
            permissions = {
                CustomerTier.REGULAR: [
                    "ACCOUNT_BALANCE", "TRANSACTION_HISTORY", "GENERAL_BANKING"
                ],
                CustomerTier.PREMIUM: [
                    "ACCOUNT_BALANCE", "TRANSACTION_HISTORY", "GENERAL_BANKING",
                    "CARD_SERVICES", "INVESTMENT_QUERY"
                ],
                CustomerTier.HNI: [
                    "ACCOUNT_BALANCE", "TRANSACTION_HISTORY", "GENERAL_BANKING",
                    "CARD_SERVICES", "INVESTMENT_QUERY", "REMITTANCE_STATUS"
                ],
                CustomerTier.VIP: [
                    "ACCOUNT_BALANCE", "TRANSACTION_HISTORY", "GENERAL_BANKING",
                    "CARD_SERVICES", "INVESTMENT_QUERY", "REMITTANCE_STATUS",
                    "LOAN_INQUIRY"
                ]
            }
            
            allowed_queries = permissions.get(customer_profile.tier, [])
            has_permission = query_type in allowed_queries
            
            logger.info(f"Permission check for {customer_profile.customer_id} "
                       f"(tier: {customer_profile.tier.value}) for {query_type}: {has_permission}")
            
            return has_permission
            
        except Exception as e:
            logger.error(f"Permission check error: {e}")
            return False
    
    def logout(self, session_token: str) -> bool:
        """
        Logout customer by invalidating session token.
        
        Args:
            session_token: Session token to invalidate
            
        Returns:
            True if logout successful, False otherwise
        """
        try:
            if session_token in self.session_tokens:
                del self.session_tokens[session_token]
                logger.info("Customer logged out successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return False
    
    def _verify_auth_token(self, customer_id: str, auth_token: str) -> bool:
        """
        Verify authentication token (simplified implementation).
        In production, this would use proper password hashing and verification.
        
        Args:
            customer_id: Customer ID
            auth_token: Authentication token
            
        Returns:
            True if token is valid, False otherwise
        """
        # Simplified verification - in production, use proper password hashing
        # For demo purposes, accept "password123" as valid token
        return auth_token == "password123"
    
    def _generate_session_token(self, customer_id: str) -> str:
        """
        Generate a JWT session token.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            JWT session token
        """
        try:
            payload = {
                'customer_id': customer_id,
                'exp': datetime.utcnow() + timedelta(hours=24),  # Token expires in 24 hours
                'iat': datetime.utcnow()
            }
            token = jwt.encode(payload, self.secret_key, algorithm='HS256')
            return token
        except Exception as e:
            logger.error(f"Token generation error: {e}")
            return ""
    
    def get_customer_profile(self, customer_id: str) -> Optional[CustomerProfile]:
        """
        Get customer profile by ID (for internal use).
        
        Args:
            customer_id: Customer ID
            
        Returns:
            CustomerProfile if found, None otherwise
        """
        return self.customer_database.get(customer_id)
    
    def update_customer_profile(self, customer_id: str, **kwargs) -> bool:
        """
        Update customer profile information.
        
        Args:
            customer_id: Customer ID
            **kwargs: Profile fields to update
            
        Returns:
            True if update successful, False otherwise
        """
        try:
            if customer_id in self.customer_database:
                customer = self.customer_database[customer_id]
                for key, value in kwargs.items():
                    if hasattr(customer, key):
                        setattr(customer, key, value)
                logger.info(f"Customer profile updated for {customer_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Profile update error: {e}")
            return False
