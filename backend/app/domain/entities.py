"""
Domain entities for the Sheikh conversation system
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..value_objects import (
    MessageId, ConversationId, UserId, Content, Role, Timestamp,
    Status, Command, FilePath, Url
)


@dataclass
class Message:
    """Message entity in a conversation"""
    message_id: MessageId
    conversation_id: ConversationId
    role: Role
    content: Content
    timestamp: Timestamp
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.conversation_id:
            raise ValueError("Message must belong to a conversation")


@dataclass
class Event:
    """Event entity for real-time communication"""
    event_id: str
    session_id: ConversationId
    event_type: str  # message, title, plan, step, tool, error, done
    data: Dict[str, Any]
    timestamp: Timestamp
    
    def __post_init__(self):
        valid_event_types = ["message", "title", "plan", "step", "tool", "error", "done"]
        if self.event_type not in valid_event_types:
            raise ValueError(f"Event type must be one of: {valid_event_types}")


@dataclass
class ShellSession:
    """Shell session entity"""
    shell_session_id: str
    conversation_id: ConversationId
    session_id: Optional[str] = None
    console: List[Dict[str, str]] = field(default_factory=list)
    created_at: Timestamp = field(default_factory=Timestamp.now)
    last_updated: Timestamp = field(default_factory=Timestamp.now)
    
    def add_console_entry(self, ps1: str, command: str, output: str) -> None:
        """Add a new console entry"""
        entry = {
            "ps1": ps1,
            "command": command,
            "output": output
        }
        self.console.append(entry)
        self.last_updated = Timestamp.now()
    
    def get_latest_output(self) -> str:
        """Get the latest shell output"""
        if not self.console:
            return ""
        return self.console[-1].get("output", "")


@dataclass
class FileOperation:
    """File operation entity"""
    file_path: FilePath
    conversation_id: ConversationId
    operation_type: str  # read, write, delete
    content: Optional[str] = None
    timestamp: Timestamp = field(default_factory=Timestamp.now)
    
    def __post_init__(self):
        valid_operations = ["read", "write", "delete"]
        if self.operation_type not in valid_operations:
            raise ValueError(f"Operation type must be one of: {valid_operations}")


@dataclass
class ConversationSession:
    """Conversation session aggregate root"""
    session_id: ConversationId
    title: str
    user_id: Optional[UserId] = None
    messages: List[Message] = field(default_factory=list)
    events: List[Event] = field(default_factory=list)
    status: Status = field(default_factory=lambda: Status("pending"))
    shell_sessions: List[ShellSession] = field(default_factory=list)
    file_operations: List[FileOperation] = field(default_factory=list)
    created_at: Timestamp = field(default_factory=Timestamp.now)
    last_updated: Timestamp = field(default_factory=Timestamp.now)
    unread_message_count: int = 0
    
    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None) -> Message:
        """Add a new message to the conversation"""
        message = Message(
            message_id=MessageId.generate(),
            conversation_id=self.session_id,
            role=Role(role),
            content=Content(content),
            timestamp=Timestamp.now(),
            metadata=metadata or {}
        )
        self.messages.append(message)
        self.last_updated = Timestamp.now()
        return message
    
    def add_event(self, event_type: str, data: Dict[str, Any]) -> Event:
        """Add a new event to the conversation"""
        event = Event(
            event_id=str(MessageId.generate()),
            session_id=self.session_id,
            event_type=event_type,
            data=data,
            timestamp=Timestamp.now()
        )
        self.events.append(event)
        self.last_updated = Timestamp.now()
        return event
    
    def create_shell_session(self, shell_session_id: str) -> ShellSession:
        """Create a new shell session"""
        shell_session = ShellSession(
            shell_session_id=shell_session_id,
            conversation_id=self.session_id
        )
        self.shell_sessions.append(shell_session)
        self.last_updated = Timestamp.now()
        return shell_session
    
    def add_file_operation(self, file_path: str, operation_type: str, content: str = None) -> FileOperation:
        """Add a new file operation"""
        file_op = FileOperation(
            file_path=FilePath(file_path),
            conversation_id=self.session_id,
            operation_type=operation_type,
            content=content
        )
        self.file_operations.append(file_op)
        self.last_updated = Timestamp.now()
        return file_op
    
    def get_latest_message(self) -> Optional[Message]:
        """Get the latest message in the conversation"""
        if not self.messages:
            return None
        return self.messages[-1]
    
    def update_status(self, new_status: str) -> None:
        """Update the conversation status"""
        self.status = Status(new_status)
        self.last_updated = Timestamp.now()
    
    def increment_unread_count(self) -> None:
        """Increment the unread message count"""
        self.unread_message_count += 1
    
    def clear_unread_count(self) -> None:
        """Clear the unread message count"""
        self.unread_message_count = 0