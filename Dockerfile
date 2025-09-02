# Use official Python 3.10 slim image
FROM python:3.10-slim

# Set metadata
LABEL maintainer="XuMing <xuming624@qq.com>"
LABEL description="MCP server for running Python code, installing packages, and executing Python files"
LABEL version="0.0.2"

# Set working directory
WORKDIR /app

# Set environment variables to prevent Python buffering
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create a non-root user for security
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Copy the rest of the application code
COPY . .

# Install the package in development mode
RUN pip3 install -e .

# Create temporary directory for code execution
RUN mkdir -p /tmp/code_execution && \
    chown -R mcpuser:mcpuser /tmp/code_execution && \
    chmod 755 /tmp/code_execution

# Switch to non-root user
USER mcpuser

# Set the default working directory for code execution
# WORKDIR .

# Expose ports for both MCP (stdio) and FastAPI
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; print('MCP server container is healthy')" || exit 1

# Default command to run the MCP server
CMD ["mcp-run-python-code"]