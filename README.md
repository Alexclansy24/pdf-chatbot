////////****IMPORTANT CLOUDFLARE R2 IS STILL IN WORK\\\\\\\\\\\\\\\\\\\\\\\\


/////////HOW TO SETUP////////////

1. Clone the project
git clone <your-repository-url>
cd pdf-chatbot
2. Backend setup
cd backend

uv venv
.venv\Scripts\activate

uv sync

Create:

backend/.env

Add:

# Application
APP_ENV=development

# Database
DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>/<database>

# Gemini
GEMINI_API_KEY=<your-gemini-api-key>

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=documents

# JWT
JWT_SECRET_KEY=<your-secret-key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Cloudflare R2
R2_ACCOUNT_ID=<your-account-id>
R2_ACCESS_KEY_ID=<your-access-key>
R2_SECRET_ACCESS_KEY=<your-secret-key>
R2_BUCKET_NAME=<your-bucket-name>
R2_ENDPOINT=<your-r2-endpoint>

# LangSmith
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=<your-langsmith-api-key>
LANGCHAIN_PROJECT=pdf-chatbot

Keep .env out of Git. Add .env to .gitignore.

3. Start Qdrant
docker run -d ^
  --name qdrant ^
  -p 6333:6333 ^
  -p 6334:6334 ^
  qdrant/qdrant

Qdrant dashboard:

http://localhost:6333/dashboard
4. Run database migrations
uv run alembic upgrade head
5. Start FastAPI
uv run uvicorn main:app --reload

API documentation:

http://localhost:8000/docs
6. Frontend setup
cd frontend
npm install
npm run dev

Frontend:

http://localhost:3000
Required Services

Before running the complete application, make sure these are available:

PostgreSQL (Neon)
Gemini API
Qdrant
Cloudflare R2
LangSmith






/////////ABOUT PDF CHATBOT\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\





An AI-powered PDF chatbot that allows users to upload PDF documents and ask questions about their content.

The project uses RAG (Retrieval-Augmented Generation) to find relevant information from uploaded documents before generating answers.

## Tech Stack

- Next.js — Frontend
- FastAPI — Backend API
- PostgreSQL — Application database
- Qdrant — Vector database
- Gemini — Embeddings and LLM
- LangChain — AI/RAG utilities
- LangGraph — RAG workflow
- Cloudflare R2 — PDF file storage
- LangSmith — AI tracing and monitoring
- Docker — Deployment and containerization

## Architecture

```text
User
 │
 ▼
Next.js
 │
 ▼
FastAPI
 │
 ├── PostgreSQL
 │     └── Users, Documents, Conversations, Messages
 │
 ├── Cloudflare R2
 │     └── PDF Files
 │
 ├── Qdrant
 │     └── Document Embeddings
 │
 └── LangGraph
       │
       ├── Retrieve
       ├── Validate
       ├── Generate
       └── Respond


How It Works
1. Upload PDF
PDF
 ↓
FastAPI
 ↓
Cloudflare R2
 ↓
PDF Parser
 ↓
Text Chunks
 ↓
Gemini Embeddings
 ↓
Qdrant


2. Ask a Question
Question
 ↓
Embedding
 ↓
Qdrant Search
 ↓
Relevant Chunks
 ↓
LangGraph
 ↓
Gemini
 ↓
Answer + Sources
3. Chat Memory

Conversations and messages are stored in PostgreSQL so users can continue previous conversations.

4. Streaming

The chatbot supports SSE streaming so answers can be displayed progressively instead of waiting for the complete response.

Main Features
PDF upload
PDF text extraction
Document chunking
Vector embeddings
Semantic search
RAG-based question answering
LangGraph workflow
Conversation history
Persistent chat
Multi-document support
Streaming AI responses
Source references
Authentication
Cloud storage
AI observability
Docker deployment


Project Flow
Upload PDF
    ↓
Store PDF
    ↓
Parse
    ↓
Chunk
    ↓
Embed
    ↓
Qdrant
    ↓
Ask Question
    ↓
Retrieve
    ↓
LangGraph
    ↓
Gemini
    ↓
Stream Answer
    ↓
Show Sources