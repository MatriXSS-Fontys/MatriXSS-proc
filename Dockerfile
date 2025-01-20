# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set environment variables to prevent python from writing .pyc files and to ensure output is sent straight to terminal
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container's working directory
COPY requirements.txt /app/

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Flask app code to the container
COPY . /app/

# Expose the port that the Flask app will run on (default Flask port is 5000)
EXPOSE 5000

# Define the command to run the Flask app
CMD ["python", "main.py"]
