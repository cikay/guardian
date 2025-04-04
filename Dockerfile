FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements files
COPY Pipfile Pipfile.lock /app/

# Install pip and pipenv
RUN pip install --no-cache-dir pipenv

# Extract requirements from Pipfile and install globally
RUN pipenv requirements > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir uvicorn

# Copy the rest of the application code
COPY . /app