# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: FastAPI server for Python code execution
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import tempfile
import uuid
from contextlib import asynccontextmanager
import uvicorn
from loguru import logger
import sys

sys.path.append('.')
from run_python_code.code import RunPythonCode


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("FastAPI server starting...")
    # Initialize temporary base directory
    temp_dir = tempfile.mkdtemp()
    app.state.base_dir = temp_dir
    app.state.python_runner = RunPythonCode(base_dir=temp_dir)
    logger.info(f"Temporary code execution directory created: {temp_dir}")

    yield

    # Shutdown
    logger.info("FastAPI server shutting down...")


app = FastAPI(
    title="MCP Run Python Code API",
    description="API for executing Python code, installing packages, and running Python files",
    version="0.0.2",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class CodeExecutionRequest(BaseModel):
    code: str
    timeout: Optional[int] = 90


class FileExecutionRequest(BaseModel):
    file_name: str
    code: str
    variable_to_return: Optional[str] = None
    overwrite: bool = True


class PackageInstallRequest(BaseModel):
    package_name: str
    upgrade: bool = False


class RunExistingFileRequest(BaseModel):
    file_name: str
    variable_to_return: Optional[str] = None


class ExecutionResponse(BaseModel):
    success: bool
    result: Optional[str] = None
    error: Optional[str] = None
    execution_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    base_dir: str


# Global execution counter
execution_counter = 0


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "MCP Run Python Code API", "version": "0.0.2"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.0.2",
        "base_dir": app.state.base_dir
    }


@app.post("/execute", response_model=ExecutionResponse)
async def execute(request: CodeExecutionRequest):
    """Execute Python code"""
    global execution_counter
    execution_id = str(uuid.uuid4())
    execution_counter += 1

    try:
        logger.info(f"Executing code (ID: {execution_id}): {request.code[:100]}...")

        result = app.state.python_runner.run_python_code(
            request.code
        )
        logger.info(f"Execution result (ID: {execution_id}): {result}")
        return ExecutionResponse(
            success=True,
            result=result,
            execution_id=execution_id
        )
    except Exception as e:
        logger.error(f"Code execution failed (ID: {execution_id}): {e}")
        return ExecutionResponse(
            success=False,
            error=str(e),
            execution_id=execution_id
        )


@app.post("/save-and-execute", response_model=ExecutionResponse)
async def save_and_execute(request: FileExecutionRequest):
    """Save code to file and execute it"""
    global execution_counter
    execution_id = str(uuid.uuid4())
    execution_counter += 1

    try:
        logger.info(f"Saving and executing code (ID: {execution_id}): {request.file_name}")

        result = app.state.python_runner.save_to_file_and_run(
            request.file_name,
            request.code,
            request.variable_to_return,
            request.overwrite
        )

        return ExecutionResponse(
            success=True,
            result=result,
            execution_id=execution_id
        )
    except Exception as e:
        logger.error(f"Save and execute failed (ID: {execution_id}): {e}")
        return ExecutionResponse(
            success=False,
            error=str(e),
            execution_id=execution_id
        )


@app.post("/install-package", response_model=ExecutionResponse)
async def install_package(request: PackageInstallRequest):
    """Install Python package using pip"""
    global execution_counter
    execution_id = str(uuid.uuid4())
    execution_counter += 1

    try:
        logger.info(f"Installing package (ID: {execution_id}): {request.package_name}")

        result = app.state.python_runner.pip_install_package(request.package_name)

        return ExecutionResponse(
            success=True,
            result=result,
            execution_id=execution_id
        )
    except Exception as e:
        logger.error(f"Package installation failed (ID: {execution_id}): {e}")
        return ExecutionResponse(
            success=False,
            error=str(e),
            execution_id=execution_id
        )


@app.post("/run-python-file", response_model=ExecutionResponse)
async def run_python_file(request: RunExistingFileRequest):
    """Run an existing Python file"""
    global execution_counter
    execution_id = str(uuid.uuid4())
    execution_counter += 1

    try:
        logger.info(f"Running file (ID: {execution_id}): {request.file_name}")

        result = app.state.python_runner.run_python_file_return_variable(
            request.file_name,
            request.variable_to_return
        )

        return ExecutionResponse(
            success=True,
            result=result,
            execution_id=execution_id
        )
    except Exception as e:
        logger.error(f"File execution failed (ID: {execution_id}): {e}")
        return ExecutionResponse(
            success=False,
            error=str(e),
            execution_id=execution_id
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8083)
