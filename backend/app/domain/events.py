"""
Domain events for the Sheikh conversation system
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime
from ..domain.value_objects import ConversationId, MessageId


@dataclass
class DomainEvent:
    """Base domain event class"""
    event_id: str
    session_id: ConversationId
    event_type: str
    timestamp: datetime
    data: Dict[str, Any]
    
    def __post_init__(self):
        if not self.event_id:
            raise ValueError("Event ID cannot be empty")


@dataclass
class SessionCreatedEvent(DomainEvent):
    """Event fired when a new session is created"""
    title: str
    
    def __init__(self, session_id: ConversationId, title: str):
        super().__init__(
            event_id=f"session_created_{session_id.value}",
            session_id=session_id,
            event_type="session_created",
            timestamp=datetime.utcnow(),
            data={"title": title}
        )
        self.title = title


@dataclass
class MessageReceivedEvent(DomainEvent):
    """Event fired when a new message is received"""
    message_content: str
    role: str
    
    def __init__(self, session_id: ConversationId, message_id: MessageId, content: str, role: str):
        super().__init__(
            event_id=f"message_received_{message_id.value}",
            session_id=session_id,
            event_type="message_received",
            timestamp=datetime.utcnow(),
            data={
                "message_id": message_id.value,
                "content": content,
                "role": role
            }
        )
        self.message_content = content
        self.role = role


@dataclass
class MessageSentEvent(DomainEvent):
    """Event fired when a message is sent"""
    message_content: str
    
    def __init__(self, session_id: ConversationId, message_id: MessageId, content: str):
        super().__init__(
            event_id=f"message_sent_{message_id.value}",
            session_id=session_id,
            event_type="message_sent",
            timestamp=datetime.utcnow(),
            data={
                "message_id": message_id.value,
                "content": content
            }
        )
        self.message_content = content


@dataclass
class ToolInvokedEvent(DomainEvent):
    """Event fired when a tool is invoked"""
    tool_name: str
    tool_parameters: Dict[str, Any]
    tool_result: Optional[Dict[str, Any]] = None
    
    def __init__(self, session_id: ConversationId, tool_name: str, parameters: Dict[str, Any], result: Dict[str, Any] = None):
        super().__init__(
            event_id=f"tool_invoked_{session_id.value}_{tool_name}",
            session_id=session_id,
            event_type="tool_invoked",
            timestamp=datetime.utcnow(),
            data={
                "tool_name": tool_name,
                "parameters": parameters,
                "result": result
            }
        )
        self.tool_name = tool_name
        self.tool_parameters = parameters
        self.tool_result = result


@dataclass
class ShellCommandExecutedEvent(DomainEvent):
    """Event fired when a shell command is executed"""
    command: str
    output: str
    exit_code: int
    
    def __init__(self, session_id: ConversationId, command: str, output: str, exit_code: int = 0):
        super().__init__(
            event_id=f"shell_executed_{session_id.value}_{hash(command)}",
            session_id=session_id,
            event_type="shell_executed",
            timestamp=datetime.utcnow(),
            data={
                "command": command,
                "output": output,
                "exit_code": exit_code
            }
        )
        self.command = command
        self.output = output
        self.exit_code = exit_code


@dataclass
class FileOperationEvent(DomainEvent):
    """Event fired when a file operation is performed"""
    file_path: str
    operation_type: str
    content: Optional[str] = None
    
    def __init__(self, session_id: ConversationId, file_path: str, operation_type: str, content: str = None):
        super().__init__(
            event_id=f"file_op_{session_id.value}_{operation_type}_{hash(file_path)}",
            session_id=session_id,
            event_type="file_operation",
            timestamp=datetime.utcnow(),
            data={
                "file_path": file_path,
                "operation_type": operation_type,
                "content": content
            }
        )
        self.file_path = file_path
        self.operation_type = operation_type
        self.content = content


@dataclass
class SessionStatusChangedEvent(DomainEvent):
    """Event fired when session status changes"""
    old_status: str
    new_status: str
    
    def __init__(self, session_id: ConversationId, old_status: str, new_status: str):
        super().__init__(
            event_id=f"status_changed_{session_id.value}_{new_status}",
            session_id=session_id,
            event_type="status_changed",
            timestamp=datetime.utcnow(),
            data={
                "old_status": old_status,
                "new_status": new_status
            }
        )
        self.old_status = old_status
        self.new_status = new_status


@dataclass
class ErrorEvent(DomainEvent):
    """Event fired when an error occurs"""
    error_message: str
    error_type: str
    
    def __init__(self, session_id: ConversationId, error_message: str, error_type: str = "general"):
        super().__init__(
            event_id=f"error_{session_id.value}_{hash(error_message)}",
            session_id=session_id,
            event_type="error",
            timestamp=datetime.utcnow(),
            data={
                "error_message": error_message,
                "error_type": error_type
            }
        )
        self.error_message = error_message
        self.error_type = error_type