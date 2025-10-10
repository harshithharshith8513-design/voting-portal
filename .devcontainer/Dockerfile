FROM mcr.microsoft.com/devcontainers/python:3.11

# Install PostgreSQL client
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y postgresql-client \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
