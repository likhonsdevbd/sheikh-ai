"""
Domain value objects for the Sheikh conversation system
"""

from abc import ABC
from typing import Any, Optional
import uuid
from dataclasses import dataclass
from datetime import datetime


class ValueObject(ABC):
    """Base class for all value objects"""
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        return hash(self._value)


@dataclass(frozen=True)
class MessageId(ValueObject):
    """Unique identifier for messages"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("MessageId cannot be empty")
    
    @classmethod
    def generate(cls) -> "MessageId":
        """Generate a new unique message ID"""
        return cls(value=str(uuid.uuid4()))


@dataclass(frozen=True)
class ConversationId(ValueObject):
    """Unique identifier for conversations"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("ConversationId cannot be empty")
    
    @classmethod
    def generate(cls) -> "ConversationId":
        """Generate a new unique conversation ID"""
        return cls(value=str(uuid.uuid4()))


@dataclass(frozen=True)
class UserId(ValueObject):
    """Unique identifier for users"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("UserId cannot be empty")


@dataclass(frozen=True)
class Content(ValueObject):
    """Message content value object"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Content cannot be empty")
        
        if len(self.value) > 10000:  # Max 10k characters
            raise ValueError("Content too long")


@dataclass(frozen=True)
class Role(ValueObject):
    """Message role (user, assistant, system)"""
    value: str
    
    def __post_init__(self):
        valid_roles = ["user", "assistant", "system"]
        if self.value not in valid_roles:
            raise ValueError(f"Role must be one of: {valid_roles}")


@dataclass(frozen=True)
class Timestamp(ValueObject):
    """Timestamp value object"""
    value: datetime
    
    @classmethod
    def now(cls) -> "Timestamp":
        """Create timestamp with current time"""
        return cls(value=datetime.utcnow())


@dataclass(frozen=True)
class Command(ValueObject):
    """Shell command value object"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Command cannot be empty")


@dataclass(frozen=True)
class FilePath(ValueObject):
    """File path value object"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("FilePath cannot be empty")


@dataclass(frozen=True)
class Url(ValueObject):
    """URL value object"""
    value: str
    
    def __post_init__(self):
        if not self.value.startswith(('http://', 'https://')):
            raise ValueError("URL must start with http:// or https://")


@dataclass(frozen=True)
class Status(ValueObject):
    """Operation status value object"""
    value: str
    
    def __post_init__(self):
        valid_statuses = ["pending", "running", "completed", "failed", "cancelled"]
        if self.value not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")