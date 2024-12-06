# Base layer - Install Linux - Debian distro
FROM python:3.12.7-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen

# Run our project/services
# Presuming there is a `my_app` command provided by the project
CMD ["uv", "run", "run.py"]

