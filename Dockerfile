# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Hugging Face Spaces expects the app to listen on port 7860
ENV PORT=7860
EXPOSE 7860

# Run the web server
CMD ["python", "server.py"]
