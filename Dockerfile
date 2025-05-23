FROM arm64v8/python:3.10-slim-buster

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-gpiozero \
    python3-gtts \
    python3-gtts-token \
    raspi-gpio \
    mpg123 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY src/requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY src/ ./src/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python3", "src/pi.py"]
