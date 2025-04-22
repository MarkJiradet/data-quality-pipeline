# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run Streamlit
CMD ["streamlit", "run", "task3_streamlit_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
