# 🏦 Banking RM Agent

An intelligent AI-powered banking relationship manager system built with CrewAI, designed to help relationship managers serve High Net Worth Individual (HNI) customers more effectively.

## 🚀 Quick Start with Docker (Recommended)

The easiest way to run the Banking RM Agent is using Docker:

```bash
# Clone the repository
git clone https://github.com/sppandita85/BankingRelationshipManagerAssistant.git
cd BankingRelationshipManagerAssistant

# Run with Docker (automated setup)
./docker-run.sh
```

This will start:
- **Streamlit Web Interface**: http://localhost:8501
- **FastAPI REST API**: http://localhost:8000
- **PostgreSQL Database**: localhost:5432

📖 **For detailed Docker setup instructions, see [DOCKER_README.md](DOCKER_README.md)**

## 🎯 Features

### 🤖 AI Agents
- **IntentClassifierAgent**: Intelligently classifies customer queries
- **QueryHandlerAgent**: Processes queries using specialized banking tools
- **AuthenticationAgent**: Handles customer authentication and session management
- **PostgreSQLAuthenticationAgent**: Production-ready authentication with database

### 🏦 Banking Capabilities
- **Remittance Status Checking**: Real-time transfer status updates
- **Account Balance Queries**: Customer account information
- **Transaction History**: Past transaction details
- **General Banking Support**: Comprehensive banking assistance

### 🔐 Security Features
- **JWT-based Authentication**: Secure session management
- **Permission-based Access Control**: Tier-based customer access (REGULAR, PREMIUM, HNI, VIP)
- **Account Locking**: Security against brute force attacks
- **Environment Variable Management**: Secure API key handling

### 📊 Customer Tiers
- **REGULAR**: Basic banking services
- **PREMIUM**: Enhanced services and priority support
- **HNI**: High Net Worth Individual services
- **VIP**: Premium VIP banking experience

## 🛠️ Manual Installation

If you prefer to run without Docker:

### Prerequisites
- Python 3.12+
- PostgreSQL 15+
- OpenAI API Key

### Setup

1. **Clone and setup environment:**
```bash
git clone https://github.com/sppandita85/BankingRelationshipManagerAssistant.git
cd BankingRelationshipManagerAssistant
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
# Run automated setup
python scripts/setup_env.py

# Edit .env file with your API key
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

3. **Setup database:**
```bash
# Create database
createdb RMagent

# Run the initialization script
psql -d RMagent -f init_db.sql
```

4. **Run the application:**
```bash
# Streamlit interface
streamlit run src/banking_rm_agent/interfaces/streamlit_app.py

# FastAPI server
python src/banking_rm_agent/interfaces/api_server.py
```

## 📁 Project Structure

```
BankingRMAgent/
├── src/banking_rm_agent/          # Main application package
│   ├── agents/                    # AI agents
│   │   ├── intent_classifier_agent.py
│   │   ├── query_handler_agent.py
│   │   ├── authentication_agent.py
│   │   └── postgresql_auth_agent.py
│   ├── core/                      # Core functionality
│   ├── interfaces/                # Web interfaces
│   ├── services/                  # Business logic
│   └── tools/                     # Banking tools
├── tests/                         # Test suite
├── docs/                          # Documentation
├── examples/                      # Usage examples
├── scripts/                       # Utility scripts
├── config/                        # Configuration files
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Multi-container setup
└── init_db.sql                   # Database initialization
```

## 🔌 API Endpoints

### FastAPI REST API (http://localhost:8000)

- `POST /query` - Process customer queries
- `POST /authenticate` - Customer authentication
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### Example API Usage

```python
import requests

# Process a query
response = requests.post("http://localhost:8000/query", json={
    "customer_query": "What is the status of my transfer RF001A?",
    "customer_id": "CUST001"
})

print(response.json())
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_agent.py
python tests/test_authentication.py
```

## 📊 Sample Data

The system comes with sample data:
- **15 customers** across different tiers
- **10 remittance transactions** with various statuses
- **Realistic banking scenarios** for testing

## 🔒 Security

- **Environment Variables**: All sensitive data stored securely
- **JWT Tokens**: Secure session management
- **Database Security**: Proper authentication and permissions
- **API Key Protection**: Never committed to repository

## 📖 Documentation

- **[Docker Setup Guide](DOCKER_README.md)** - Complete Docker instructions
- **[Security Guide](docs/SECURITY_GUIDE.md)** - Security best practices
- **[Usage Guide](docs/USAGE_GUIDE.md)** - Detailed usage instructions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/sppandita85/BankingRelationshipManagerAssistant/issues)
- **Documentation**: Check the `docs/` folder
- **Docker Issues**: See [DOCKER_README.md](DOCKER_README.md)

## 🎉 Acknowledgments

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI) framework
- Powered by OpenAI GPT models
- Database: PostgreSQL
- Web Interface: Streamlit
- API: FastAPI

---

**Built for Banking Excellence 🏦✨**
