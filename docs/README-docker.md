# Docker Usage

This document provides instructions for running the MCP Run Python Code server using Docker.

## Quick Start

### Build and Run with Docker Compose

```bash
# Build the image
docker-compose build

# Run the container
docker-compose up

# Run in detached mode
docker-compose up -d

# Stop the container
docker-compose down
```

### Run with Docker CLI

```bash
# Build the image
docker build -t mcp-run-python-code .

# Run the container
docker run -it --rm mcp-run-python-code

# Run with custom base directory
docker run -it --rm -v $(pwd)/code_execution:/tmp/code_execution mcp-run-python-code

# Run in detached mode
docker run -d --name mcp-run-python-server mcp-run-python-code
```

## Docker Configuration

### Base Docker Image
- Uses `python:3.10-slim` for a lightweight container
- Includes necessary system dependencies for Python package installation
- Runs as a non-root user for security

### Environment Variables
- `PYTHONUNBUFFERED=1`: Prevents Python from buffering output
- `PYTHONDONTWRITEBYTECODE=1`: Prevents Python from writing .pyc files

### Directory Structure
- `/app`: Application code directory
- `/tmp/code_execution`: Default working directory for code execution
- `/tmp/code_execution` is owned by the non-root user `mcpuser`

## Docker Compose Configuration

The `docker-compose.yml` file includes:

- **mcp-run-python-code**: Main service running the MCP server
- **Volumes**: Can be mounted for development and persistent data
- **Environment**: Can override base directory and log level
- **Restart policy**: `unless-stopped` for automatic restart

### Development Setup

```bash
# Mount local code execution directory
docker-compose up -d

# View logs
docker-compose logs -f

# Stop and remove
docker-compose down

# Development with live reload (when enabled)
# docker-compose up dev
```

## Docker Commands

### Building and Pushing

```bash
# Build the image
docker build -t mcp-run-python-code .

# Tag for registry
docker tag mcp-run-python-code your-registry/mcp-run-python-code:latest

# Push to registry
docker push your-registry/mcp-run-python-code:latest
```

### Container Management

```bash
# List running containers
docker ps

# View container logs
docker logs mcp-run-python-code-server

# Stop a container
docker stop mcp-run-python-code-server

# Remove a container
docker rm mcp-run-python-code-server

# Enter a running container
docker exec -it mcp-run-python-code-server bash
```

## Security Considerations

- The container runs as a non-root user (`mcpuser`)
- File permissions are properly set for code execution directory
- The `.dockerignore` file excludes sensitive files
- Health checks are configured for monitoring container status

## Troubleshooting

### Common Issues

1. **Permission denied**: Ensure the mounted volumes have proper permissions
2. **Code execution errors**: Check the container logs for detailed error messages
3. **Package installation failures**: The container includes `gcc` for compiling Python packages

### Debug Commands

```bash
# Run container with interactive shell for debugging
docker run -it --rm mcp-run-python-code bash

# Check container health
docker inspect mcp-run-python-code-server --format='{{.State.Health.Status}}'

# View detailed container information
docker inspect mcp-run-python-code-server
```

## Performance Optimization

- Use multi-stage builds for smaller production images
- Layer the Dockerfile for better caching
- Use specific image tags instead of `latest` for production
- Monitor resource usage with `docker stats`