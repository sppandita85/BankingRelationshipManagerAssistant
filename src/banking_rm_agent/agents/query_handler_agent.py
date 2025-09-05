"""
Query Handler Agent for Banking RM System.
"""
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from ..core.config import Config
from ..tools.banking_tools import (
    RemittanceStatusTool, 
    AccountBalanceTool, 
    TransactionHistoryTool,
    GeneralBankingTool
)
import logging

logger = logging.getLogger(__name__)

class QueryHandlerAgent:
    """Agent responsible for handling customer queries based on classified intent."""
    
    def __init__(self):
        """Initialize the Query Handler Agent."""
        self.llm = ChatOpenAI(
            model=Config.AGENT_MODEL,
            temperature=Config.TEMPERATURE,
            openai_api_key=Config.OPENAI_API_KEY
        )
        
        # Initialize banking tools
        self.remittance_tool = RemittanceStatusTool()
        self.balance_tool = AccountBalanceTool()
        self.history_tool = TransactionHistoryTool()
        self.general_tool = GeneralBankingTool()
        
        # Create the query handler agent
        self.agent = Agent(
            role="Banking Customer Service Specialist",
            goal="Provide accurate and helpful responses to customer banking queries",
            backstory="""You are an experienced banking relationship manager with extensive 
            knowledge of banking products, services, and customer needs. You excel at 
            providing personalized, accurate, and timely responses to customer inquiries 
            while maintaining a professional and empathetic tone.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                self.remittance_tool,
                self.balance_tool, 
                self.history_tool,
                self.general_tool
            ]
        )
    
    def handle_query(self, customer_query: str, intent: str, customer_id: str = None) -> str:
        """
        Handle customer query based on classified intent.
        
        Args:
            customer_query: The customer's query text
            intent: The classified intent
            customer_id: Customer ID for account-specific queries
            
        Returns:
            Response to the customer query
        """
        try:
            if intent == "OUT_OF_SCOPE":
                return Config.APOLOGY_MESSAGE
            
            # Create appropriate task based on intent
            task_description = self._create_task_description(customer_query, intent, customer_id)
            
            task = Task(
                description=task_description,
                agent=self.agent,
                expected_output="A helpful and accurate response to the customer's banking query"
            )
            
            # Execute the task
            crew = Crew(
                agents=[self.agent],
                tasks=[task],
                verbose=True
            )
            
            result = crew.kickoff()
            return str(result)
            
        except Exception as e:
            logger.error(f"Error handling query: {str(e)}")
            return Config.APOLOGY_MESSAGE
    
    def _create_task_description(self, query: str, intent: str, customer_id: str) -> str:
        """
        Create task description based on intent and query.
        
        Args:
            query: Customer query
            intent: Classified intent
            customer_id: Customer ID
            
        Returns:
            Task description for the agent
        """
        base_context = f"Customer Query: '{query}'\nIntent: {intent}"
        
        if customer_id:
            base_context += f"\nCustomer ID: {customer_id}"
        
        if intent == "REMITTANCE_STATUS":
            return f"""
            {base_context}
            
            The customer is asking about remittance status. Use the remittance_status_checker tool 
            to retrieve the current status of their remittance transactions. Provide a clear, 
            professional response about the status of their transfers, including any relevant 
            transaction details, amounts, and expected completion times.
            """
        
        elif intent == "ACCOUNT_BALANCE":
            return f"""
            {base_context}
            
            The customer is asking about their account balance. Use the account_balance_checker tool 
            to retrieve their current account balances and provide a comprehensive summary. 
            Include information about different account types and total balance.
            """
        
        elif intent == "TRANSACTION_HISTORY":
            return f"""
            {base_context}
            
            The customer is asking about their transaction history. Use the transaction_history_checker tool 
            to retrieve their recent transaction history. Provide a clear summary of recent transactions 
            with dates, descriptions, and amounts.
            """
        
        elif intent == "GENERAL_BANKING":
            return f"""
            {base_context}
            
            The customer has a general banking question. Use the general_banking_helper tool 
            to provide helpful information about banking services, hours, contact information, 
            or other general banking topics. Be informative and helpful.
            """
        
        else:
            return f"""
            {base_context}
            
            Handle this customer query appropriately. If you cannot provide a satisfactory answer 
            using the available tools, provide a helpful response directing them to contact 
            customer service or their relationship manager.
            """
