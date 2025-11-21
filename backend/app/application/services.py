"""
Application services for the Sheikh conversation system
"""

from typing import List, Optional, Dict, Any, AsyncGenerator
import uuid
import json
import asyncio
from datetime import datetime

from ..domain.entities import ConversationSession, Message, ShellSession, FileOperation
from ..domain.value_objects import (
    ConversationId, MessageId, Content, Role, Timestamp, Status
)
from ..domain.services import (
    ConversationDomainService, ToolExecutionService, 
    StreamingService, EventService
)
from ..domain.events import (
    SessionCreatedEvent, MessageReceivedEvent, MessageSentEvent,
    ToolInvokedEvent, ShellCommandExecutedEvent, FileOperationEvent,
    SessionStatusChangedEvent, ErrorEvent
)


class ConversationApplicationService:
    """Application service for conversation management"""
    
    def __init__(
        self,
        conversation_service: ConversationDomainService,
        tool_service: ToolExecutionService,
        event_service: EventService
    ):
        self.conversation_service = conversation_service
        self.tool_service = tool_service
        self.event_service = event_service
    
    async def create_session(self, title: str = "New Conversation") -> Dict[str, Any]:
        """Create a new conversation session"""
        try:
            session = await self.conversation_service.create_session(title)
            
            # Fire domain event
            await self.event_service.create_event(
                session, "session_created", {"title": title}
            )
            
            return {
                "code": 0,
                "msg": "success",
                "data": {
                    "session_id": session.session_id.value
                }
            }
        except Exception as e:
            return {
                "code": 500,
                "msg": f"Failed to create session: {str(e)}",
                "data": None
            }
    
    async def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get session information including conversation history"""
        try:
            conversation_id = ConversationId(session_id)
            session = await self.conversation_service.get_session(conversation_id)
            
            if not session:
                return {
                    "code": 404,
                    "msg": "Session not found",
                    "data": None
                }
            
            return {
                "code": 0,
                "msg": "success",
                "data": {
                    "session_id": session.session_id.value,
                    "title": session.title,
                    "events": [
                        {
                            "event_id": event.event_id,
                            "event_type": event.event_type,
                            "data": event.data,
                            "timestamp": event.timestamp.isoformat()
                        }
                        for event in session.events
                    ]
                }
            }
        except Exception as e:
            return {
                "code": 500,
                "msg": f"Failed to get session: {str(e)}",
                "data": None
            }
    
    async def list_sessions(self) -> Dict[str, Any]:
        """Get list of all sessions"""
        try:
            sessions = await self.conversation_service.list_sessions()
            
            session_list = []
            for session in sessions:
                latest_message = ""
                latest_message_at = 0
                
                if session.messages:
                    latest_msg = session.messages[-1]
                    latest_message = latest_msg.content.value
                    latest_message_at = int(latest_msg.timestamp.value.timestamp())
                
                session_list.append({
                    "session_id": session.session_id.value,
                    "title": session.title,
                    "latest_message": latest_message,
                    "latest_message_at": latest_message_at,
                    "status": session.status.value,
                    "unread_message_count": session.unread_message_count
                })
            
            return {
                "code": 0,
                "msg": "success",
                "data": {
                    "sessions": session_list
                }
            }
        except Exception as e:
            return {
                "code": 500,
                "msg": f"Failed to list sessions: {str(e)}",
                "data": None
            }
    
    async def delete_session(self, session_id: str) -> Dict[str, Any]:
        """Delete a conversation session"""
        try:
            conversation_id = ConversationId(session_id)
            success = await self.conversation_service.delete_session(conversation_id)
            
            if not success:
                return {
                    "code": 404,
                    "msg": "Session not found",
                    "data": None
                }
            
            return {
                "code": 0,
                "msg": "success",
                "data": None
            }
        except Exception as e:
            return {
                "code": 500,
                "msg": f"Failed to delete session: {str(e)}",
                "data": None
            }
    
    async def stop_session(self, session_id: str) -> Dict[str, Any]:
        """Stop an active session"""
        try:
            conversation_id = ConversationId(session_id)
            session = await self.conversation_service.get_session(conversation_id)
            
            if not session:
                return {
                    "code": 404,
                    "msg": "Session not found",
                    "data": None
                }
            
            # Update status
            session.update_status("stopped")
            
            return {
                "code": 0,
                "msg": "success",
                "data": None
            }
        except Exception as e:
            return {
                "code": 500,
                "msg": f"Failed to stop session: {str(e)}",
                "data": None
            }
    
    async def process_chat_message(self, session_id: str, message: str, timestamp: int, event_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a chat message and return response"""
        try:
            conversation_id = ConversationId(session_id)
            session = await self.conversation_service.get_session(conversation_id)
            
            if not session:
                return {
                    "code": 404,
                    "msg": "Session not found",
                    "data": None
                }
            
            # Add user message
            user_message = session.add_message("user", message)
            
            # Fire event
            await self.event_service.create_event(
                session, "message_received", {
                    "message": message,
                    "timestamp": timestamp,
                    "event_id": event_id
                }
            )
            
            # Simulate AI processing (in real implementation, this would call OpenAI)
            response = await self._generate_ai_response(session, message)
            
            # Add assistant message
            assistant_message = session.add_message("assistant", response)
            
            return {
                "code": 0,
                "msg": "success",
                "data": {
                    "response": response,
                    "message_id": assistant_message.message_id.value
                }
            }
        except Exception as e:
            return {
                "code": 500,
                "msg": f"Failed to process chat: {str(e)}",
                "data": None
            }
    
    async def _generate_ai_response(self, session: ConversationSession, user_message: str) -> str:
        """Generate AI response (placeholder for OpenAI integration)"""
        # This would integrate with OpenAI API
        return f"I understand you said: '{user_message}'. How can I help you with tools like shell commands, file operations, or browser automation?"


class ShellApplicationService:
    """Application service for shell operations"""
    
    def __init__(self, conversation_service: ConversationDomainService, tool_service: ToolExecutionService):
        self.conversation_service = conversation_service
        self.tool_service = tool_service
    
    async def view_shell_session(self, session_id: str, shell_session_id: str) -> Dict[str, Any]:
        """View shell session output"""
        try:
            conversation_id = ConversationId(session_id)
            session = await self.conversation_service.get_session(conversation_id)
            
            if not session:
                return {
                    "code": 404,
                    "msg": "Session not found",
                    "data": None
                }
            
            # Find shell session
            shell_session = None
            for shell in session.shell_sessions:
                if shell.shell_session_id == shell_session_id:
                    shell_session = shell
                    break
            
            if not shell_session:
                return {
                    "code": 404,
                    "msg": "Shell session not found",
                    "data": None
                }
            
            return {
                "code": 0,
                "msg": "success",
                "data": {
                    "output": shell_session.get_latest_output(),
                    "session_id": shell_session.shell_session_id,
                    "console": shell_session.console
                }
            }
        except Exception as e:
            return {
                "code": 500,
                "msg": f"Failed to view shell session: {str(e)}",
                "data": None
            }


class FileApplicationService:
    """Application service for file operations"""
    
    def __init__(self, conversation_service: ConversationDomainService, tool_service: ToolExecutionService):
        self.conversation_service = conversation_service
        self.tool_service = tool_service
    
    async def view_file_content(self, session_id: str, file_path: str) -> Dict[str, Any]:
        """View file content in sandbox environment"""
        try:
            conversation_id = ConversationId(session_id)
            session = await self.conversation_service.get_session(conversation_id)
            
            if not session:
                return {
                    "code": 404,
                    "msg": "Session not found",
                    "data": None
                }
            
            # Use tool service to read file
            result = await self.tool_service.read_file(session, file_path)
            
            return {
                "code": 0,
                "msg": "success",
                "data": {
                    "content": result.get("content", ""),
                    "file": file_path
                }
            }
        except Exception as e:
            return {
                "code": 500,
                "msg": f"Failed to view file: {str(e)}",
                "data": None
            }