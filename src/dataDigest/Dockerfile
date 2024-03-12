# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app


# Install PostgreSQL client
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir psycopg2 pandas numpy

# Make port 8081 available to the world outside this container
EXPOSE 8081

# Run start.sh when the container launches
CMD ["/usr/src/app/entry_point.sh"]
