"""
Remittance Service for Banking RM System.
Handles remittance operations and status checking using PostgreSQL database.
"""
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class RemittanceStatus(Enum):
    """Remittance status levels."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TransactionType(Enum):
    """Transaction type levels."""
    DOMESTIC = "domestic"
    INTERNATIONAL = "international"
    WIRE_TRANSFER = "wire_transfer"
    ACH = "ach"

@dataclass
class RemittanceDetails:
    """Remittance details information."""
    remittance_id: str
    customer_id: str
    reference_id: str
    amount: float
    currency: str
    sender_name: str
    sender_account: Optional[str]
    recipient_name: str
    recipient_account: Optional[str]
    recipient_bank: Optional[str]
    recipient_country: str
    status: RemittanceStatus
    transaction_type: TransactionType
    purpose: Optional[str]
    exchange_rate: Optional[float]
    fees: float
    net_amount: Optional[float]
    initiated_date: datetime
    processed_date: Optional[datetime]
    completed_date: Optional[datetime]
    failure_reason: Optional[str]

class RemittanceService:
    """Service for handling remittance operations."""
    
    def __init__(self, db_config: Dict[str, str] = None):
        """
        Initialize the Remittance Service.
        
        Args:
            db_config: Database configuration dictionary
        """
        self.db_config = db_config or {
            'host': 'localhost',
            'database': 'RMagent',
            'user': 'sppandita85',
            'port': '5432'
        }
        
        # Test database connection
        self._test_connection()
        
    def _test_connection(self):
        """Test database connection."""
        try:
            conn = psycopg2.connect(**self.db_config)
            conn.close()
            logger.info("Remittance Service - PostgreSQL connection successful")
        except Exception as e:
            logger.error(f"Remittance Service - PostgreSQL connection failed: {e}")
            raise
    
    def _get_connection(self):
        """Get database connection."""
        return psycopg2.connect(**self.db_config)
    
    def get_remittance_by_reference(self, reference_id: str, customer_id: str = None) -> Optional[RemittanceDetails]:
        """
        Get remittance details by reference ID.
        
        Args:
            reference_id: Reference ID of the remittance
            customer_id: Optional customer ID for security check
            
        Returns:
            RemittanceDetails if found, None otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT remittance_id, customer_id, reference_id, amount, currency,
                       sender_name, sender_account, recipient_name, recipient_account,
                       recipient_bank, recipient_country, status, transaction_type,
                       purpose, exchange_rate, fees, net_amount, initiated_date,
                       processed_date, completed_date, failure_reason
                FROM remittances 
                WHERE reference_id = %s
            """
            params = [reference_id]
            
            # Add customer ID filter for security if provided
            if customer_id:
                query += " AND customer_id = %s"
                params.append(customer_id)
            
            cursor.execute(query, params)
            remittance_data = cursor.fetchone()
            
            if remittance_data:
                return RemittanceDetails(
                    remittance_id=remittance_data['remittance_id'],
                    customer_id=remittance_data['customer_id'],
                    reference_id=remittance_data['reference_id'],
                    amount=float(remittance_data['amount']),
                    currency=remittance_data['currency'],
                    sender_name=remittance_data['sender_name'],
                    sender_account=remittance_data['sender_account'],
                    recipient_name=remittance_data['recipient_name'],
                    recipient_account=remittance_data['recipient_account'],
                    recipient_bank=remittance_data['recipient_bank'],
                    recipient_country=remittance_data['recipient_country'],
                    status=RemittanceStatus(remittance_data['status']),
                    transaction_type=TransactionType(remittance_data['transaction_type']),
                    purpose=remittance_data['purpose'],
                    exchange_rate=float(remittance_data['exchange_rate']) if remittance_data['exchange_rate'] else None,
                    fees=float(remittance_data['fees']),
                    net_amount=float(remittance_data['net_amount']) if remittance_data['net_amount'] else None,
                    initiated_date=remittance_data['initiated_date'],
                    processed_date=remittance_data['processed_date'],
                    completed_date=remittance_data['completed_date'],
                    failure_reason=remittance_data['failure_reason']
                )
            return None
            
        except Exception as e:
            logger.error(f"Error getting remittance by reference {reference_id}: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_customer_remittances(self, customer_id: str, limit: int = 10) -> List[RemittanceDetails]:
        """
        Get recent remittances for a customer.
        
        Args:
            customer_id: Customer ID
            limit: Maximum number of remittances to return
            
        Returns:
            List of RemittanceDetails
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT remittance_id, customer_id, reference_id, amount, currency,
                       sender_name, sender_account, recipient_name, recipient_account,
                       recipient_bank, recipient_country, status, transaction_type,
                       purpose, exchange_rate, fees, net_amount, initiated_date,
                       processed_date, completed_date, failure_reason
                FROM remittances 
                WHERE customer_id = %s
                ORDER BY initiated_date DESC
                LIMIT %s
            """, (customer_id, limit))
            
            remittances = []
            for row in cursor.fetchall():
                remittances.append(RemittanceDetails(
                    remittance_id=row['remittance_id'],
                    customer_id=row['customer_id'],
                    reference_id=row['reference_id'],
                    amount=float(row['amount']),
                    currency=row['currency'],
                    sender_name=row['sender_name'],
                    sender_account=row['sender_account'],
                    recipient_name=row['recipient_name'],
                    recipient_account=row['recipient_account'],
                    recipient_bank=row['recipient_bank'],
                    recipient_country=row['recipient_country'],
                    status=RemittanceStatus(row['status']),
                    transaction_type=TransactionType(row['transaction_type']),
                    purpose=row['purpose'],
                    exchange_rate=float(row['exchange_rate']) if row['exchange_rate'] else None,
                    fees=float(row['fees']),
                    net_amount=float(row['net_amount']) if row['net_amount'] else None,
                    initiated_date=row['initiated_date'],
                    processed_date=row['processed_date'],
                    completed_date=row['completed_date'],
                    failure_reason=row['failure_reason']
                ))
            
            return remittances
            
        except Exception as e:
            logger.error(f"Error getting customer remittances for {customer_id}: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_remittance_status_summary(self, customer_id: str) -> Dict[str, Any]:
        """
        Get remittance status summary for a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Dictionary with status summary
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get status counts
            cursor.execute("""
                SELECT status, COUNT(*) as count, SUM(amount) as total_amount
                FROM remittances 
                WHERE customer_id = %s
                GROUP BY status
            """, (customer_id,))
            
            status_summary = {}
            total_amount = 0
            
            for row in cursor.fetchall():
                status_summary[row['status']] = {
                    'count': row['count'],
                    'total_amount': float(row['total_amount']) if row['total_amount'] else 0
                }
                total_amount += float(row['total_amount']) if row['total_amount'] else 0
            
            # Get recent activity
            cursor.execute("""
                SELECT COUNT(*) as recent_count
                FROM remittances 
                WHERE customer_id = %s 
                AND initiated_date >= %s
            """, (customer_id, datetime.now() - timedelta(days=30)))
            
            recent_count = cursor.fetchone()['recent_count']
            
            return {
                'status_summary': status_summary,
                'total_amount': total_amount,
                'recent_activity': recent_count,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting remittance status summary for {customer_id}: {e}")
            return {}
        finally:
            if 'conn' in locals():
                conn.close()
    
    def create_remittance(self, remittance_data: Dict[str, Any]) -> bool:
        """
        Create a new remittance record.
        
        Args:
            remittance_data: Remittance information dictionary
            
        Returns:
            True if creation successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO remittances (
                    remittance_id, customer_id, reference_id, amount, currency,
                    sender_name, sender_account, recipient_name, recipient_account,
                    recipient_bank, recipient_country, status, transaction_type,
                    purpose, exchange_rate, fees, net_amount
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                remittance_data['remittance_id'],
                remittance_data['customer_id'],
                remittance_data['reference_id'],
                remittance_data['amount'],
                remittance_data.get('currency', 'USD'),
                remittance_data['sender_name'],
                remittance_data.get('sender_account'),
                remittance_data['recipient_name'],
                remittance_data.get('recipient_account'),
                remittance_data.get('recipient_bank'),
                remittance_data['recipient_country'],
                remittance_data.get('status', 'pending'),
                remittance_data['transaction_type'],
                remittance_data.get('purpose'),
                remittance_data.get('exchange_rate'),
                remittance_data.get('fees', 0),
                remittance_data.get('net_amount')
            ))
            
            conn.commit()
            logger.info(f"Remittance created: {remittance_data['remittance_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Remittance creation error: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
    
    def update_remittance_status(self, remittance_id: str, status: str, 
                               processed_date: datetime = None, 
                               completed_date: datetime = None,
                               failure_reason: str = None) -> bool:
        """
        Update remittance status.
        
        Args:
            remittance_id: Remittance ID
            status: New status
            processed_date: Processing date
            completed_date: Completion date
            failure_reason: Failure reason if applicable
            
        Returns:
            True if update successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            update_fields = ["status = %s", "updated_at = CURRENT_TIMESTAMP"]
            values = [status]
            
            if processed_date:
                update_fields.append("processed_date = %s")
                values.append(processed_date)
            
            if completed_date:
                update_fields.append("completed_date = %s")
                values.append(completed_date)
            
            if failure_reason:
                update_fields.append("failure_reason = %s")
                values.append(failure_reason)
            
            values.append(remittance_id)
            
            query = f"""
                UPDATE remittances 
                SET {', '.join(update_fields)}
                WHERE remittance_id = %s
            """
            
            cursor.execute(query, values)
            conn.commit()
            
            logger.info(f"Remittance status updated: {remittance_id} -> {status}")
            return True
            
        except Exception as e:
            logger.error(f"Remittance status update error: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
    
    def search_remittances(self, customer_id: str, search_term: str = None, 
                          status: str = None, limit: int = 20) -> List[RemittanceDetails]:
        """
        Search remittances with filters.
        
        Args:
            customer_id: Customer ID
            search_term: Search term for reference ID or recipient name
            status: Filter by status
            limit: Maximum number of results
            
        Returns:
            List of matching RemittanceDetails
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT remittance_id, customer_id, reference_id, amount, currency,
                       sender_name, sender_account, recipient_name, recipient_account,
                       recipient_bank, recipient_country, status, transaction_type,
                       purpose, exchange_rate, fees, net_amount, initiated_date,
                       processed_date, completed_date, failure_reason
                FROM remittances 
                WHERE customer_id = %s
            """
            values = [customer_id]
            
            if search_term:
                query += " AND (reference_id ILIKE %s OR recipient_name ILIKE %s)"
                search_pattern = f"%{search_term}%"
                values.extend([search_pattern, search_pattern])
            
            if status:
                query += " AND status = %s"
                values.append(status)
            
            query += " ORDER BY initiated_date DESC LIMIT %s"
            values.append(limit)
            
            cursor.execute(query, values)
            
            remittances = []
            for row in cursor.fetchall():
                remittances.append(RemittanceDetails(
                    remittance_id=row['remittance_id'],
                    customer_id=row['customer_id'],
                    reference_id=row['reference_id'],
                    amount=float(row['amount']),
                    currency=row['currency'],
                    sender_name=row['sender_name'],
                    sender_account=row['sender_account'],
                    recipient_name=row['recipient_name'],
                    recipient_account=row['recipient_account'],
                    recipient_bank=row['recipient_bank'],
                    recipient_country=row['recipient_country'],
                    status=RemittanceStatus(row['status']),
                    transaction_type=TransactionType(row['transaction_type']),
                    purpose=row['purpose'],
                    exchange_rate=float(row['exchange_rate']) if row['exchange_rate'] else None,
                    fees=float(row['fees']),
                    net_amount=float(row['net_amount']) if row['net_amount'] else None,
                    initiated_date=row['initiated_date'],
                    processed_date=row['processed_date'],
                    completed_date=row['completed_date'],
                    failure_reason=row['failure_reason']
                ))
            
            return remittances
            
        except Exception as e:
            logger.error(f"Error searching remittances: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()
