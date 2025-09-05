# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p logs data

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Expose ports
EXPOSE 8501 8000

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting Banking RM Agent..."\n\
echo "Waiting for PostgreSQL to be ready..."\n\
sleep 10\n\
echo "Starting Streamlit app..."\n\
streamlit run src/banking_rm_agent/interfaces/streamlit_app.py --server.port=8501 --server.address=0.0.0.0 &\n\
echo "Starting FastAPI server..."\n\
cd src/banking_rm_agent/interfaces && python api_server.py --host 0.0.0.0 --port 8000\n\
' > /app/start.sh && chmod +x /app/start.sh

# Default command
CMD ["/app/start.sh"]
