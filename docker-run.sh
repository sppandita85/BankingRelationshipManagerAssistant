#!/bin/bash

# Banking RM Agent Docker Setup Script
# This script helps you run the Banking RM Agent with Docker

set -e

echo "🚀 Banking RM Agent - Docker Setup"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env_template.txt .env
    echo "📝 Please edit .env file with your OpenAI API key before continuing."
    echo "   Set OPENAI_API_KEY=your_actual_api_key_here"
    read -p "Press Enter after updating .env file..."
fi

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if OpenAI API key is set
if [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ] || [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Please set your OpenAI API key in .env file"
    echo "   OPENAI_API_KEY=sk-your-actual-api-key-here"
    exit 1
fi

echo "✅ Environment check passed"

# Create necessary directories
mkdir -p logs data

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 15

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Show access information
echo ""
echo "🎉 Banking RM Agent is now running!"
echo "=================================="
echo "📊 Streamlit Web Interface: http://localhost:8501"
echo "🔌 FastAPI REST API: http://localhost:8000"
echo "🗄️  PostgreSQL Database: localhost:5432"
echo ""
echo "📋 Database Credentials:"
echo "   Database: RMagent"
echo "   Username: banking_user"
echo "   Password: banking_password_2024"
echo ""
echo "🛠️  Useful Commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart: docker-compose restart"
echo "   Rebuild: docker-compose up --build"
echo ""
echo "📖 API Documentation: http://localhost:8000/docs"
echo ""

# Test the API
echo "🧪 Testing API connection..."
sleep 5
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ FastAPI server is responding"
else
    echo "⚠️  FastAPI server may still be starting up"
fi

echo "🎯 Ready to use! Open http://localhost:8501 in your browser"
