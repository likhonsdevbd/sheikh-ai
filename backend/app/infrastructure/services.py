"""
Infrastructure layer implementation for the Sheikh conversation system
"""

import os
import json
import aiofiles
import asyncio
from typing import Dict, List, Optional, Any, AsyncGenerator
from pathlib import Path
from datetime import datetime

from ..domain.entities import ConversationSession, Message, ShellSession, FileOperation
from ..domain.value_objects import ConversationId, Status, Command
from ..domain.services import (
    ConversationDomainService, ToolExecutionService, 
    StreamingService, EventService
)
from .config import Settings


class FileConversationRepository:
    """File-based repository for conversation persistence"""
    
    def __init__(self, data_directory: str = "./data"):
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(exist_ok=True)
        
        # Session storage file
        self.sessions_file = self.data_directory / "sessions.json"
        self._ensure_sessions_file()
    
    def _ensure_sessions_file(self):
        """Ensure sessions file exists and has valid structure"""
        if not self.sessions_file.exists():
            with open(self.sessions_file, 'w') as f:
                json.dump({}, f)
    
    async def save_session(self, session: ConversationSession) -> None:
        """Save session to file"""
        sessions = await self._load_all_sessions()
        sessions[session.session_id.value] = {
            "session_id": session.session_id.value,
            "title": session.title,
            "status": session.status.value,
            "messages": [
                {
                    "message_id": msg.message_id.value,
                    "role": msg.role.value,
                    "content": msg.content.value,
                    "timestamp": msg.timestamp.value.isoformat(),
                    "metadata": msg.metadata
                }
                for msg in session.messages
            ],
            "events": [
                {
                    "event_id": event.event_id,
                    "event_type": event.event_type,
                    "data": event.data,
                    "timestamp": event.timestamp.value.isoformat()
                }
                for event in session.events
            ],
            "shell_sessions": [
                {
                    "shell_session_id": shell.shell_session_id,
                    "console": shell.console,
                    "created_at": shell.created_at.value.isoformat(),
                    "last_updated": shell.last_updated.value.isoformat()
                }
                for shell in session.shell_sessions
            ],
            "file_operations": [
                {
                    "file_path": file_op.file_path.value,
                    "operation_type": file_op.operation_type,
                    "content": file_op.content,
                    "timestamp": file_op.timestamp.value.isoformat()
                }
                for file_op in session.file_operations
            ],
            "created_at": session.created_at.value.isoformat(),
            "last_updated": session.last_updated.value.isoformat(),
            "unread_message_count": session.unread_message_count
        }
        
        async with aiofiles.open(self.sessions_file, 'w') as f:
            await f.write(json.dumps(sessions, indent=2))
    
    async def load_session(self, session_id: ConversationId) -> Optional[ConversationSession]:
        """Load session from file"""
        sessions = await self._load_all_sessions()
        
        if session_id.value not in sessions:
            return None
        
        data = sessions[session_id.value]
        
        # Reconstruct session
        session = ConversationSession(
            session_id=ConversationId(data["session_id"]),
            title=data["title"],
            status=Status(data["status"]),
            unread_message_count=data["unread_message_count"]
        )
        
        # Reconstruct messages
        for msg_data in data.get("messages", []):
            from ..domain.entities import Message
            from ..domain.value_objects import Role, Content, Timestamp
            
            message = Message(
                message_id=msg_data["message_id"],
                conversation_id=session.session_id,
                role=Role(msg_data["role"]),
                content=Content(msg_data["content"]),
                timestamp=Timestamp(datetime.fromisoformat(msg_data["timestamp"])),
                metadata=msg_data.get("metadata", {})
            )
            session.messages.append(message)
        
        # Reconstruct events
        from ..domain.entities import Event
        for event_data in data.get("events", []):
            event = Event(
                event_id=event_data["event_id"],
                session_id=session.session_id,
                event_type=event_data["event_type"],
                data=event_data["data"],
                timestamp=Timestamp(datetime.fromisoformat(event_data["timestamp"]))
            )
            session.events.append(event)
        
        # Reconstruct shell sessions
        for shell_data in data.get("shell_sessions", []):
            shell_session = ShellSession(
                shell_session_id=shell_data["shell_session_id"],
                conversation_id=session.session_id,
                created_at=Timestamp(datetime.fromisoformat(shell_data["created_at"])),
                last_updated=Timestamp(datetime.fromisoformat(shell_data["last_updated"]))
            )
            shell_session.console = shell_data.get("console", [])
            session.shell_sessions.append(shell_session)
        
        return session
    
    async def delete_session(self, session_id: ConversationId) -> bool:
        """Delete session from file"""
        sessions = await self._load_all_sessions()
        
        if session_id.value not in sessions:
            return False
        
        del sessions[session_id.value]
        
        async with aiofiles.open(self.sessions_file, 'w') as f:
            await f.write(json.dumps(sessions, indent=2))
        
        return True
    
    async def list_sessions(self) -> List[ConversationSession]:
        """List all sessions"""
        sessions_data = await self._load_all_sessions()
        sessions = []
        
        for session_data in sessions_data.values():
            session = await self.load_session(ConversationId(session_data["session_id"]))
            if session:
                sessions.append(session)
        
        return sessions
    
    async def _load_all_sessions(self) -> Dict[str, Any]:
        """Load all sessions from file"""
        async with aiofiles.open(self.sessions_file, 'r') as f:
            content = await f.read()
            return json.loads(content) if content else {}


class ConversationRepositoryService(ConversationDomainService):
    """Conversation domain service with file repository"""
    
    def __init__(self, repository: FileConversationRepository):
        self.repository = repository
        self._sessions_cache = {}
    
    async def create_session(self, title: str) -> ConversationSession:
        """Create a new conversation session"""
        session = ConversationSession(
            session_id=ConversationId.generate(),
            title=title,
            status=Status("pending")
        )
        
        await self.repository.save_session(session)
        return session
    
    async def get_session(self, session_id: ConversationId) -> Optional[ConversationSession]:
        """Get a conversation session by ID"""
        # Try cache first
        if session_id.value in self._sessions_cache:
            return self._sessions_cache[session_id.value]
        
        session = await self.repository.load_session(session_id)
        if session:
            self._sessions_cache[session_id.value] = session
        
        return session
    
    async def list_sessions(self) -> List[ConversationSession]:
        """List all conversation sessions"""
        return await self.repository.list_sessions()
    
    async def delete_session(self, session_id: ConversationId) -> bool:
        """Delete a conversation session"""
        # Remove from cache
        if session_id.value in self._sessions_cache:
            del self._sessions_cache[session_id.value]
        
        return await self.repository.delete_session(session_id)
    
    async def stop_session(self, session_id: ConversationId) -> bool:
        """Stop an active conversation session"""
        session = await self.get_session(session_id)
        if session:
            session.update_status("stopped")
            await self.repository.save_session(session)
            self._sessions_cache[session_id.value] = session
            return True
        return False


class OpenAIIntegrationService:
    """OpenAI API integration service"""
    
    def __init__(self, api_key: str, model: str = "gpt-4", max_tokens: int = 2000):
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.base_url = "https://api.openai.com/v1"
    
    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate response using OpenAI API"""
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            response = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"


class ShellToolService(ToolExecutionService):
    """Shell command execution service"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
    
    async def execute_shell_command(self, session: ConversationSession, command: str) -> Dict[str, Any]:
        """Execute a shell command"""
        try:
            # Create subprocess with timeout
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.timeout
                )
                
                output = stdout.decode('utf-8') if stdout else ""
                error = stderr.decode('utf-8') if stderr else ""
                
                return {
                    "success": process.returncode == 0,
                    "output": output,
                    "error": error,
                    "exit_code": process.returncode
                }
            except asyncio.TimeoutError:
                process.kill()
                return {
                    "success": False,
                    "output": "",
                    "error": "Command timeout",
                    "exit_code": -1
                }
        
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "exit_code": -1
            }
    
    async def read_file(self, session: ConversationSession, file_path: str) -> Dict[str, Any]:
        """Read file content"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return {
                    "success": False,
                    "content": "",
                    "error": "File not found"
                }
            
            if file_path.is_file():
                async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                    content = await f.read()
                return {
                    "success": True,
                    "content": content
                }
            else:
                return {
                    "success": False,
                    "content": "",
                    "error": "Path is not a file"
                }
        
        except Exception as e:
            return {
                "success": False,
                "content": "",
                "error": str(e)
            }
    
    async def write_file(self, session: ConversationSession, file_path: str, content: str) -> Dict[str, Any]:
        """Write file content"""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(content)
            
            return {
                "success": True,
                "file_path": str(file_path)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def search_web(self, query: str) -> Dict[str, Any]:
        """Perform web search (placeholder implementation)"""
        # This would integrate with a search API like Google or Bing
        return {
            "success": True,
            "results": [f"Search results for: {query}"],
            "query": query
        }
    
    async def browser_automation(self, session: ConversationSession, action: str, **kwargs) -> Dict[str, Any]:
        """Perform browser automation"""
        # This would integrate with the browser automation module
        return {
            "success": True,
            "action": action,
            "result": "Browser action completed",
            "data": kwargs
        }


class SSEStreamingService(StreamingService):
    """Server-Sent Events streaming service"""
    
    def __init__(self):
        self.active_streams = {}
    
    async def stream_conversation(self, session: ConversationSession, message: str) -> AsyncGenerator[str, None]:
        """Stream conversation response via SSE"""
        
        # Send initial event
        yield f"event: message\ndata: {json.dumps({'content': 'Processing your message...'})}\n\n"
        
        # Simulate AI processing with steps
        steps = [
            "Analyzing your request...",
            "Identifying relevant tools...",
            "Executing commands...",
            "Generating response..."
        ]
        
        for step in steps:
            yield f"event: step\ndata: {json.dumps({'step': step})}\n\n"
            await asyncio.sleep(1)
        
        # Generate final response
        response = f"I received your message: '{message}'. This is a streaming response."
        
        yield f"event: message\ndata: {json.dumps({'content': response})}\n\n"
        yield f"event: done\ndata: {json.dumps({'completed': True})}\n\n"


class EventManagementService(EventService):
    """Event management service"""
    
    def __init__(self):
        self.event_handlers = {}
    
    async def create_event(self, session: ConversationSession, event_type: str, data: Dict[str, Any]) -> bool:
        """Create and emit an event"""
        try:
            # Create event in session
            event = session.add_event(event_type, data)
            
            # Notify registered handlers
            if event_type in self.event_handlers:
                for handler in self.event_handlers[event_type]:
                    await handler(session, event)
            
            return True
        
        except Exception as e:
            print(f"Failed to create event: {str(e)}")
            return False
    
    async def get_session_events(self, session_id: ConversationId) -> List[Dict[str, Any]]:
        """Get events for a session"""
        # This would query the repository for events
        return []
    
    def register_event_handler(self, event_type: str, handler):
        """Register an event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)