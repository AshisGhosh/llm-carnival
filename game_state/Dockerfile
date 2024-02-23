# Use an official lightweight Python image.
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY shared/pyproject.toml shared/poetry.lock* /app/shared/
RUN cd /app/shared && poetry install --no-dev

# Copy only the pyproject.toml and poetry.lock* to install dependencies
COPY game_state/pyproject.toml game_state/poetry.lock* /app/

# Install dependencies
RUN poetry install --no-dev

# The source code will be mounted via Docker Compose, so no need to COPY
# COPY game_state /app
# COPY shared /app/shared

# The command to run the app will be specified in docker-compose.yml