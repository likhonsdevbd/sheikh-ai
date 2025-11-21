# Sheikh - Intelligent Conversation Agent System

Sheikh is an intelligent conversation agent system built with FastAPI and OpenAI API, featuring Domain-Driven Design (DDD) architecture for robust, scalable, and maintainable code.

## Architecture Overview

### Backend (FastAPI + DDD)
- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and services
- **Infrastructure Layer**: Database, external services, and adapters
- **Interface Layer**: API controllers and middleware

### Frontend
- Modern React-based UI
- Interactive conversation interface
- File operation management
- Real-time communication with backend

### Sandbox
- Browser automation capabilities
- File system operations
- Shell command execution
- System monitoring and management

## Features

- 🧠 **Intelligent Dialogue**: Advanced conversation processing with OpenAI API
- 📁 **File Operations**: Secure file management and manipulation
- 🐚 **Shell Execution**: Safe command execution environment
- 🌐 **Browser Automation**: Automated web browsing and interaction
- 🏗️ **DDD Architecture**: Clean, maintainable codebase structure
- 🔒 **Security**: Robust security measures for all operations

## Project Structure

```
sheikh/
├── backend/          # FastAPI backend with DDD
│   ├── app/
│   │   ├── domain/   # Core business logic
│   │   ├── application/  # Use cases and services
│   │   ├── infrastructure/  # Database and external services
│   │   └── interfaces/  # API controllers
│   ├── tests/
│   └── docs/
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── pages/       # Application pages
│   │   ├── services/    # API communication
│   │   └── types/       # TypeScript definitions
│   └── tests/
└── sandbox/          # Automation and execution environment
    ├── automation/    # Browser automation
    ├── file_ops/     # File system operations
    ├── shell_execution/  # Command execution
    └── monitoring/   # System monitoring
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)

### Installation

1. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   ```

3. **Run the Application**:
   ```bash
   # Start backend
   cd backend && uvicorn app.interfaces.api.main:app --reload

   # Start frontend
   cd frontend && npm start
   ```

## Domain-Driven Design Implementation

### Domain Layer
- **Entities**: Conversation, User, FileOperation
- **Value Objects**: MessageId, UserId, Command
- **Aggregates**: ConversationAggregate
- **Services**: ConversationService, FileOperationService

### Application Layer
- **Use Cases**: SendMessageUseCase, ExecuteCommandUseCase
- **Command Handlers**: ProcessMessageHandler, ExecuteFileOperationHandler
- **Query Handlers**: GetConversationHandler, ListFilesHandler

### Infrastructure Layer
- **Persistence**: SQLAlchemy repositories
- **External Services**: OpenAI API client
- **Adapters**: File system adapter, shell execution adapter

## API Endpoints

### Conversations
- `POST /api/conversations` - Create new conversation
- `POST /api/conversations/{id}/messages` - Send message
- `GET /api/conversations/{id}` - Get conversation history

### File Operations
- `GET /api/files` - List files
- `POST /api/files` - Upload file
- `DELETE /api/files/{path}` - Delete file
- `GET /api/files/{path}/content` - Read file content

### Shell Commands
- `POST /api/shell/execute` - Execute command
- `GET /api/shell/processes` - List running processes

### Browser Automation
- `POST /api/browser/navigate` - Navigate to URL
- `POST /api/browser/click` - Click element
- `POST /api/browser/screenshot` - Take screenshot

## Security Considerations

- Input validation and sanitization
- Secure command execution with sandboxing
- Rate limiting and authentication
- File system access controls
- Browser session isolation

## Contributing

1. Follow DDD principles when adding new features
2. Maintain separation between layers
3. Write comprehensive tests
4. Document API changes
5. Follow security best practices

## License

MIT License - see LICENSE file for details

## Author

MiniMax Agent