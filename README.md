# Sheikh AI Assistant - Enhanced with Modern AI SDK Integration

Sheikh is a cutting-edge intelligent conversation agent system enhanced with AI SDK providers, Google Generative AI (Gemini 3 Pro Preview), AG-UI Protocol, and CopilotKit integration. Built with Domain-Driven Design (DDD) architecture for robust, scalable, and maintainable code.

## ✨ What's New in v2.0

### 🤖 AI SDK Integration
- **Google Generative AI** with Gemini 3 Pro Preview
- **Advanced Reasoning** with configurable thinking levels
- **Multi-modal AI** (text, images, files, documents)
- **Tool Calling** and function execution
- **Web Search** with Google Search grounding
- **Image Generation** using Imagen 3.0
- **Structured Data** output with JSON schemas

### 🌐 AG-UI Protocol & CopilotKit
- Bi-directional agent-user communication
- Real-time streaming responses
- Enhanced user experience with rich interactions
- Production-ready AI components
- Built-in security and prompt injection protection

### ♿ Accessibility & UX (WCAG Compliant)
- Full keyboard navigation support
- Screen reader compatibility
- High contrast mode support
- Mobile-optimized touch targets (≥44px)
- Focus management and ARIA compliance

## 🚀 Architecture Overview

### Backend (FastAPI + DDD + AI SDK)
- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and AI services
- **Infrastructure Layer**: Database, AI providers, and adapters
- **Interface Layer**: Enhanced API with AI SDK integration

### Frontend (Vue 3 + Enhanced AI Interface)
- **Three Chat Modes**: Traditional, Enhanced, and AI SDK Interface
- **Accessibility-first design** following WCAG guidelines
- **Real-time streaming** with AI responses
- **Multi-modal support** for files and images
- **Advanced UI components** with rich interactions

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

## Core Features

### 🤖 AI-Powered Capabilities
- 🧠 **Advanced Reasoning**: Gemini 3 Pro Preview with configurable thinking levels
- 💻 **Code Generation**: Multi-language code analysis and generation
- 🔍 **Web Research**: Google Search grounding with sources and citations
- 📄 **File Analysis**: Multi-modal document, image, and code analysis
- 🎨 **Image Generation**: Text-to-image with Imagen 3.0
- 📊 **Structured Data**: JSON schema-based structured responses

### 🛠️ System Operations
- 📁 **File Operations**: Secure file management and manipulation
- 🐚 **Shell Execution**: Safe command execution environment
- 🌐 **Browser Automation**: Automated web browsing and interaction
- 🏗️ **DDD Architecture**: Clean, maintainable codebase structure
- 🔒 **Security**: Robust security measures and content safety filtering

### 🎨 User Interface
- 📱 **Responsive Design**: Mobile-first, accessibility-compliant interface
- ⌨️ **Keyboard Navigation**: Full keyboard support for all features
- 🎯 **Three Chat Modes**: Traditional, Enhanced AI, and AI SDK Interface
- ⚡ **Real-time Streaming**: Live response updates and progress indicators
- 🎪 **Rich Interactions**: Dynamic UI components and action buttons

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