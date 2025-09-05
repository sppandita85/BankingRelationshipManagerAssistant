"""
Intent Classification Agent for Banking RM System.
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
from ..core.config import Config
import logging

logger = logging.getLogger(__name__)

class IntentClassifierAgent:
    """Agent responsible for classifying customer query intents."""
    
    def __init__(self):
        """Initialize the Intent Classifier Agent."""
        self.llm = ChatOpenAI(
            model=Config.AGENT_MODEL,
            temperature=Config.TEMPERATURE,
            openai_api_key=Config.OPENAI_API_KEY
        )
        
        self.agent = Agent(
            role="Intent Classification Specialist",
            goal="Accurately classify customer banking queries into appropriate categories",
            backstory="""You are an expert banking customer service specialist with deep knowledge 
            of banking operations and customer intent patterns. You excel at quickly identifying 
            what customers are asking for and categorizing their queries appropriately.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def classify_intent(self, customer_query: str) -> str:
        """
        Classify the intent of a customer query.
        
        Args:
            customer_query: The customer's query text
            
        Returns:
            Classified intent category
        """
        try:
            prompt = Config.INTENT_CLASSIFICATION_PROMPT.format(query=customer_query)
            
            # Use the LLM directly for classification
            response = self.llm.invoke(prompt)
            classification = response.content.strip().upper()
            
            # Validate the classification
            valid_intents = [
                "REMITTANCE_STATUS", "ACCOUNT_BALANCE", "TRANSACTION_HISTORY",
                "INVESTMENT_QUERY", "LOAN_INQUIRY", "CARD_SERVICES", 
                "GENERAL_BANKING", "OUT_OF_SCOPE"
            ]
            
            if classification in valid_intents:
                logger.info(f"Intent classified as: {classification}")
                return classification
            else:
                logger.warning(f"Invalid classification '{classification}', defaulting to OUT_OF_SCOPE")
                return "OUT_OF_SCOPE"
                
        except Exception as e:
            logger.error(f"Error classifying intent: {str(e)}")
            return "OUT_OF_SCOPE"
    
    def is_supported_intent(self, intent: str) -> bool:
        """
        Check if the intent is supported for automated handling.
        
        Args:
            intent: The classified intent
            
        Returns:
            True if the intent is supported, False otherwise
        """
        return intent in Config.SUPPORTED_INTENTS
