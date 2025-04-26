from datetime import datetime
from fastapi import FastAPI, Response
import uvicorn
import logging
from contextlib import asynccontextmanager

from app.core.logging import setup_logging
from app.core.middleware import setup_middleware
from app.core.tracing import setup_tracing

# Setup logging with explicit console output
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 Application startup complete")
    yield
    logger.info("🛑 Application shutdown initiated")


"""Create and configure the FastAPI application"""
app = FastAPI(
    title="E-Commerce API with Monitoring",
    description="FastAPI application with Prometheus and Loki integration",
    version="1.0.0",
    lifespan=lifespan,
)

# Import routers after creating the app to avoid circular imports
from app.api.routes.query import router as query_router
from app.api.routes.product import router as product_router
from app.api.routes.monitoring import router as monitoring_router

# Configure middleware and tracing
setup_middleware(app)
setup_tracing(app)

# Add other routers
app.include_router(query_router)
app.include_router(product_router)
app.include_router(monitoring_router, tags=["Monitoring"])

@app.get("/")
def get_home() -> Response:
    """
    Return server status
    """
    logger.info("🏠 Home endpoint accessed")
    return Response("Server is running")

if __name__ == "__main__":
    # Try both logger and print to compare
    print("🔥 Launching FastAPI app using print...")
    logger.info("🔥 Launching FastAPI app using logger...")
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        # Add these to prevent Uvicorn from taking over logging
        log_config=None,
        access_log=False
    )