"""
API v1 routers for the Sheikh conversation system
"""

from fastapi import APIRouter, HTTPException, Depends, WebSocket, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Dict, Any, Optional, List
import json
import asyncio
from datetime import datetime

from ...application.services import (
    ConversationApplicationService, ShellApplicationService, FileApplicationService
)
from ...application.command_handlers import (
    CreateSessionCommand, DeleteSessionCommand, StopSessionCommand,
    SendMessageCommand, ExecuteShellCommandCommand, ReadFileCommand
)
from ...application.query_handlers import (
    GetSessionQuery, ListSessionsQuery, GetSessionHistoryQuery
)
from ...infrastructure.services import (
    ConversationRepositoryService, ShellToolService, SSEStreamingService,
    EventManagementService, FileConversationRepository
)


def get_conversation_service() -> ConversationApplicationService:
    """Dependency injection for conversation service"""
    repository = FileConversationRepository()
    domain_service = ConversationRepositoryService(repository)
    tool_service = ShellToolService()
    event_service = EventManagementService()
    
    return ConversationApplicationService(domain_service, tool_service, event_service)


def get_shell_service() -> ShellApplicationService:
    """Dependency injection for shell service"""
    repository = FileConversationRepository()
    domain_service = ConversationRepositoryService(repository)
    tool_service = ShellToolService()
    
    return ShellApplicationService(domain_service, tool_service)


def get_file_service() -> FileApplicationService:
    """Dependency injection for file service"""
    repository = FileConversationRepository()
    domain_service = ConversationRepositoryService(repository)
    tool_service = ShellToolService()
    
    return FileApplicationService(domain_service, tool_service)


# Create router
router = APIRouter()


@router.put("/sessions")
async def create_session(
    conversation_service: ConversationApplicationService = Depends(get_conversation_service)
) -> Dict[str, Any]:
    """Create a new conversation session"""
    result = await conversation_service.create_session()
    return result


@router.get("/sessions/{session_id}")
async def get_session(
    session_id: str,
    conversation_service: ConversationApplicationService = Depends(get_conversation_service)
) -> Dict[str, Any]:
    """Get session information including conversation history"""
    return await conversation_service.get_session(session_id)


@router.get("/sessions")
async def list_sessions(
    conversation_service: ConversationApplicationService = Depends(get_conversation_service)
) -> Dict[str, Any]:
    """Get list of all sessions"""
    return await conversation_service.list_sessions()


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    conversation_service: ConversationApplicationService = Depends(get_conversation_service)
) -> Dict[str, Any]:
    """Delete a session"""
    return await conversation_service.delete_session(session_id)


@router.post("/sessions/{session_id}/stop")
async def stop_session(
    session_id: str,
    conversation_service: ConversationApplicationService = Depends(get_conversation_service)
) -> Dict[str, Any]:
    """Stop an active session"""
    return await conversation_service.stop_session(session_id)


@router.post("/sessions/{session_id}/chat")
async def chat_with_session(
    session_id: str,
    request: Dict[str, Any],
    background_tasks: BackgroundTasks,
    conversation_service: ConversationApplicationService = Depends(get_conversation_service)
):
    """Send a message to the session and receive streaming response"""
    
    # Extract request data
    message = request.get("message", "")
    timestamp = request.get("timestamp", int(datetime.utcnow().timestamp()))
    event_id = request.get("event_id")
    
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    async def generate_stream():
        """Generate SSE stream for chat response"""
        try:
            # Process the message
            result = await conversation_service.process_chat_message(
                session_id, message, timestamp, event_id
            )
            
            if result["code"] != 0:
                yield f"event: error\ndata: {json.dumps(result)}\n\n"
                return
            
            # Stream initial response
            response = result["data"]["response"]
            yield f"event: message\ndata: {json.dumps({'content': response})}\n\n"
            
            # Send completion event
            yield f"event: done\ndata: {json.dumps({'completed': True})}\n\n"
            
        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.post("/sessions/{session_id}/shell")
async def view_shell_session(
    session_id: str,
    request: Dict[str, Any],
    shell_service: ShellApplicationService = Depends(get_shell_service)
) -> Dict[str, Any]:
    """View shell session output in the sandbox environment"""
    shell_session_id = request.get("shell_session_id", "")
    
    if not shell_session_id:
        raise HTTPException(status_code=400, detail="shell_session_id is required")
    
    return await shell_service.view_shell_session(session_id, shell_session_id)


@router.post("/sessions/{session_id}/file")
async def view_file_content(
    session_id: str,
    request: Dict[str, Any],
    file_service: FileApplicationService = Depends(get_file_service)
) -> Dict[str, Any]:
    """View file content in the sandbox environment"""
    file_path = request.get("file", "")
    
    if not file_path:
        raise HTTPException(status_code=400, detail="file path is required")
    
    return await file_service.view_file_content(session_id, file_path)


@router.websocket("/sessions/{session_id}/vnc")
async def vnc_websocket(
    session_id: str,
    websocket: WebSocket
):
    """Establish VNC WebSocket connection to session's sandbox environment"""
    await websocket.accept(subprotocol="binary")
    
    try:
        # Simulate VNC connection
        # In a real implementation, this would:
        # 1. Create or connect to a Docker container
        # 2. Start VNC server in the container
        # 3. Forward VNC traffic through WebSocket
        
        # Send welcome message
        await websocket.send_text(json.dumps({
            "type": "welcome",
            "session_id": session_id,
            "message": "VNC connection established"
        }))
        
        # Keep connection alive and handle VNC traffic
        while True:
            # Receive data from WebSocket
            data = await websocket.receive()
            
            # Handle different message types
            if isinstance(data, dict) and "bytes" in data:
                # Binary VNC data
                binary_data = data["bytes"]
                # Process VNC protocol data here
                # Send response back
                await websocket.send_bytes(binary_data)
            elif isinstance(data, dict) and "text" in data:
                # Text messages (commands, queries, etc.)
                text_data = json.loads(data["text"])
                await websocket.send_text(json.dumps({
                    "type": "ack",
                    "data": text_data
                }))
    
    except Exception as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))
        await websocket.close()