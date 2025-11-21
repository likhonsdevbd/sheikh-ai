# Sheikh AI - Intelligent Conversation Agent

A modern, enhanced AI conversation system built with Vue 3, FastAPI, and advanced AI protocols. Sheikh AI features AI SDK integration, AG-UI protocols, CopilotKit, and multi-provider AI support including Google Generative AI (Gemini 3 Pro Preview) and OpenAI.

## 🚀 Features

### Core Features
- **Real-time Conversation**: Interactive chat interface with streaming responses
- **Multi-modal AI Support**: Text, images, and advanced reasoning capabilities
- **File Operations**: Upload, read, and manage files within conversations
- **Shell Integration**: Execute shell commands in a secure sandbox environment
- **Browser Automation**: VNC-based remote desktop access for sessions
- **Session Management**: Persistent conversation sessions with history

### AI & Protocols
- **AI SDK Integration**: Unified AI provider interface
- **Google Generative AI**: Gemini 3 Pro Preview with enhanced reasoning
- **OpenAI Integration**: GPT-4 and other OpenAI models
- **AG-UI Protocol**: Advanced Graphical User Interface protocols
- **CopilotKit Integration**: Enhanced developer experience
- **Tool Calling**: Structured function calling capabilities
- **Web Search with Grounding**: Real-time web search integration
- **Image Generation**: AI-powered image creation
- **Structured Data Output**: JSON schema validation and structured responses

### Technical Features
- **Domain-Driven Design**: Clean architecture with separated concerns
- **Event Sourcing**: Comprehensive event management system
- **CQRS Pattern**: Command and Query Responsibility Segregation
- **Real-time Updates**: Server-Sent Events (SSE) for live updates
- **WebSocket Support**: Bi-directional communication for VNC sessions
- **CORS Support**: Cross-origin resource sharing configuration
- **Async/Await**: Full asynchronous Python backend
- **Type Safety**: Pydantic models for data validation

## 🏗️ Architecture

### Frontend (Vue 3 + Vite)
```
frontend/
├── src/
│   ├── components/        # Vue components
│   ├── views/            # Page components
│   ├── stores/           # Pinia state management
│   ├── services/         # API services
│   ├── types/            # TypeScript definitions
│   └── utils/            # Utility functions
├── public/               # Static assets
└── package.json          # Dependencies and scripts
```

### Backend (FastAPI + Python)
```
backend/
├── app/
│   ├── domain/           # Domain models and logic
│   │   ├── entities.py   # Core entities
│   │   ├── value_objects.py # Value objects
│   │   ├── events.py     # Domain events
│   │   └── services.py   # Domain services
│   ├── application/      # Application layer
│   │   ├── services.py   # Application services
│   │   ├── command_handlers/ # Command handlers
│   │   └── query_handlers/   # Query handlers
│   ├── infrastructure/   # Infrastructure layer
│   │   ├── config.py     # Configuration management
│   │   ├── services.py   # Infrastructure services
│   │   └── adapters/     # External adapters
│   └── interfaces/       # Interface layer
│       └── api/          # REST API endpoints
└── requirements.txt      # Python dependencies
```

## 🚦 Getting Started

### Prerequisites
- **Node.js** 18+ and **pnpm**
- **Python** 3.11+ and **uv**
- **Git** for version control

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/likhonsdevbd/sheikh-ai.git
   cd sheikh-ai
   ```

2. **Backend Setup**
   ```bash
   cd backend
   
   # Create virtual environment and install dependencies
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   
   # Install dependencies
   pnpm install
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your API keys
   ```

### API Keys Configuration

Create `.env` files in both directories with your API keys:

**Backend .env:**
```env
# Google Generative AI
google_generative_ai_api_key=your_google_ai_api_key

# OpenAI
openai_api_key=your_openai_api_key

# AI SDK Settings
ai_sdk_providers=google,openai
default_ai_provider=google
enable_streaming=true
max_tokens=4096
temperature=0.7

# Server Settings
host=127.0.0.1
port=8000
debug=true

# CopilotKit
copilotkit_enabled=true
copilotkit_config_path=/copilotkit
```

**Frontend .env:**
```env
# Google Generative AI
VITE_GOOGLE_GENERATIVE_AI_API_KEY=your_google_ai_api_key
```

### Running the Application

1. **Start Backend**
   ```bash
   cd backend
   python start_server.py
   # Backend runs on http://localhost:8000
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   pnpm dev
   # Frontend runs on http://localhost:3000
   ```

3. **Access the Application**
   Open your browser to `http://localhost:3000`

## 📊 API Endpoints

### Conversation Management
- `GET /api/conversations/sessions` - List all sessions
- `PUT /api/conversations/sessions` - Create new session
- `GET /api/conversations/sessions/{id}` - Get session details
- `DELETE /api/conversations/sessions/{id}` - Delete session
- `POST /api/conversations/sessions/{id}/chat` - Send chat message
- `POST /api/conversations/sessions/{id}/stop` - Stop session

### File Operations
- `POST /api/files/sessions/{id}/file` - View file content

### Shell Operations
- `POST /api/shell/sessions/{id}/shell` - View shell session

### Browser Operations
- `WS /api/browser/sessions/{id}/vnc` - VNC WebSocket connection

### AI Integration
- `POST /api/ai/chat` - AI SDK chat endpoint
- `POST /api/ai/generate` - AI generation endpoint

### System
- `GET /` - Root endpoint with system information
- `GET /health` - Health check endpoint

## 🛠️ Development

### Code Structure
- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and application services
- **Infrastructure Layer**: External integrations and persistence
- **Interface Layer**: HTTP APIs and web interfaces

### Key Patterns
- **DDD (Domain-Driven Design)**: Clear separation of concerns
- **CQRS**: Command and Query Responsibility Segregation
- **Event Sourcing**: Comprehensive event tracking
- **Dependency Injection**: Clean service management

### Development Commands

```bash
# Backend development
cd backend
python -m pytest tests/          # Run tests
python start_server.py           # Start development server

# Frontend development  
cd frontend
pnpm dev                        # Start development server
pnpm build                      # Build for production
pnpm preview                    # Preview production build
pnpm type-check                 # TypeScript type checking
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Manual Deployment
1. **Backend**: Deploy FastAPI app to your preferred Python hosting
2. **Frontend**: Build and deploy static files to CDN/hosting service
3. **Database**: Set up PostgreSQL or SQLite as needed
4. **Environment**: Configure production environment variables

## 🔧 Configuration

### Environment Variables

**Backend Configuration:**
- `google_generative_ai_api_key`: Google AI API key
- `openai_api_key`: OpenAI API key
- `ai_sdk_providers`: Comma-separated AI providers
- `default_ai_provider`: Default AI provider
- `enable_streaming`: Enable streaming responses
- `max_tokens`: Maximum tokens for AI responses
- `temperature`: AI response creativity (0.0-1.0)

**Frontend Configuration:**
- `VITE_GOOGLE_GENERATIVE_AI_API_KEY`: Frontend Google AI key

### Server Settings
- `host`: Server host (default: 127.0.0.1)
- `port`: Server port (default: 8000)
- `debug`: Enable debug mode
- `allowed_origins`: CORS allowed origins
- `log_level`: Logging level

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow the existing code structure and patterns
- Add type hints for Python code
- Include docstrings for functions and classes
- Write tests for new functionality
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Generative AI** for Gemini 3 Pro Preview
- **OpenAI** for GPT-4 and API access
- **Vue.js Team** for the excellent frontend framework
- **FastAPI Team** for the modern Python web framework
- **AI SDK** for unified AI provider interface
- **CopilotKit** for enhanced development experience

## 📞 Support

For support, email [likhonsdevbd@gmail.com](mailto:likhonsdevbd@gmail.com) or join our Discord community.

---

**Built with ❤️ by [Likhon Sheikh](https://github.com/likhonsdevbd)**