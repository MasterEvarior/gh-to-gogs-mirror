# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install tzdata to configure timezone
RUN apt-get update && apt-get install -y tzdata

# Copy the current directory contents into the container
COPY ./script.py /app
COPY ./requirements.txt /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script
CMD ["python", "script.py"]