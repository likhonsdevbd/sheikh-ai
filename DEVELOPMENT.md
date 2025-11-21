# Sheikh AI Assistant - Development Guide

Author: **Likhon Sheikh and Team Sheikh**

## Overview

Sheikh is an intelligent conversation agent system built with FastAPI and OpenAI API, featuring Domain-Driven Design (DDD) architecture and a comprehensive sandbox environment for secure AI-powered operations.

## Architecture

### Backend (FastAPI + DDD)
- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and services
- **Infrastructure Layer**: Database, external services, and adapters
- **Interface Layer**: API controllers and middleware

### Frontend (Vue 3 + TypeScript + Vite)
- Modern React-based UI with Ant Design X
- RICH paradigm for AI interface design
- Real-time communication with backend
- Interactive tool panels

### Sandbox Environment
- Docker-based isolated execution
- Secure shell command execution
- File system operations
- Browser automation with Chrome
- VNC remote access

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for local development)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd sheikh
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Start Services
```bash
./start.sh
```

### 4. Run Frontend (Separate Terminal)
```bash
cd frontend
npm install
npm run dev
```

### 5. Access Application
- Backend API: http://localhost:8080
- Frontend: http://localhost:3000
- VNC Access: localhost:5900
- Chrome DevTools: http://localhost:9222

## API Documentation

### Session Management

#### Create Session
```http
PUT /api/v1/sessions
```
Creates a new conversation session.

**Response:**
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "session_id": "uuid-string"
  }
}
```

#### Get Session
```http
GET /api/v1/sessions/{session_id}
```
Retrieves session information and conversation history.

#### List Sessions
```http
GET /api/v1/sessions
```
Returns list of all sessions with metadata.

#### Delete Session
```http
DELETE /api/v1/sessions/{session_id}
```
Removes a session permanently.

#### Stop Session
```http
POST /api/v1/sessions/{session_id}/stop
```
Stops an active session.

### Real-time Chat

#### Chat with Session (SSE)
```http
POST /api/v1/sessions/{session_id}/chat
```

**Request Body:**
```json
{
  "message": "User message",
  "timestamp": 1700000000,
  "event_id": "optional-event-id"
}
```

**Response:** Server-Sent Events stream

**Event Types:**
- `message`: Text message from assistant
- `title`: Session title update
- `plan`: Execution plan with steps
- `step`: Step status update
- `tool`: Tool invocation information
- `error`: Error information
- `done`: Conversation completion

### Tool Integration

#### Shell Operations
```http
POST /api/v1/sessions/{session_id}/shell
```

#### File Operations
```http
POST /api/v1/sessions/{session_id}/file
```

#### Browser Automation
```http
POST /api/v1/sessions/{session_id}/browser
```

### VNC Access

#### WebSocket Connection
```
WebSocket /api/v1/sessions/{session_id}/vnc
```

Protocol: WebSocket (binary mode)
Subprotocol: binary

## Development

### Backend Development

#### Structure
```
backend/
├── app/
│   ├── domain/           # Core business logic
│   │   ├── entities.py
│   │   ├── value_objects.py
│   │   ├── services.py
│   │   └── events.py
│   ├── application/      # Use cases and services
│   │   ├── services.py
│   │   ├── command_handlers.py
│   │   └── query_handlers.py
│   ├── infrastructure/   # Database and external services
│   │   ├── config.py
│   │   └── services.py
│   └── interfaces/       # API controllers
│       ├── api/
│       │   ├── main.py
│       │   ├── routers.py
│       │   └── dependencies.py
└── tests/
```

#### Running Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.interfaces.api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Adding New Tools

1. **Define Tool Interface** (domain layer):
```python
# backend/app/domain/services.py
class NewToolService:
    @abstractmethod
    async def execute_operation(self, param: str) -> Dict[str, Any]:
        pass
```

2. **Implement Tool** (infrastructure layer):
```python
# backend/app/infrastructure/services.py
class ConcreteNewToolService(NewToolService):
    async def execute_operation(self, param: str) -> Dict[str, Any]:
        # Implementation here
        return {"success": True, "result": "operation completed"}
```

3. **Register Tool** (application layer):
```python
# Update services.py to register new tool
tool_service = ConcreteNewToolService()
```

### Frontend Development

#### Structure
```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   ├── pages/           # Application pages
│   ├── stores/          # Pinia state management
│   ├── services/        # API communication
│   ├── types/           # TypeScript definitions
│   └── styles/          # Global styles
├── public/
└── tests/
```

#### Running Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Key Components

**Chat Interface** (`App.vue`):
- Real-time messaging
- Message streaming
- Tool integration
- Session management

**Tool Panels**:
- Terminal: Shell command execution
- File Explorer: File system operations
- Browser: Web automation
- Search: Web search integration

### DDD Implementation

#### Value Objects
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class MessageId:
    value: str
```

#### Entities
```python
@dataclass
class Message:
    message_id: MessageId
    content: Content
    role: Role
    timestamp: Timestamp
```

#### Domain Services
```python
class ConversationDomainService:
    async def create_session(self, title: str) -> ConversationSession:
        # Core business logic
        pass
```

#### Application Services
```python
class ConversationApplicationService:
    def __init__(self, domain_service, tool_service, event_service):
        self.domain_service = domain_service
        self.tool_service = tool_service
        self.event_service = event_service
```

## Sandbox Environment

### Docker Configuration

#### Dockerfile Features
- Ubuntu 22.04 base
- Python 3.11 environment
- Node.js 18 for frontend
- VNC server setup
- Chrome browser automation
- Process management with Supervisor

#### Process Management
The sandbox uses Supervisor for process orchestration:

- **FastAPI Backend**: Main application server
- **VNC Server**: Remote desktop access
- **Xvfb**: Virtual framebuffer
- **Chrome Browser**: Browser automation
- **Window Manager**: Fluxbox
- **Process Monitor**: System monitoring

### Browser Automation

#### Chrome Setup
- Remote debugging enabled on port 9222
- User data directory for session persistence
- Security settings for automation

#### Playwright Integration
```python
from playwright.async_api import async_playwright

async def automate_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage']
    )
    # Automation logic here
```

### Security Considerations

#### Shell Command Execution
- Timeout enforcement
- Command whitelisting
- Workspace isolation
- Process monitoring

#### File System Access
- Sandboxed file operations
- Path validation
- Size limitations
- Extension filtering

#### Browser Security
- Isolated browser instances
- Remote debugging interface
- Session management
- Security headers

## Testing

### Backend Testing
```bash
cd backend
pytest tests/ -v
```

### Frontend Testing
```bash
cd frontend
npm run test
```

### Integration Testing
```bash
# Run full system test
docker-compose -f docker-compose.test.yml up --build
```

## Deployment

### Production Deployment
1. **Environment Setup**:
   ```bash
   cp .env.example .env.production
   # Configure production settings
   ```

2. **Build and Deploy**:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

3. **Health Check**:
   ```bash
   curl http://localhost:8080/health
   ```

### Scaling Considerations
- Redis for session storage
- PostgreSQL for production database
- Load balancing for multiple instances
- Monitoring and metrics

## Troubleshooting

### Common Issues

#### Backend Not Starting
```bash
# Check logs
docker-compose logs backend

# Common solutions
# 1. Check OpenAI API key
# 2. Verify port availability
# 3. Check environment variables
```

#### Frontend Build Issues
```bash
# Clear dependencies
rm -rf node_modules package-lock.json
npm install

# Check TypeScript
npm run type-check
```

#### Browser Automation Issues
```bash
# Check Chrome version
google-chrome --version

# Clear browser data
rm -rf browser/user_data/*
```

### Debug Mode
Set environment variables:
```bash
DEBUG=true
LOG_LEVEL=DEBUG
VERBOSE_LOGGING=true
```

## Contributing

### Code Style
- **Backend**: Black, isort, mypy
- **Frontend**: ESLint, Prettier, TypeScript strict mode

### Commit Messages
Follow conventional commits:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/modifications
- `chore:` Build/process changes

### Pull Request Process
1. Fork the repository
2. Create feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit pull request with description

## License

MIT License - see LICENSE file for details

## Support

For questions and support:
- Create an issue on GitHub
- Check the documentation
- Review the API examples

## Authors

**Likhon Sheikh and Team Sheikh** - Initial work and ongoing development

## Acknowledgments

- Ant Design team for the RICH paradigm
- FastAPI community for the excellent framework
- Vue.js team for the progressive framework
- All contributors and users of Sheikh AI Assistant