from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from src.core.config import settings
from src.core.logger import setup_logging, logger
from src.interfaces.v1.explain import semgrep, gitleaks
from src.interfaces import system
import time
import uuid

# Setup Logging
setup_logging()

# Initialize App
app = FastAPI(
    title=settings.APP_NAME,
    docs_url="/doc" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    openapi_url="/openapi.json" if settings.ENVIRONMENT == "development" else None,
)

# Middleware for Logging and Correlation IDs
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    logger.info(
        "Request processed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": process_time,
            "request_id": request_id
        }
    )
    
    response.headers["X-Request-ID"] = request_id
    return response

# Health Checks
@app.get("/health/live")
async def liveness():
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness():
    return {"status": "ready"}

@app.get("/health/startup")
async def startup():
    return {"status": "started"}

# Routes
app.include_router(semgrep.router, prefix="/v1/explain", tags=["Semgrep"])
app.include_router(gitleaks.router, prefix="/v1/explain", tags=["Gitleaks"])
app.include_router(system.router, tags=["System"])

# Metrics
Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
