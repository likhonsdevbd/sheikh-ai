"""
Command handlers for the Sheikh conversation system
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
import uuid
from datetime import datetime

from ...application.services import (
    ConversationApplicationService, ShellApplicationService, FileApplicationService
)


class Command(ABC):
    """Base command class"""
    pass


class CreateSessionCommand(Command):
    """Command to create a new session"""
    
    def __init__(self, title: str = "New Conversation"):
        self.title = title


class DeleteSessionCommand(Command):
    """Command to delete a session"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id


class StopSessionCommand(Command):
    """Command to stop an active session"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id


class SendMessageCommand(Command):
    """Command to send a message in a session"""
    
    def __init__(self, session_id: str, message: str, timestamp: int, event_id: str = None):
        self.session_id = session_id
        self.message = message
        self.timestamp = timestamp
        self.event_id = event_id


class ExecuteShellCommandCommand(Command):
    """Command to execute a shell command"""
    
    def __init__(self, session_id: str, command: str):
        self.session_id = session_id
        self.command = command


class ReadFileCommand(Command):
    """Command to read file content"""
    
    def __init__(self, session_id: str, file_path: str):
        self.session_id = session_id
        self.file_path = file_path


class WriteFileCommand(Command):
    """Command to write file content"""
    
    def __init__(self, session_id: str, file_path: str, content: str):
        self.session_id = session_id
        self.file_path = file_path
        self.content = content


class CommandHandler(ABC):
    """Base command handler interface"""
    
    @abstractmethod
    async def handle(self, command: Command) -> Dict[str, Any]:
        """Handle a command and return result"""
        pass


class CreateSessionCommandHandler(CommandHandler):
    """Handler for creating sessions"""
    
    def __init__(self, service: ConversationApplicationService):
        self.service = service
    
    async def handle(self, command: CreateSessionCommand) -> Dict[str, Any]:
        """Handle create session command"""
        return await self.service.create_session(command.title)


class DeleteSessionCommandHandler(CommandHandler):
    """Handler for deleting sessions"""
    
    def __init__(self, service: ConversationApplicationService):
        self.service = service
    
    async def handle(self, command: DeleteSessionCommand) -> Dict[str, Any]:
        """Handle delete session command"""
        return await self.service.delete_session(command.session_id)


class StopSessionCommandHandler(CommandHandler):
    """Handler for stopping sessions"""
    
    def __init__(self, service: ConversationApplicationService):
        self.service = service
    
    async def handle(self, command: StopSessionCommand) -> Dict[str, Any]:
        """Handle stop session command"""
        return await self.service.stop_session(command.session_id)


class SendMessageCommandHandler(CommandHandler):
    """Handler for sending messages"""
    
    def __init__(self, service: ConversationApplicationService):
        self.service = service
    
    async def handle(self, command: SendMessageCommand) -> Dict[str, Any]:
        """Handle send message command"""
        return await self.service.process_chat_message(
            command.session_id,
            command.message,
            command.timestamp,
            command.event_id
        )


class ExecuteShellCommandCommandHandler(CommandHandler):
    """Handler for executing shell commands"""
    
    def __init__(self, shell_service: ShellApplicationService):
        self.shell_service = shell_service
    
    async def handle(self, command: ExecuteShellCommandCommand) -> Dict[str, Any]:
        """Handle execute shell command"""
        # This would integrate with actual shell execution
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "command": command.command,
                "output": f"Executing: {command.command}",
                "exit_code": 0
            }
        }


class ReadFileCommandHandler(CommandHandler):
    """Handler for reading files"""
    
    def __init__(self, file_service: FileApplicationService):
        self.file_service = file_service
    
    async def handle(self, command: ReadFileCommand) -> Dict[str, Any]:
        """Handle read file command"""
        return await self.file_service.view_file_content(command.session_id, command.file_path)


class WriteFileCommandHandler(CommandHandler):
    """Handler for writing files"""
    
    def __init__(self, file_service: FileApplicationService):
        self.file_service = file_service
    
    async def handle(self, command: WriteFileCommand) -> Dict[str, Any]:
        """Handle write file command"""
        # This would implement actual file writing
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "file": command.file_path,
                "content": command.content
            }
        }


class CommandBus:
    """Command bus for handling commands"""
    
    def __init__(self):
        self.handlers = {}
    
    def register_handler(self, command_type: type, handler: CommandHandler):
        """Register a command handler"""
        self.handlers[command_type] = handler
    
    async def send(self, command: Command) -> Dict[str, Any]:
        """Send a command to the appropriate handler"""
        command_type = type(command)
        
        if command_type not in self.handlers:
            raise ValueError(f"No handler registered for command type: {command_type}")
        
        handler = self.handlers[command_type]
        return await handler.handle(command)


# Export all classes for easy importing
__all__ = [
    'Command',
    'CreateSessionCommand',
    'DeleteSessionCommand',
    'StopSessionCommand',
    'SendMessageCommand',
    'ExecuteShellCommandCommand',
    'ReadFileCommand',
    'WriteFileCommand',
    'CommandHandler',
    'CreateSessionCommandHandler',
    'DeleteSessionCommandHandler',
    'StopSessionCommandHandler',
    'SendMessageCommandHandler',
    'ExecuteShellCommandCommandHandler',
    'ReadFileCommandHandler',
    'WriteFileCommandHandler',
    'CommandBus'
]