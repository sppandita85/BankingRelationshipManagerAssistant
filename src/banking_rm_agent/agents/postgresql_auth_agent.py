"""
PostgreSQL-based Authentication Agent for Banking RM System.
Handles customer identity verification and access control using PostgreSQL database.
"""
import hashlib
import jwt
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
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

class PostgreSQLAuthenticationAgent:
    """PostgreSQL-based Authentication Agent."""
    
    def __init__(self, db_config: Dict[str, str] = None):
        """
        Initialize the PostgreSQL Authentication Agent.
        
        Args:
            db_config: Database configuration dictionary
        """
        self.db_config = db_config or {
            'host': 'localhost',
            'database': 'RMagent',
            'user': 'sppandita85',
            'port': '5432'
        }
        self.secret_key = "banking_secret_key_2024"
        self.session_tokens = {}  # In production, use Redis or database
        
        # Test database connection
        self._test_connection()
        
    def _test_connection(self):
        """Test database connection."""
        try:
            conn = psycopg2.connect(**self.db_config)
            conn.close()
            logger.info("PostgreSQL connection successful")
        except Exception as e:
            logger.error(f"PostgreSQL connection failed: {e}")
            raise
    
    def _get_connection(self):
        """Get database connection."""
        return psycopg2.connect(**self.db_config)
    
    def authenticate_customer(self, customer_id: str, auth_token: str) -> AuthResult:
        """
        Authenticate a customer using their ID and authentication token.
        
        Args:
            customer_id: Customer's unique identifier
            auth_token: Authentication token (password, PIN, etc.)
            
        Returns:
            AuthResult with authentication status and customer profile
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get customer data
            cursor.execute("""
                SELECT customer_id, name, email, phone, tier, account_status, 
                       auth_token, last_login, failed_attempts, locked_until
                FROM customers 
                WHERE customer_id = %s
            """, (customer_id,))
            
            customer_data = cursor.fetchone()
            
            if not customer_data:
                logger.warning(f"Authentication failed: Customer {customer_id} not found")
                return AuthResult(
                    is_authenticated=False,
                    error_message="Customer not found"
                )
            
            # Check if account is locked
            if customer_data['locked_until'] and datetime.now() < customer_data['locked_until']:
                logger.warning(f"Authentication failed: Account {customer_id} is locked")
                return AuthResult(
                    is_authenticated=False,
                    error_message="Account is temporarily locked due to multiple failed attempts"
                )
            
            # Check account status
            if customer_data['account_status'] != 'active':
                logger.warning(f"Authentication failed: Account {customer_id} status is {customer_data['account_status']}")
                return AuthResult(
                    is_authenticated=False,
                    error_message=f"Account is {customer_data['account_status']}"
                )
            
            # Verify authentication token
            if self._verify_auth_token(customer_data['auth_token'], auth_token):
                # Reset failed attempts on successful login
                cursor.execute("""
                    UPDATE customers 
                    SET failed_attempts = 0, locked_until = NULL, 
                        last_login = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
                    WHERE customer_id = %s
                """, (customer_id,))
                conn.commit()
                
                # Create customer profile
                customer_profile = CustomerProfile(
                    customer_id=customer_data['customer_id'],
                    name=customer_data['name'],
                    email=customer_data['email'],
                    phone=customer_data['phone'],
                    tier=CustomerTier(customer_data['tier']),
                    account_status=AccountStatus(customer_data['account_status']),
                    last_login=datetime.now(),
                    failed_attempts=0,
                    locked_until=None
                )
                
                # Generate session token
                session_token = self._generate_session_token(customer_id)
                self.session_tokens[session_token] = customer_id
                
                logger.info(f"Authentication successful for customer {customer_id}")
                return AuthResult(
                    is_authenticated=True,
                    customer_profile=customer_profile,
                    session_token=session_token
                )
            else:
                # Increment failed attempts
                new_failed_attempts = customer_data['failed_attempts'] + 1
                locked_until = None
                
                # Lock account after 3 failed attempts
                if new_failed_attempts >= 3:
                    locked_until = datetime.now() + timedelta(minutes=15)
                    logger.warning(f"Account {customer_id} locked due to multiple failed attempts")
                
                cursor.execute("""
                    UPDATE customers 
                    SET failed_attempts = %s, locked_until = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE customer_id = %s
                """, (new_failed_attempts, locked_until, customer_id))
                conn.commit()
                
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
        finally:
            if 'conn' in locals():
                conn.close()
    
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
                return self.get_customer_profile(customer_id)
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
    
    def _verify_auth_token(self, stored_token: str, provided_token: str) -> bool:
        """
        Verify authentication token.
        
        Args:
            stored_token: Token stored in database
            provided_token: Token provided by user
            
        Returns:
            True if token is valid, False otherwise
        """
        # For now, simple string comparison
        # In production, use proper password hashing (bcrypt, scrypt, etc.)
        return stored_token == provided_token
    
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
        Get customer profile by ID.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            CustomerProfile if found, None otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT customer_id, name, email, phone, tier, account_status, 
                       last_login, failed_attempts, locked_until
                FROM customers 
                WHERE customer_id = %s
            """, (customer_id,))
            
            customer_data = cursor.fetchone()
            
            if customer_data:
                return CustomerProfile(
                    customer_id=customer_data['customer_id'],
                    name=customer_data['name'],
                    email=customer_data['email'],
                    phone=customer_data['phone'],
                    tier=CustomerTier(customer_data['tier']),
                    account_status=AccountStatus(customer_data['account_status']),
                    last_login=customer_data['last_login'],
                    failed_attempts=customer_data['failed_attempts'],
                    locked_until=customer_data['locked_until']
                )
            return None
            
        except Exception as e:
            logger.error(f"Error getting customer profile: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()
    
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
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Build dynamic update query
            update_fields = []
            values = []
            
            for key, value in kwargs.items():
                if key in ['name', 'email', 'phone', 'tier', 'account_status', 'auth_token']:
                    update_fields.append(f"{key} = %s")
                    values.append(value)
            
            if not update_fields:
                return False
            
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            values.append(customer_id)
            
            query = f"""
                UPDATE customers 
                SET {', '.join(update_fields)}
                WHERE customer_id = %s
            """
            
            cursor.execute(query, values)
            conn.commit()
            
            logger.info(f"Customer profile updated for {customer_id}")
            return True
            
        except Exception as e:
            logger.error(f"Profile update error: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
    
    def create_customer(self, customer_data: Dict[str, Any]) -> bool:
        """
        Create a new customer.
        
        Args:
            customer_data: Customer information dictionary
            
        Returns:
            True if creation successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO customers (customer_id, name, email, phone, tier, account_status, auth_token)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                customer_data['customer_id'],
                customer_data['name'],
                customer_data['email'],
                customer_data['phone'],
                customer_data['tier'],
                customer_data['account_status'],
                customer_data['auth_token']
            ))
            
            conn.commit()
            logger.info(f"Customer created: {customer_data['customer_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Customer creation error: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_all_customers(self) -> list:
        """
        Get all customers from database.
        
        Returns:
            List of customer profiles
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT customer_id, name, email, phone, tier, account_status, 
                       last_login, failed_attempts, locked_until, created_at
                FROM customers 
                ORDER BY customer_id
            """)
            
            customers = []
            for row in cursor.fetchall():
                customers.append({
                    'customer_id': row['customer_id'],
                    'name': row['name'],
                    'email': row['email'],
                    'phone': row['phone'],
                    'tier': row['tier'],
                    'account_status': row['account_status'],
                    'last_login': row['last_login'],
                    'failed_attempts': row['failed_attempts'],
                    'locked_until': row['locked_until'],
                    'created_at': row['created_at']
                })
            
            return customers
            
        except Exception as e:
            logger.error(f"Error getting all customers: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()
