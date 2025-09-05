"""
Configuration settings for the Banking RM Agent system.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Banking RM Agent."""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    AGENT_MODEL = os.getenv("AGENT_MODEL", "gpt-4")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
    
    # Banking System Configuration
    BANKING_API_BASE_URL = os.getenv("BANKING_API_BASE_URL", "https://api.bankingsystem.com")
    BANKING_API_KEY = os.getenv("BANKING_API_KEY")
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "banking_rm_agent.log")
    
    # Agent Configuration
    INTENT_CLASSIFICATION_PROMPT = """
    You are an expert intent classifier for banking customer service queries.
    Classify the following customer query into one of these categories:
    
    1. REMITTANCE_STATUS - Query about remittance status, transfer status, or payment tracking
    2. ACCOUNT_BALANCE - Query about account balance or funds
    3. TRANSACTION_HISTORY - Query about past transactions
    4. INVESTMENT_QUERY - Query about investments, portfolios, or financial products
    5. LOAN_INQUIRY - Query about loans, credit, or borrowing
    6. CARD_SERVICES - Query about debit/credit cards
    7. GENERAL_BANKING - General banking questions
    8. OUT_OF_SCOPE - Query is not related to banking services or is too complex
    
    Customer Query: {query}
    
    Respond with only the category name (e.g., REMITTANCE_STATUS).
    """
    
    APOLOGY_MESSAGE = """
    I apologize, but I'm unable to assist with this particular query at the moment. 
    As your Relationship Manager, I'll personally follow up with you to address this matter. 
    Please expect a call from me within the next business day to ensure we provide you with the best possible service.
    """
    
    # Supported intents for automated handling
    SUPPORTED_INTENTS = [
        "REMITTANCE_STATUS",
        "ACCOUNT_BALANCE", 
        "TRANSACTION_HISTORY",
        "GENERAL_BANKING"
    ]
