# FastAPI API Documentation

This document provides comprehensive API documentation for the MCP Run Python Code FastAPI server.

## Overview

The FastAPI server provides RESTful API endpoints for executing Python code, installing packages, and running Python files. It serves as an HTTP interface to the core Python code execution functionality.

## Base URL

```
http://localhost:8083
```

## Authentication

Currently, the API does not require authentication. For production use, consider implementing authentication and rate limiting.

## API Endpoints

### 1. Health Check

**GET** `/health`

Check the health and status of the API server.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.0.2",
  "base_dir": "/tmp/tmpXXXXXXXX"
}
```

### 2. Execute Python Code

**POST** `/execute`

Execute Python code directly and optionally return a variable value.

**Request Body:**
```json
{
  "code": "x = 10\ny = 20\nz = x + y\nprint(z)",
  "timeout": 90
}
```

**Parameters:**
- `code` (string, required): The Python code to execute
- `timeout` (integer, optional): Execution timeout in seconds (default: 90)

**Response:**
```json
{
  "success": true,
  "result": "30",
  "error": null,
  "execution_id": "uuid-string"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8083/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "x = 5\ny = 10\nresult = x * y\nprint(result)"
  }'
```

### 3. Save and Execute Code

**POST** `/save-and-execute`

Save Python code to a file and execute it.

**Request Body:**
```json
{
  "file_name": "script.py",
  "code": "def calculate_sum(a, b):\n    return a + b\n\nresult = calculate_sum(5, 10)",
  "variable_to_return": "result",
  "overwrite": true
}
```

**Parameters:**
- `file_name` (string, required): Name of the file to save (e.g., "script.py")
- `code` (string, required): Python code to save and execute
- `variable_to_return` (string, optional): Variable name to return its value
- `overwrite` (boolean, optional): Whether to overwrite existing file (default: true)

**Response:**
```json
{
  "success": true,
  "result": "15",
  "error": null,
  "execution_id": "uuid-string"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8083/save-and-execute" \
  -H "Content-Type: application/json" \
  -d '{
    "file_name": "fibonacci.py",
    "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\nresult = fibonacci(10)",
    "variable_to_return": "result"
  }'
```

### 4. Install Package

**POST** `/install-package`

Install a Python package using pip.

**Request Body:**
```json
{
  "package_name": "requests",
  "upgrade": false
}
```

**Parameters:**
- `package_name` (string, required): Name of the package to install
- `upgrade` (boolean, optional): Whether to upgrade the package if already installed (default: false)

**Response:**
```json
{
  "success": true,
  "result": "successfully installed package requests",
  "error": null,
  "execution_id": "uuid-string"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8083/install-package" \
  -H "Content-Type: application/json" \
  -d '{
    "package_name": "numpy",
    "upgrade": false
  }'
```

### 5. Run Existing Python File

**POST** `/run-python-file`

Run an existing Python file and optionally return a variable value.

**Request Body:**
```json
{
  "file_name": "script.py",
  "variable_to_return": "result"
}
```

**Parameters:**
- `file_name` (string, required): Name of the Python file to run
- `variable_to_return` (string, optional): Variable name to return its value

**Response:**
```json
{
  "success": true,
  "result": "42",
  "error": null,
  "execution_id": "uuid-string"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8083/run-python-file" \
  -H "Content-Type: application/json" \
  -d '{
    "file_name": "existing_script.py",
    "variable_to_return": "output"
  }'
```


## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "result": null,
  "error": "Error message describing the issue",
  "execution_id": "uuid-string"
}
```

Common error scenarios:
- **Syntax errors**: Invalid Python syntax
- **Import errors**: Missing modules or packages
- **Variable not found**: Requested variable doesn't exist
- **File not found**: Specified file doesn't exist
- **Permission denied**: File system permission issues
- **Timeout**: Code execution exceeds timeout limit

## Usage Examples

### Basic Code Execution
```python
import requests

# Execute simple calculation
response = requests.post("http://localhost:8083/execute", json={
    "code": "result = 2 ** 10",
    "variable_to_return": "result"
})
print(response.json())
# Output: {"success": true, "result": "1024", ...}
```

### Data Processing
```python
import requests

# Process JSON data
response = requests.post("http://localhost:8083/execute", json={
    "code": """
import json
data = {'name': 'Alice', 'age': 25}
json_str = json.dumps(data, ensure_ascii=False)
""",
    "variable_to_return": "json_str"
})
print(response.json())
# Output: {"success": true, "result": "{'name': 'Alice', 'age': 25}", ...}
```

### File Operations
```python
import requests

# Save and run script
response = requests.post("http://localhost:8083/save-and-execute", json={
    "file_name": "calculator.py",
    "code": """
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

result = multiply(6, 7)
""",
    "variable_to_return": "result"
})
print(response.json())
# Output: {"success": true, "result": "42", ...}
```

### Package Installation
```python
import requests

# Install package
response = requests.post("http://localhost:8083/install-package", json={
    "package_name": "pandas"
})
print(response.json())
# Output: {"success": true, "result": "successfully installed package pandas", ...}
```

## Security Considerations

1. **Code Execution Security**: The API executes arbitrary Python code, which poses security risks
2. **Sandboxing**: Each execution runs in a temporary directory
3. **Resource Limits**: Consider implementing execution time and memory limits
4. **Network Access**: Be cautious with network access in production
5. **File System**: Limited to the execution directory
6. **Authentication**: Implement proper authentication for production use

## Rate Limiting

Currently, no rate limiting is implemented. Consider adding rate limiting for production deployments.

## CORS Configuration

The server is configured with CORS enabled for all origins. Adjust the `allow_origins` list in the FastAPI configuration for production security.

## Development

### Running the Server

```bash
# Run with uvicorn (development)
python -m run_python_code.fastapi_server

# Or with uvicorn directly
uvicorn run_python_code.fastapi_server:app --host 0.0.0.0 --port 8083 --reload
```

### API Documentation

- **Swagger UI**: `http://localhost:8083/docs`
- **ReDoc**: `http://localhost:8083/redoc`
- **OpenAPI Schema**: `http://localhost:8083/openapi.json`

### Testing

```bash
# Test the API
curl -X GET "http://localhost:8083/health"

# Execute code
curl -X POST "http://localhost:8083/execute" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello, World!\")"}'
```

## Integration Examples

### Python
```python
import requests

# Execute code
response = requests.post('http://localhost:8083/execute', json={
    'code': 'r = sum([1, 2, 3, 4, 5]);print(r)',
})

print(response.json()['result'])  # "15"
```

### Shell Script
```bash
#!/bin/bash

# Execute code
RESULT=$(curl -s -X POST "http://localhost:8083/execute" \
  -H "Content-Type: application/json" \
  -d '{"code": "import os; result = os.getcwd();print(result)"}')

echo "Execution result: $RESULT"
```

## Docker Integration

### Running with Docker Compose
```bash
# Start both MCP and FastAPI services
docker-compose up -d

# View logs
docker-compose logs -f fastapi-server

# Access API documentation
open http://localhost:8083/docs
```

### Using Docker Container
```bash
# Build image
docker build -t mcp-fastapi -f Dockerfile.fastapi .

# Run container
docker run -p 8083:8083 mcp-fastapi

# Test API
curl -X GET "http://localhost:8083/health"
```