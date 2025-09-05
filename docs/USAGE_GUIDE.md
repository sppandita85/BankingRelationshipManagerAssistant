# 📖 Banking RM Agent Usage Guide

This guide provides detailed instructions for using the Banking RM Agent system effectively.

## 🎯 Overview

The Banking RM Agent is designed to help Relationship Managers serve HNI customers more efficiently by:
- Automatically classifying customer queries
- Handling routine banking inquiries
- Providing professional responses for complex queries
- Tracking performance metrics

## 🚀 Getting Started

### 1. Initial Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   - Copy `env_example.txt` to `.env`
   - Add your OpenAI API key
   - Configure other settings as needed

3. **Test Installation**:
   ```bash
   python test_agent.py
   ```

### 2. Running the System

#### Web Interface (Recommended for RMs)
```bash
python run_streamlit.py
```
- Open browser to http://localhost:8501
- User-friendly interface for daily use
- Real-time statistics and conversation history

#### API Server (For Integration)
```bash
python run_api.py
```
- Access at http://localhost:8000
- API documentation at http://localhost:8000/docs
- Suitable for integration with existing systems

## 💬 Using the Web Interface

### 1. Customer Query Processing

1. **Enter Customer Information**:
   - Customer ID (optional but recommended)
   - Customer Name (optional)

2. **Input Customer Query**:
   - Type the customer's question in the text area
   - Be specific and clear for best results

3. **Process Query**:
   - Click "🚀 Process Query" button
   - Wait for the agent to process (usually 2-5 seconds)

4. **Review Response**:
   - Check the agent's response
   - Review intent classification
   - Note if query is supported or out-of-scope

### 2. Understanding Responses

#### ✅ Supported Queries
These queries are handled automatically:
- **REMITTANCE_STATUS**: "What's the status of my transfer?"
- **ACCOUNT_BALANCE**: "What's my current balance?"
- **TRANSACTION_HISTORY**: "Show me recent transactions"
- **GENERAL_BANKING**: "What are your hours?"

#### ❌ Out-of-Scope Queries
These require manual follow-up:
- Investment advice
- Loan applications
- Complex financial planning
- Non-banking topics

### 3. Monitoring Performance

The sidebar shows real-time statistics:
- **Total Queries**: Number of queries processed
- **Supported Queries**: Queries handled automatically
- **Support Rate**: Percentage of automated responses
- **Intent Distribution**: Breakdown of query types

## 🔧 API Usage

### Basic Query Processing

```python
import requests

# Process a customer query
response = requests.post("http://localhost:8000/query", json={
    "query": "What is my account balance?",
    "customer_id": "CUST001",
    "customer_name": "John Doe"
})

result = response.json()
print(f"Intent: {result['intent']}")
print(f"Response: {result['response']}")
```

### Getting Statistics

```python
# Get agent performance statistics
stats = requests.get("http://localhost:8000/statistics").json()
print(f"Support Rate: {stats['support_rate']:.1%}")
```

### Retrieving Conversations

```python
# Get conversation history for a customer
conversations = requests.get(
    "http://localhost:8000/conversations?customer_id=CUST001"
).json()
```

## 📊 Best Practices

### 1. Query Input
- **Be Specific**: "What's the status of transaction TXN001?" vs "Check my transfer"
- **Include Context**: Mention customer ID when available
- **Use Natural Language**: The agent understands conversational queries

### 2. Response Handling
- **Review Intent**: Always check the classified intent
- **Verify Accuracy**: Cross-check automated responses when possible
- **Follow Up**: For out-of-scope queries, ensure personal follow-up

### 3. Performance Monitoring
- **Track Support Rate**: Aim for 70%+ automated handling
- **Monitor Intent Distribution**: Understand customer query patterns
- **Review Out-of-Scope Queries**: Identify opportunities for improvement

## 🎯 Common Use Cases

### 1. Remittance Status Inquiries
**Customer**: "I sent money to my son in the US last week. Can you check the status?"

**Agent Response**: Provides transaction status, amount, recipient, and completion date.

### 2. Account Balance Requests
**Customer**: "What's my current balance across all accounts?"

**Agent Response**: Shows detailed breakdown of all account balances.

### 3. Transaction History
**Customer**: "Can you show me my recent transactions?"

**Agent Response**: Lists recent transactions with dates, descriptions, and amounts.

### 4. General Banking Information
**Customer**: "What are your banking hours?"

**Agent Response**: Provides current banking hours and contact information.

## 🔍 Troubleshooting

### Common Issues

1. **"Unable to retrieve..." Messages**:
   - Check if banking API is properly configured
   - Verify customer ID format
   - Ensure network connectivity

2. **Low Support Rate**:
   - Review out-of-scope queries
   - Consider adding new supported intents
   - Update intent classification prompts

3. **Slow Response Times**:
   - Check OpenAI API key and limits
   - Monitor system resources
   - Consider using faster models for simple queries

### Error Handling

The system includes comprehensive error handling:
- Invalid queries return apology messages
- API errors are logged and handled gracefully
- Fallback responses ensure service continuity

## 📈 Performance Optimization

### 1. Improving Support Rate
- Add new supported intents based on common queries
- Refine intent classification prompts
- Create specialized tools for frequent query types

### 2. Response Quality
- Regularly review agent responses
- Update banking tools with real API integrations
- Fine-tune prompts for better accuracy

### 3. System Performance
- Monitor API response times
- Optimize database queries
- Implement caching for frequent requests

## 🔒 Security Best Practices

1. **API Key Management**:
   - Store keys in environment variables
   - Rotate keys regularly
   - Use least-privilege access

2. **Data Protection**:
   - Log all interactions for audit
   - Implement data encryption
   - Follow banking compliance requirements

3. **Access Control**:
   - Implement proper authentication
   - Use HTTPS in production
   - Monitor access logs

## 📞 Support and Maintenance

### Regular Maintenance
- Monitor system logs
- Update dependencies regularly
- Review and update prompts
- Analyze performance metrics

### Getting Help
- Check system logs in `banking_rm_agent.log`
- Review API documentation
- Test with provided test scripts
- Contact technical support for complex issues

---

**Remember**: The Banking RM Agent is designed to enhance, not replace, the personal touch that RMs provide to HNI customers. Use it as a tool to handle routine queries efficiently while ensuring complex matters receive personal attention.
