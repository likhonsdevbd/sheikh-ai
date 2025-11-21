"""
Query handlers for the Sheikh conversation system
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ...application.services import ConversationApplicationService


class Query(ABC):
    """Base query class"""
    pass


class GetSessionQuery(Query):
    """Query to get a specific session"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id


class ListSessionsQuery(Query):
    """Query to list all sessions"""
    
    def __init__(self):
        pass


class GetSessionEventsQuery(Query):
    """Query to get session events"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id


class GetSessionHistoryQuery(Query):
    """Query to get session conversation history"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id


class QueryHandler(ABC):
    """Base query handler interface"""
    
    @abstractmethod
    async def handle(self, query: Query) -> Dict[str, Any]:
        """Handle a query and return result"""
        pass


class GetSessionQueryHandler(QueryHandler):
    """Handler for getting specific sessions"""
    
    def __init__(self, service: ConversationApplicationService):
        self.service = service
    
    async def handle(self, query: GetSessionQuery) -> Dict[str, Any]:
        """Handle get session query"""
        return await self.service.get_session(query.session_id)


class ListSessionsQueryHandler(QueryHandler):
    """Handler for listing sessions"""
    
    def __init__(self, service: ConversationApplicationService):
        self.service = service
    
    async def handle(self, query: ListSessionsQuery) -> Dict[str, Any]:
        """Handle list sessions query"""
        return await self.service.list_sessions()


class GetSessionEventsQueryHandler(QueryHandler):
    """Handler for getting session events"""
    
    def __init__(self, service: ConversationApplicationService):
        self.service = service
    
    async def handle(self, query: GetSessionEventsQuery) -> Dict[str, Any]:
        """Handle get session events query"""
        try:
            session_data = await self.service.get_session(query.session_id)
            
            if session_data["code"] != 0:
                return session_data
            
            events = session_data["data"]["events"]
            return {
                "code": 0,
                "msg": "success",
                "data": {
                    "events": events
                }
            }
        except Exception as e:
            return {
                "code": 500,
                "msg": f"Failed to get session events: {str(e)}",
                "data": None
            }


class GetSessionHistoryQueryHandler(QueryHandler):
    """Handler for getting session conversation history"""
    
    def __init__(self, service: ConversationApplicationService):
        self.service = service
    
    async def handle(self, query: GetSessionHistoryQuery) -> Dict[str, Any]:
        """Handle get session history query"""
        try:
            session_data = await self.service.get_session(query.session_id)
            
            if session_data["code"] != 0:
                return session_data
            
            session = session_data["data"]
            
            # Extract messages from events
            messages = []
            for event in session["events"]:
                if event["event_type"] in ["message_received", "message_sent"]:
                    messages.append({
                        "role": "user" if event["event_type"] == "message_received" else "assistant",
                        "content": event["data"].get("content", ""),
                        "timestamp": event.get("timestamp", "")
                    })
            
            return {
                "code": 0,
                "msg": "success",
                "data": {
                    "session_id": session["session_id"],
                    "title": session["title"],
                    "messages": messages
                }
            }
        except Exception as e:
            return {
                "code": 500,
                "msg": f"Failed to get session history: {str(e)}",
                "data": None
            }


class QueryBus:
    """Query bus for handling queries"""
    
    def __init__(self):
        self.handlers = {}
    
    def register_handler(self, query_type: type, handler: QueryHandler):
        """Register a query handler"""
        self.handlers[query_type] = handler
    
    async def ask(self, query: Query) -> Dict[str, Any]:
        """Ask a query to the appropriate handler"""
        query_type = type(query)
        
        if query_type not in self.handlers:
            raise ValueError(f"No handler registered for query type: {query_type}")
        
        handler = self.handlers[query_type]
        return await handler.handle(query)