"""
Sheikh AI Service - Enhanced with AI SDK Providers
Implements modern AI SDK integration with Google Generative AI and other providers
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import os

# AI SDK imports (these would be installed in requirements.txt)
try:
    import google.generativeai as genai
    from google.generativeai.types import file_types
    from google.generativeai import upload_file, get_file
    AI_SDK_AVAILABLE = True
except ImportError:
    AI_SDK_AVAILABLE = False
    logging.warning("Google Generative AI SDK not available. Install with: pip install google-generativeai")

# Setup logging
logger = logging.getLogger(__name__)

# Pydantic models for AI SDK requests
class AIRequest(BaseModel):
    prompt: str = Field(..., description="The prompt to send to the AI")
    provider: str = Field("google", description="AI provider to use")
    model: str = Field("gemini-3-pro-preview", description="Model to use")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens in response")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    thinking_level: Optional[str] = Field("medium", description="Thinking level for Gemini")
    enable_thinking: Optional[bool] = Field(True, description="Enable thinking process")
    enable_tools: Optional[bool] = Field(False, description="Enable tool calling")
    stream: Optional[bool] = Field(True, description="Enable streaming response")
    
class StreamingRequest(AIRequest):
    stream: bool = True

class FileAnalysisRequest(BaseModel):
    file_path: str = Field(..., description="Path to file for analysis")
    analysis_type: str = Field("general", description="Type of analysis")
    prompt: Optional[str] = Field(None, description="Additional prompt")

class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Code to analyze")
    language: str = Field("javascript", description="Programming language")
    analysis_type: str = Field("review", description="Type of analysis")
    context: Optional[str] = Field(None, description="Additional context")

class WebSearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    include_sources: Optional[bool] = Field(True, description="Include sources")
    use_grounding: Optional[bool] = Field(True, description="Use Google search grounding")
    top_k: Optional[int] = Field(5, description="Number of results")

class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Image generation prompt")
    aspect_ratio: str = Field("16:9", description="Image aspect ratio")
    model: str = Field("imagen-3.0-generate-002", description="Image generation model")

class MultiModalRequest(BaseModel):
    messages: List[Dict[str, Any]] = Field(..., description="Multi-modal conversation")
    include_images: Optional[bool] = Field(True, description="Include image responses")
    thinking_level: Optional[str] = Field("medium", description="Thinking level")

class StructuredOutputRequest(BaseModel):
    prompt: str = Field(..., description="Prompt for structured output")
    schema: Dict[str, Any] = Field(..., description="JSON schema for output")
    enable_structured: Optional[bool] = Field(True, description="Enable structured outputs")

# AI Service class
class SheikhAIService:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if AI_SDK_AVAILABLE and self.google_api_key:
            try:
                genai.configure(api_key=self.google_api_key)
                logger.info("Google Generative AI configured successfully")
            except Exception as e:
                logger.error(f"Failed to configure Google Generative AI: {e}")
        else:
            logger.warning("Google Generative AI API key not available")
    
    async def generate_text(self, request: AIRequest) -> Dict[str, Any]:
        """Generate text using AI SDK providers"""
        try:
            if request.provider == "google":
                return await self._generate_with_google(request)
            elif request.provider == "openai":
                return await self._generate_with_openai(request)
            else:
                raise ValueError(f"Unsupported provider: {request.provider}")
        except Exception as e:
            logger.error(f"Text generation error: {e}")
            raise HTTPException(status_code=500, detail=f"Text generation failed: {str(e)}")
    
    async def _generate_with_google(self, request: AIRequest) -> Dict[str, Any]:
        """Generate text using Google Generative AI"""
        if not AI_SDK_AVAILABLE:
            raise HTTPException(status_code=503, detail="Google Generative AI SDK not available")
        
        try:
            model = genai.GenerativeModel(request.model)
            
            # Configure generation parameters
            generation_config = {
                "temperature": request.temperature,
                "top_p": 0.8,
                "top_k": 40,
            }
            
            if request.max_tokens:
                generation_config["max_output_tokens"] = request.max_tokens
            
            # Configure safety settings
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_HIGH"
                }
            ]
            
            # Configure thinking for Gemini models
            tools = []
            if request.enable_tools:
                tools.append(genai.protos.Tool(
                    google_search=genai.protos.GoogleSearchTool()
                ))
                if request.enable_thinking:
                    generation_config["tools"] = tools
                    generation_config["tool_config"] = {
                        "function_calling_config": {
                            "mode": "ANY",
                            "allowed_function_names": ["google_search"]
                        }
                    }
            
            # Generate response
            response = model.generate_content(
                request.prompt,
                generation_config=genai.protos.GenerationConfig(**generation_config),
                safety_settings=safety_settings
            )
            
            return {
                "success": True,
                "text": response.text,
                "provider": "google",
                "model": request.model,
                "usage": getattr(response, 'usage_metadata', {}),
                "safety_ratings": getattr(response, 'safety_ratings', [])
            }
            
        except Exception as e:
            logger.error(f"Google AI generation error: {e}")
            raise HTTPException(status_code=500, detail=f"Google AI generation failed: {str(e)}")
    
    async def _generate_with_openai(self, request: AIRequest) -> Dict[str, Any]:
        """Generate text using OpenAI (placeholder implementation)"""
        # This would require the OpenAI Python client
        raise HTTPException(status_code=503, detail="OpenAI provider not yet implemented")
    
    async def analyze_file(self, request: FileAnalysisRequest) -> Dict[str, Any]:
        """Analyze files using multi-modal AI"""
        try:
            if not AI_SDK_AVAILABLE:
                raise HTTPException(status_code=503, detail="File analysis requires Google Generative AI SDK")
            
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Upload file
            uploaded_file = upload_file(request.file_path)
            
            # Analyze file
            prompt = f"Analyze this {request.analysis_type}: {request.prompt or 'Provide a comprehensive analysis'}"
            
            response = model.generate_content([prompt, uploaded_file])
            
            return {
                "success": True,
                "analysis": response.text,
                "file_path": request.file_path,
                "analysis_type": request.analysis_type,
                "provider": "google",
                "model": "gemini-1.5-flash"
            }
            
        except Exception as e:
            logger.error(f"File analysis error: {e}")
            raise HTTPException(status_code=500, detail=f"File analysis failed: {str(e)}")
    
    async def analyze_code(self, request: CodeAnalysisRequest) -> Dict[str, Any]:
        """Analyze code with advanced reasoning"""
        try:
            model = genai.GenerativeModel('gemini-3-pro-preview')
            
            analysis_prompt = f"""
            Analyze this {request.language} code:
            
            ```{request.language}
            {request.code}
            ```
            
            Analysis type: {request.analysis_type}
            {f"Context: {request.context}" if request.context else ""}
            
            Provide:
            1. Code explanation
            2. Potential improvements
            3. Best practices
            4. Security considerations
            5. Performance optimizations
            """
            
            response = model.generate_content(analysis_prompt)
            
            return {
                "success": True,
                "analysis": response.text,
                "code": request.code,
                "language": request.language,
                "analysis_type": request.analysis_type,
                "provider": "google",
                "model": "gemini-3-pro-preview"
            }
            
        except Exception as e:
            logger.error(f"Code analysis error: {e}")
            raise HTTPException(status_code=500, detail=f"Code analysis failed: {str(e)}")
    
    async def web_search(self, request: WebSearchRequest) -> Dict[str, Any]:
        """Perform web search with grounding"""
        try:
            if not AI_SDK_AVAILABLE:
                raise HTTPException(status_code=503, detail="Web search requires Google Generative AI SDK")
            
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            tools = []
            if request.use_grounding:
                tools.append(genai.protos.Tool(
                    google_search=genai.protos.GoogleSearchTool()
                ))
            
            response = model.generate_content(
                request.query,
                tools=tools if tools else None
            )
            
            return {
                "success": True,
                "answer": response.text,
                "query": request.query,
                "sources": getattr(response, 'grounding_metadata', {}),
                "provider": "google",
                "model": "gemini-1.5-flash"
            }
            
        except Exception as e:
            logger.error(f"Web search error: {e}")
            raise HTTPException(status_code=500, detail=f"Web search failed: {str(e)}")
    
    async def generate_image(self, request: ImageGenerationRequest) -> Dict[str, Any]:
        """Generate images using Imagen"""
        try:
            if not AI_SDK_AVAILABLE:
                raise HTTPException(status_code=503, detail="Image generation requires Google Generative AI SDK")
            
            model = genai.GenerativeModel('imagen-3.0-generate-002')
            
            response = model.generate_content(request.prompt)
            
            # Handle image generation (this would need to be implemented based on Imagen API)
            return {
                "success": True,
                "image_url": "placeholder_image_url",  # Would be actual image URL
                "prompt": request.prompt,
                "aspect_ratio": request.aspect_ratio,
                "provider": "google",
                "model": request.model
            }
            
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")
    
    async def multi_modal_chat(self, request: MultiModalRequest) -> Dict[str, Any]:
        """Handle multi-modal conversations"""
        try:
            model = genai.GenerativeModel('gemini-3-pro-preview')
            
            # Process messages
            content_parts = []
            for message in request.messages:
                if message['role'] == 'user':
                    if isinstance(message['content'], str):
                        content_parts.append(message['content'])
                    elif isinstance(message['content'], list):
                        for part in message['content']:
                            if part['type'] == 'text':
                                content_parts.append(part['text'])
                            elif part['type'] == 'file':
                                # Handle file uploads
                                pass
            
            response = model.generate_content(content_parts)
            
            return {
                "success": True,
                "response": response.text,
                "messages": request.messages,
                "provider": "google",
                "model": "gemini-3-pro-preview"
            }
            
        except Exception as e:
            logger.error(f"Multi-modal chat error: {e}")
            raise HTTPException(status_code=500, detail=f"Multi-modal chat failed: {str(e)}")

# Create service instance
ai_service = SheikhAIService()

# Create router
router = APIRouter(prefix="/ai", tags=["AI SDK Integration"])

# Routes
@router.post("/generate")
async def generate_text_endpoint(request: AIRequest):
    """Generate text using AI SDK providers"""
    result = await ai_service.generate_text(request)
    return result

@router.post("/analyze-file")
async def analyze_file_endpoint(request: FileAnalysisRequest):
    """Analyze files using AI SDK"""
    result = await ai_service.analyze_file(request)
    return result

@router.post("/analyze-code")
async def analyze_code_endpoint(request: CodeAnalysisRequest):
    """Analyze code with AI SDK"""
    result = await ai_service.analyze_code(request)
    return result

@router.post("/web-search")
async def web_search_endpoint(request: WebSearchRequest):
    """Perform web search with AI SDK"""
    result = await ai_service.web_search(request)
    return result

@router.post("/generate-image")
async def generate_image_endpoint(request: ImageGenerationRequest):
    """Generate images using AI SDK"""
    result = await ai_service.generate_image(request)
    return result

@router.post("/multi-modal")
async def multi_modal_endpoint(request: MultiModalRequest):
    """Handle multi-modal conversations with AI SDK"""
    result = await ai_service.multi_modal_chat(request)
    return result

@router.get("/models")
async def list_models():
    """List available AI models"""
    models = {
        "google": [
            "gemini-3-pro-preview",
            "gemini-2.5-flash", 
            "gemini-1.5-pro",
            "imagen-3.0-generate-002"
        ],
        "openai": [
            "gpt-4",
            "gpt-3.5-turbo",
            "gpt-4-turbo-preview"
        ]
    }
    return {"models": models}

@router.get("/providers")
async def list_providers():
    """List available AI providers"""
    providers = {
        "google": {
            "name": "Google Generative AI",
            "models": 4,
            "features": ["text", "image", "multi-modal", "tools", "thinking"]
        },
        "openai": {
            "name": "OpenAI",
            "models": 3,
            "features": ["text", "function-calling"]
        }
    }
    return {"providers": providers}

@router.get("/health")
async def ai_health_check():
    """Health check for AI SDK services"""
    status = {
        "google": AI_SDK_AVAILABLE and bool(ai_service.google_api_key),
        "openai": bool(ai_service.openai_api_key),
        "overall": AI_SDK_AVAILABLE
    }
    return {"status": status}