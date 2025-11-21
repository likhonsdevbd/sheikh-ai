"""
Sheikh Backend - FastAPI Application
Main entry point for the intelligent conversation agent system
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from .routers import conversations, files, shell, browser
from .dependencies import get_conversation_service, get_file_service
from ...infrastructure.config import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    print("🚀 Starting Sheikh Backend...")
    yield
    # Shutdown
    print("🛑 Shutting down Sheikh Backend...")


# Create FastAPI application
app = FastAPI(
    title="Sheikh Intelligent Conversation Agent",
    description="Advanced conversation agent with file operations, shell execution, and browser automation",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.sheikh.ai"]
)

# Include routers
app.include_router(
    conversations.router,
    prefix="/api/conversations",
    tags=["conversations"]
)

app.include_router(
    files.router,
    prefix="/api/files",
    tags=["files"]
)

app.include_router(
    shell.router,
    prefix="/api/shell",
    tags=["shell"]
)

app.include_router(
    browser.router,
    prefix="/api/browser",
    tags=["browser"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sheikh Intelligent Conversation Agent API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "sheikh-backend",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    
    settings = Settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )