# 🐳 Docker Setup for Banking RM Agent

This guide will help you run the Banking RM Agent using Docker containers, making it portable and easy to deploy on any machine.

## 📋 Prerequisites

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **OpenAI API Key**

### Install Docker

**macOS:**
```bash
# Using Homebrew
brew install --cask docker

# Or download from: https://docs.docker.com/desktop/mac/install/
```

**Linux:**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
```

**Windows:**
Download Docker Desktop from: https://docs.docker.com/desktop/windows/install/

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Run the automated setup script
./docker-run.sh
```

This script will:
- Check Docker installation
- Create `.env` file from template
- Build Docker images
- Start all services
- Verify everything is working

### Option 2: Manual Setup

1. **Set up environment variables:**
```bash
# Copy template and edit with your API key
cp env_template.txt .env
# Edit .env and set: OPENAI_API_KEY=sk-your-actual-api-key-here
```

2. **Build and start services:**
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d
```

3. **Check status:**
```bash
docker-compose ps
```

## 🌐 Access Points

Once running, you can access:

- **Streamlit Web Interface**: http://localhost:8501
- **FastAPI REST API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **PostgreSQL Database**: localhost:5432

## 🗄️ Database Information

**Connection Details:**
- **Host**: localhost (or `postgres` from within containers)
- **Port**: 5432
- **Database**: RMagent
- **Username**: banking_user
- **Password**: banking_password_2024

**Sample Data:**
The database comes pre-populated with:
- 15 sample customers (different tiers: regular, premium, hni, vip)
- 10 sample remittance transactions
- Proper indexes and relationships

## 🛠️ Docker Commands

### Basic Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f banking_rm_agent
docker-compose logs -f postgres
```

### Development Commands

```bash
# Rebuild and restart
docker-compose up --build

# Run in foreground (see logs)
docker-compose up

# Execute commands in running container
docker-compose exec banking_rm_agent bash
docker-compose exec postgres psql -U banking_user -d RMagent
```

### Database Operations

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U banking_user -d RMagent

# Backup database
docker-compose exec postgres pg_dump -U banking_user RMagent > backup.sql

# Restore database
docker-compose exec -T postgres psql -U banking_user -d RMagent < backup.sql
```

## 📁 Project Structure

```
BankingRMAgent/
├── Dockerfile                 # Main application container
├── docker-compose.yml         # Multi-container setup
├── init_db.sql               # Database initialization
├── docker-run.sh             # Automated setup script
├── .dockerignore             # Docker ignore file
├── DOCKER_README.md          # This file
├── src/                      # Application source code
├── logs/                     # Application logs
└── data/                     # Persistent data
```

## 🔧 Configuration

### Environment Variables

Key environment variables in `docker-compose.yml`:

```yaml
environment:
  # Database
  DB_HOST: postgres
  DB_PORT: 5432
  DB_NAME: RMagent
  DB_USER: banking_user
  DB_PASSWORD: banking_password_2024
  
  # OpenAI
  OPENAI_API_KEY: ${OPENAI_API_KEY}
  
  # JWT
  JWT_SECRET_KEY: banking_jwt_secret_2024_secure_key
  
  # Application
  LOG_LEVEL: INFO
  AGENT_MODEL: gpt-4
```

### Ports

- **8501**: Streamlit web interface
- **8000**: FastAPI REST API
- **5432**: PostgreSQL database

### Volumes

- **postgres_data**: Persistent database storage
- **./logs**: Application logs
- **./data**: Application data

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use:**
```bash
# Check what's using the port
lsof -i :8501
lsof -i :8000
lsof -i :5432

# Stop conflicting services or change ports in docker-compose.yml
```

2. **Permission denied:**
```bash
# Make scripts executable
chmod +x docker-run.sh

# On Linux, add user to docker group
sudo usermod -aG docker $USER
# Then logout and login again
```

3. **Container won't start:**
```bash
# Check logs
docker-compose logs banking_rm_agent

# Check if all dependencies are installed
docker-compose build --no-cache
```

4. **Database connection issues:**
```bash
# Check if PostgreSQL is ready
docker-compose exec postgres pg_isready -U banking_user -d RMagent

# Check database logs
docker-compose logs postgres
```

### Reset Everything

```bash
# Stop and remove all containers, networks, and volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Start fresh
./docker-run.sh
```

## 🔒 Security Notes

- Default passwords are used for development
- Change passwords in production
- The `.env` file is not included in Docker images
- Database data persists in Docker volumes

## 🚀 Production Deployment

For production deployment:

1. **Change default passwords**
2. **Use environment-specific configuration**
3. **Set up proper SSL/TLS**
4. **Configure backup strategies**
5. **Use Docker secrets for sensitive data**

## 📊 Monitoring

### Health Checks

```bash
# Check all services
docker-compose ps

# Check specific service health
docker inspect banking_rm_agent | grep Health -A 10
```

### Logs

```bash
# Follow all logs
docker-compose logs -f

# Follow specific service
docker-compose logs -f banking_rm_agent
```

## 🎯 Next Steps

1. **Access the web interface**: http://localhost:8501
2. **Test the API**: http://localhost:8000/docs
3. **Explore the database**: Connect with your favorite PostgreSQL client
4. **Customize configuration**: Edit `docker-compose.yml` as needed

## 📞 Support

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify Docker installation: `docker --version`
3. Check port availability: `lsof -i :8501`
4. Review the troubleshooting section above

---

**Happy Banking! 🏦✨**
