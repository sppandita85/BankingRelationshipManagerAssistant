# 🔐 Security Guide for Banking RM Agent

## API Key Management Best Practices

### 1. Environment Variables (Recommended)

**Never commit API keys directly to your code or repository!**

#### Setup Steps:

1. **Create a `.env` file** in your project root:
```bash
# Copy the template
cp env_template.txt .env
```

2. **Fill in your actual values** in `.env`:
```bash
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=RMagent
DB_USER=sppandita85
DB_PASSWORD=your_actual_database_password

# JWT Secret for Authentication (generate a strong random key)
JWT_SECRET_KEY=your-super-secret-jwt-key-here

# Application Configuration
LOG_LEVEL=INFO
LOG_FILE=banking_rm_agent.log
```

3. **Verify `.env` is in `.gitignore`** (it should be):
```bash
# Check if .env is ignored
git check-ignore .env
```

### 2. Generate Strong JWT Secret

Use Python to generate a secure JWT secret:

```python
import secrets
print(secrets.token_urlsafe(32))
```

### 3. Production Security Measures

#### A. Use Secret Management Services

**For Production Environments:**

- **AWS Secrets Manager**
- **Azure Key Vault**
- **Google Secret Manager**
- **HashiCorp Vault**

#### B. Environment-Specific Configuration

```bash
# Development
.env.development

# Staging
.env.staging

# Production
.env.production
```

#### C. Docker Secrets (if using Docker)

```dockerfile
# Use Docker secrets for sensitive data
RUN echo "$OPENAI_API_KEY" > /run/secrets/openai_key
```

### 4. Database Security

#### A. Connection Security
- Use SSL/TLS for database connections
- Implement connection pooling
- Use read-only users for queries

#### B. Password Security
- Use strong, unique passwords
- Rotate passwords regularly
- Consider using database certificates

### 5. API Key Rotation

#### A. Regular Rotation Schedule
- Rotate API keys monthly/quarterly
- Implement key versioning
- Use multiple keys for redundancy

#### B. Monitoring and Alerting
- Monitor API key usage
- Set up alerts for unusual activity
- Track failed authentication attempts

### 6. Code Security

#### A. Never Hardcode Secrets
```python
# ❌ BAD - Never do this
OPENAI_API_KEY = "sk-1234567890abcdef"

# ✅ GOOD - Use environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

#### B. Validate Environment Variables
```python
def validate_required_env_vars():
    required_vars = ["OPENAI_API_KEY", "DB_PASSWORD", "JWT_SECRET_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {missing_vars}")
```

### 7. Deployment Security

#### A. Server Configuration
- Use HTTPS in production
- Implement proper firewall rules
- Regular security updates

#### B. Access Control
- Implement proper user authentication
- Use role-based access control (RBAC)
- Monitor user activities

### 8. Monitoring and Logging

#### A. Security Logging
```python
import logging

# Log security events
security_logger = logging.getLogger('security')
security_logger.warning(f"Failed authentication attempt for user: {user_id}")
```

#### B. Audit Trail
- Log all authentication attempts
- Track data access patterns
- Monitor system changes

### 9. Backup and Recovery

#### A. Secure Backups
- Encrypt backup data
- Store backups securely
- Test recovery procedures

#### B. Disaster Recovery
- Document recovery procedures
- Test recovery scenarios
- Maintain backup integrity

### 10. Compliance

#### A. Data Protection
- Implement GDPR compliance
- Follow PCI DSS standards
- Maintain data privacy

#### B. Regular Audits
- Conduct security audits
- Review access permissions
- Update security policies

## Quick Setup Commands

```bash
# 1. Create .env file
cp env_template.txt .env

# 2. Generate JWT secret
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"

# 3. Verify .env is ignored
git check-ignore .env

# 4. Test configuration
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OpenAI Key:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"
```

## Security Checklist

- [ ] `.env` file created and configured
- [ ] `.env` file added to `.gitignore`
- [ ] Strong JWT secret generated
- [ ] Database password is secure
- [ ] API keys are not hardcoded
- [ ] Environment variables validated
- [ ] HTTPS enabled in production
- [ ] Security logging implemented
- [ ] Access controls configured
- [ ] Backup procedures in place
- [ ] Security monitoring active
- [ ] Regular security audits scheduled

## Emergency Procedures

### If API Key is Compromised:

1. **Immediately rotate the key** in your service provider's dashboard
2. **Update your `.env` file** with the new key
3. **Restart your application**
4. **Monitor for suspicious activity**
5. **Review access logs**

### If Database is Compromised:

1. **Change database passwords immediately**
2. **Review database access logs**
3. **Check for unauthorized data access**
4. **Update connection strings**
5. **Implement additional security measures**

Remember: **Security is an ongoing process, not a one-time setup!**
