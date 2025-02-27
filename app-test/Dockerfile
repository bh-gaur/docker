# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt first to take advantage of Docker layer caching
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . /app/

# Expose port 5000 to make the app accessible from outside the container
EXPOSE 5000

# Define environment variable to indicate this container should run the app
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["python", "app.py"]