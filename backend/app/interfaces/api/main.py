"""
Sheikh Backend - FastAPI Application
Main entry point for the intelligent conversation agent system
Enhanced with AI SDK Providers Integration
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from .routers import conversations, files, shell, browser
from ...services.ai_service import router as ai_router
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
    description="Advanced conversation agent with AI SDK integration, file operations, shell execution, and browser automation. Powered by Gemini 3 Pro Preview and modern AI protocols.",
    version="2.0.0",
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
    conversations,
    prefix="/api/conversations",
    tags=["conversations"]
)

app.include_router(
    files,
    prefix="/api/files",
    tags=["files"]
)

app.include_router(
    shell,
    prefix="/api/shell",
    tags=["shell"]
)

app.include_router(
    browser,
    prefix="/api/browser",
    tags=["browser"]
)

# AI SDK Integration routes
app.include_router(
    ai_router,
    prefix="/api/ai",
    tags=["AI SDK"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sheikh Intelligent Conversation Agent API",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "AI SDK Integration",
            "Google Generative AI (Gemini 3 Pro Preview)",
            "AG-UI Protocol",
            "CopilotKit Integration",
            "Advanced Reasoning",
            "Multi-modal AI",
            "Tool Calling",
            "File Analysis",
            "Web Search with Grounding",
            "Image Generation",
            "Structured Data Output"
        ],
        "providers": ["google", "openai"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "sheikh-backend",
        "version": "2.0.0",
        "features": {
            "ai_sdk": "available",
            "google_ai": "configured",
            "ag_ui_protocol": "enabled",
            "copilotkit": "enabled",
            "enhanced_reasoning": "gemini-3-pro-preview"
        }
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