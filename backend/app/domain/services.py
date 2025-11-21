"""
Domain services for the Sheikh conversation system
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, AsyncGenerator
from ..domain.entities import ConversationSession, Message, ShellSession, FileOperation
from ..domain.value_objects import ConversationId, Status


class ConversationDomainService(ABC):
    """Domain service for conversation management"""
    
    @abstractmethod
    async def create_session(self, title: str) -> ConversationSession:
        """Create a new conversation session"""
        pass
    
    @abstractmethod
    async def get_session(self, session_id: ConversationId) -> Optional[ConversationSession]:
        """Get a conversation session by ID"""
        pass
    
    @abstractmethod
    async def list_sessions(self) -> List[ConversationSession]:
        """List all conversation sessions"""
        pass
    
    @abstractmethod
    async def delete_session(self, session_id: ConversationId) -> bool:
        """Delete a conversation session"""
        pass
    
    @abstractmethod
    async def stop_session(self, session_id: ConversationId) -> bool:
        """Stop an active conversation session"""
        pass


class ToolExecutionService(ABC):
    """Domain service for tool execution"""
    
    @abstractmethod
    async def execute_shell_command(self, session: ConversationSession, command: str) -> Dict[str, Any]:
        """Execute a shell command"""
        pass
    
    @abstractmethod
    async def read_file(self, session: ConversationSession, file_path: str) -> Dict[str, Any]:
        """Read file content"""
        pass
    
    @abstractmethod
    async def write_file(self, session: ConversationSession, file_path: str, content: str) -> Dict[str, Any]:
        """Write file content"""
        pass
    
    @abstractmethod
    async def search_web(self, query: str) -> Dict[str, Any]:
        """Perform web search"""
        pass
    
    @abstractmethod
    async def browser_automation(self, session: ConversationSession, action: str, **kwargs) -> Dict[str, Any]:
        """Perform browser automation"""
        pass


class StreamingService(ABC):
    """Domain service for streaming responses"""
    
    @abstractmethod
    async def stream_conversation(self, session: ConversationSession, message: str) -> AsyncGenerator[str, None]:
        """Stream conversation response via SSE"""
        pass


class EventService(ABC):
    """Domain service for event management"""
    
    @abstractmethod
    async def create_event(self, session: ConversationSession, event_type: str, data: Dict[str, Any]) -> bool:
        """Create and emit an event"""
        pass
    
    @abstractmethod
    async def get_session_events(self, session_id: ConversationId) -> List[Dict[str, Any]]:
        """Get events for a session"""
        pass