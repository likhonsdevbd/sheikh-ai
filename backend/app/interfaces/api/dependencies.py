"""
API dependencies for dependency injection
"""

from ..application.services import (
    ConversationApplicationService, ShellApplicationService, FileApplicationService
)
from ..infrastructure.services import (
    ConversationRepositoryService, ShellToolService, 
    SSEStreamingService, EventManagementService,
    FileConversationRepository
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