# Use the official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL=postgresql://postgres:domino@some-postgres:5432/postgres

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL dependencies
RUN apt-get update && apt-get install -y libpq-dev

# Create the upload directory and set permissions
RUN mkdir -p /app/temp && chmod -R 755 /app/temp

# Copy the rest of your application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]