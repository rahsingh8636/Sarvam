import os
import time
import random
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get version from environment variable
APP_VERSION = os.getenv("APP_VERSION", "v1.0.0")
APP_NAME = os.getenv("APP_NAME", "canary-demo")

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')
ERROR_COUNT = Counter('http_errors_total', 'Total HTTP errors', ['method', 'endpoint', 'status'])

app = FastAPI(
    title=f"{APP_NAME} Canary Demo",
    description="A FastAPI application for demonstrating canary deployments",
    version=APP_VERSION
)

# Version-specific responses
VERSION_RESPONSES = {
    "v1.0.0": {
        "message": "Hello from Canary Demo v1!",
        "features": ["Basic functionality", "Health checks", "Metrics"],
        "color": "blue",
        "timestamp": None
    },
    "v2.0.0": {
        "message": "Hello from Canary Demo v2!",
        "features": ["Enhanced functionality", "Advanced metrics", "Better performance"],
        "color": "green",
        "timestamp": None
    }
}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Record metrics
    REQUEST_LATENCY.observe(process_time)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    if response.status_code >= 400:
        ERROR_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
    
    return response

@app.get("/")
async def root():
    """Main endpoint that returns version-specific information"""
    response_data = VERSION_RESPONSES.get(APP_VERSION, VERSION_RESPONSES["v1.0.0"]).copy()
    response_data["timestamp"] = datetime.utcnow().isoformat()
    response_data["version"] = APP_VERSION
    response_data["pod_name"] = os.getenv("HOSTNAME", "unknown")
    
    logger.info(f"Serving request from version {APP_VERSION}")
    return response_data

@app.get("/health")
async def health_check():
    """Health check endpoint for Kubernetes probes"""
    return {
        "status": "healthy",
        "version": APP_VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "pod_name": os.getenv("HOSTNAME", "unknown")
    }

@app.get("/version")
async def version_info():
    """Get detailed version information"""
    return {
        "version": APP_VERSION,
        "app_name": APP_NAME,
        "pod_name": os.getenv("HOSTNAME", "unknown"),
        "deployment_time": datetime.utcnow().isoformat()
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return JSONResponse(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.post("/simulate-error")
async def simulate_error(error_rate: float = 0.5):
    """Simulate errors for testing canary rollback scenarios"""
    if random.random() < error_rate:
        logger.error(f"Simulating error in version {APP_VERSION}")
        raise HTTPException(status_code=500, detail="Simulated error for testing")
    
    return {
        "message": "No error simulated",
        "version": APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/status")
async def status():
    """Detailed status endpoint for monitoring"""
    return {
        "status": "running",
        "version": APP_VERSION,
        "app_name": APP_NAME,
        "pod_name": os.getenv("HOSTNAME", "unknown"),
        "uptime": time.time(),
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 