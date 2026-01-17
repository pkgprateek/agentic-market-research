from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, research, export
from app.core.config import settings

app = FastAPI(
    title="Agentic Market Research API",
    description="Enterprise-grade AI-powered competitive intelligence",
    version="0.1.0",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(research.router, prefix="/api", tags=["research"])
app.include_router(export.router, prefix="/api", tags=["export"])
