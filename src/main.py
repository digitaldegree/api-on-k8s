import os
import platform
import socket
import uuid
from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import FastAPI

app = FastAPI(
    title="System Info API",
    description="A simple API that returns system information including hostname",
    version="1.0.0",
)


@app.get("/", response_model=Dict[str, Any])
async def get_system_info():
    """
    Get system information including hostname and compute layer details.
    """
    return {
        "hostname": os.environ.get("HOSTNAME", socket.gethostname()),
        "pod_name": os.environ.get("POD_NAME", "unknown"),
        "pod_ip": os.environ.get("POD_IP", "127.0.0.1"),
        "node_name": os.environ.get("NODE_NAME", "unknown"),
        "instance_id": str(uuid.uuid4())[
            :8
        ],  # Short unique ID for this container instance
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
