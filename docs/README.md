# 🏦 Banking Relationship Manager Agent

An AI-powered chatbot system built with CrewAI to help Relationship Managers (RMs) serve High Net Worth Individual (HNI) customers more effectively. The system automatically classifies customer queries, handles supported intents, and provides apology messages for out-of-scope queries.

## 🎯 Key Features

- **Intent Classification**: Automatically identifies customer query intents
- **Automated Query Handling**: Processes supported banking queries automatically
- **Customer Authentication**: Secure customer identity verification and session management
- **Permission-based Access Control**: Different access levels based on customer tier
- **Remittance Status Checking**: Specialized tool for remittance transaction status
- **Account Balance & Transaction History**: Quick access to customer financial data
- **Out-of-Scope Handling**: Professional apology messages for unsupported queries
- **Multiple Interfaces**: Web UI (Streamlit) and REST API (FastAPI)
- **Real-time Statistics**: Track agent performance and query patterns
- **Security Features**: Account locking, audit logging, and session management

## 🔐 Authentication System

The Banking RM Agent includes a comprehensive authentication system with the following features:

### Customer Tiers and Permissions

| Tier | Permissions |
|------|-------------|
| **REGULAR** | Account Balance, Transaction History, General Banking |
| **PREMIUM** | + Card Services, Investment Queries |
| **HNI** | + Remittance Status |
| **VIP** | + Loan Inquiries |

### Security Features

- **JWT Session Tokens**: Secure session management with expiration
- **Account Locking**: Automatic locking after 3 failed authentication attempts
- **Permission Validation**: Real-time permission checking based on customer tier
- **Audit Logging**: Complete authentication and access logs
- **Session Management**: Secure login/logout functionality

### Authentication Flow

1. **Customer Authentication**: Verify customer identity with tokens
2. **Session Creation**: Generate JWT session token upon successful authentication
3. **Permission Check**: Validate customer permissions for requested query type
4. **Query Processing**: Process query if permissions are sufficient
5. **Session Management**: Maintain session state and handle logout

## 🏗️ Project Structure

```
BankingRMAgent/
├── src/
│   └── banking_rm_agent/
│       ├── __init__.py
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── intent_classifier.py
│       │   ├── query_handler.py
│       │   └── authentication_agent.py
│       ├── tools/
│       │   ├── __init__.py
│       │   └── banking_tools.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── banking_rm_agent.py
│       │   └── config.py
│       └── interfaces/
│           ├── __init__.py
│           ├── streamlit_app.py
│           └── api_server.py
├── config/
│   ├── env_example.txt
│   └── settings.yaml
├── scripts/
│   ├── run_streamlit.py
│   └── run_api.py
├── tests/
│   ├── __init__.py
│   ├── test_agent.py
│   └── test_authentication.py
├── docs/
│   ├── README.md
│   └── USAGE_GUIDE.md
├── examples/
│   ├── basic_usage.py
│   └── authentication_example.py
├── requirements.txt
├── setup.py
├── pyproject.toml
├── Makefile
└── .gitignore
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Banking system API access (optional for mock data)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd BankingRMAgent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp config/env_example.txt .env
   # Edit .env with your OpenAI API key and other configurations
   ```

### Running the Application

#### Option 1: Streamlit Web Interface
```bash
python scripts/run_streamlit.py
# or
make run-streamlit
```
Access the web interface at: http://localhost:8501

#### Option 2: FastAPI REST API
```bash
python scripts/run_api.py
# or
make run-api
```
Access the API at: http://localhost:8000
API documentation at: http://localhost:8000/docs

#### Option 3: Command Line Testing
```bash
python tests/test_agent.py
# or
make run-test
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Banking System Configuration (Optional)
BANKING_API_BASE_URL=https://api.bankingsystem.com
BANKING_API_KEY=your_banking_api_key_here

# Agent Configuration
AGENT_MODEL=gpt-4
TEMPERATURE=0.1
MAX_TOKENS=1000

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=banking_rm_agent.log
```

### Customization
- Modify `src/banking_rm_agent/core/config.py` to adjust agent behavior and prompts
- Update banking tools in `src/banking_rm_agent/tools/banking_tools.py` to integrate with real APIs
- Customize intent classification in `src/banking_rm_agent/agents/intent_classifier.py`

## 📊 Usage Examples

### Example 1: Remittance Status Query
**Customer Query**: "What is the status of my remittance transaction TXN001?"

**Agent Response**:
```
Transaction TXN001 Status: Completed - Amount: $10,000 USD to John Doe on 2024-01-15
```

### Example 2: Account Balance Query
**Customer Query**: "Can you check my account balance?"

**Agent Response**:
```
Account Summary for Customer CUST001:
Total Balance: $670,000.00

- Savings (****1234): $125,000.00 USD
- Checking (****5678): $45,000.00 USD
- Investment (****9012): $500,000.00 USD
```

### Example 3: Out-of-Scope Query
**Customer Query**: "I want to invest in cryptocurrency"

**Agent Response**:
```
I apologize, but I'm unable to assist with this particular query at the moment. 
As your Relationship Manager, I'll personally follow up with you to address this matter. 
Please expect a call from me within the next business day to ensure we provide you with the best possible service.
```

## 🔌 API Usage

### Process Query
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What is my account balance?",
       "customer_id": "CUST001",
       "customer_name": "John Doe"
     }'
```

### Get Statistics
```bash
curl -X GET "http://localhost:8000/statistics"
```

### Get Conversations
```bash
curl -X GET "http://localhost:8000/conversations?customer_id=CUST001"
```

## 📈 Monitoring & Analytics

The system provides comprehensive monitoring capabilities:

- **Real-time Statistics**: Track support rate, query distribution, and performance metrics
- **Conversation History**: Maintain complete audit trail of customer interactions
- **Intent Analysis**: Understand customer query patterns and trends
- **Performance Metrics**: Monitor agent effectiveness and identify improvement areas

## 🛠️ Development

### Development Setup
```bash
# Complete development setup
make dev-setup

# Run tests
make test

# Format code
make format

# Run linting
make lint
```

### Adding New Tools
1. Create a new tool class in `src/banking_rm_agent/tools/banking_tools.py`
2. Inherit from `BaseTool` and implement the `_run` method
3. Add the tool to the Query Handler Agent's tools list
4. Update intent classification to handle new query types

### Adding New Intents
1. Update the `INTENT_CLASSIFICATION_PROMPT` in `src/banking_rm_agent/core/config.py`
2. Add the new intent to `SUPPORTED_INTENTS` if it should be automated
3. Create appropriate task descriptions in `src/banking_rm_agent/agents/query_handler.py`

## 🔒 Security Considerations

- Store API keys securely in environment variables
- Implement proper authentication for production deployments
- Log all customer interactions for audit purposes
- Ensure compliance with banking data protection regulations
- Use HTTPS in production environments

## 🚀 Deployment

### Production Deployment
1. Set up a production environment with proper security
2. Configure environment variables for production
3. Set up monitoring and logging
4. Implement proper error handling and fallback mechanisms
5. Set up CI/CD pipeline for automated deployments

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000 8501

CMD ["python", "scripts/run_api.py"]
```

## 📞 Support

For technical support or questions:
- Check the logs in `banking_rm_agent.log`
- Review the API documentation at `/docs` endpoint
- Test with the provided test script
- Ensure all environment variables are properly configured

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Built with ❤️ using CrewAI for Banking Excellence**