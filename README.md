# Job Application Automation System

**A complete full-stack application for automating job applications using AI agents**

An autonomous multi-agent AI system that applies to job openings on your behalf. Six specialized AI agents coordinate through LangGraph to scrape jobs, customize resumes, handle form filling, and track applications - all while maintaining human oversight and comprehensive monitoring.

**Current Version:** 0.1.0 MVP  
**Current Phase:** Phase 1 - Foundation & Core Infrastructure  
**Architecture:** Multi-Agent System with LangGraph  
**Last Updated:** 2025-12-30

---

## 🎯 Project Overview

### What This System Does

This is a complete job application automation platform that:

1. **Automatically finds jobs** - Scrapes job boards every 3 hours (Indeed, Greenhouse, Workday, LinkedIn)
2. **Matches jobs to you** - Uses AI embeddings to calculate match scores (0-100) based on your profile
3. **Customizes your resume** - AI tailors your resume for each job using LLMs (OpenAI, Claude, Gemini, Groq)
4. **Generates cover letters** - Creates personalized cover letters for each application
5. **Fills application forms** - Automatically navigates and fills job application forms
6. **Handles security** - Detects and solves CAPTCHAs using vision AI
7. **Tracks everything** - Monitors application status, email responses, and syncs to Google Sheets
8. **Keeps you in control** - Human approval before each submission, screenshots for review

### Key Features

- 🤖 **6 Specialized AI Agents** coordinated by LangGraph
- 🎯 **AI-Powered Job Matching** using vector similarity (pgvector)
- 📝 **Intelligent Resume Customization** per job with ATS optimization
- ✍️ **Context-Aware Cover Letters** generated for each application
- 🤖 **Automated Form Filling** with Playwright browser automation
- 🔒 **CAPTCHA Solving** using vision models and fallback services
- 📊 **Comprehensive Tracking** with Google Sheets sync
- 👁️ **Human-in-the-Loop** approval system
- 📈 **Full Observability** with LangSmith, Prometheus, and Grafana

---

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (Frontend)                 │
│              React + TypeScript + Vite + Tailwind            │
│  - Dashboard with agent status                              │
│  - Job listings and filters                                 │
│  - Application history                                      │
│  - Profile management                                        │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
┌──────────────────────▼──────────────────────────────────────┐
│              Backend API (FastAPI)                           │
│  - Authentication & Authorization                            │
│  - Job management                                           │
│  - Application tracking                                     │
│  - Agent control endpoints                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│         Multi-Agent System (LangGraph)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Job Hunter   │→ │ Content Gen  │→ │ Application  │     │
│  │   Agent      │  │    Agent     │  │    Agent     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Security    │  │  Monitoring  │  │ Communication│     │
│  │   Agent      │  │    Agent     │  │    Agent     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Database (PostgreSQL + pgvector)               │
│  - User data & profiles                                      │
│  - Job listings with embeddings                             │
│  - Application history                                      │
│  - Agent execution tracking                                 │
└─────────────────────────────────────────────────────────────┘
```

### Multi-Agent Workflow

```
[Job Hunter Agent]
    ↓ Finds new jobs
[Content Generator Agent]
    ↓ Creates resume + cover letter
[Application Agent]
    ↓ Fills form, captures screenshot
[HUMAN APPROVAL] ✋
    ↓ User reviews and approves
[Application Agent] → [Security Agent] (if CAPTCHA)
    ↓ Submits application
[Monitoring Agent]
    ↓ Tracks status changes
[Communication Agent]
    ↓ Syncs to Google Sheets + Sends notifications
```

---

## 📁 Project Structure

```
job-apply-app/                    # Root directory
│
├── applier/                      # Backend + AI System
│   ├── app/                      # Main application
│   │   ├── api/                  # REST API endpoints
│   │   ├── agents/               # 6 AI agents (LangGraph)
│   │   ├── core/                 # Config, logging, exceptions
│   │   ├── models/               # Database models (SQLAlchemy)
│   │   ├── schemas/              # Pydantic validation schemas
│   │   ├── services/             # Business logic
│   │   └── db/                   # Database connection
│   ├── alembic/                  # Database migrations
│   ├── storage/                  # File storage (resumes, screenshots)
│   ├── tests/                    # Test suite
│   ├── main.py                   # FastAPI entry point
│   └── README.md                 # Backend-specific documentation
│
├── frontend/                     # Frontend (React + TypeScript)
│   └── (to be initialized)
│
├── shared/                       # Shared TypeScript types
│   └── types/
│
├── README.md                     # This file (overall project)
├── CLAUDE.md                     # Detailed development guide
└── LOGS.md                       # Implementation history
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** with UV package manager
- **PostgreSQL 14+** with pgvector extension (running locally)
- **Node.js 18+** (for frontend, when ready)
- **API Keys:**
  - At least one LLM provider: OpenAI, Anthropic, Google, or Groq
  - LangSmith (optional but recommended for agent monitoring)

### Backend Setup

```bash
# 1. Navigate to backend
cd applier

# 2. Install dependencies
uv pip install -r requirements.txt

# 3. Create .env file (copy from CLAUDE.md template)
# Edit with your database URL and API keys

# 4. Set up PostgreSQL database
createdb job_applier
psql job_applier -c "CREATE EXTENSION vector;"

# 5. Run database migrations (after models are created)
uv run alembic upgrade head

# 6. Start development server
uv run uvicorn main:app --reload --port 8000

# Server at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Frontend Setup (Coming Soon)

```bash
cd frontend
npm install
npm run dev
# Frontend at http://localhost:5173
```

---

## 🤖 Multi-Agent System

### The 6 Agents

1. **Job Hunter Agent** - Scrapes jobs, calculates match scores, removes duplicates
2. **Content Generator Agent** - Customizes resumes and generates cover letters
3. **Application Agent** - Fills forms, uploads documents, captures screenshots
4. **Security Agent** - Detects and solves CAPTCHAs
5. **Monitoring Agent** - Tracks application status, monitors emails
6. **Communication Agent** - Syncs to Google Sheets, sends notifications

### How They Work Together

- **LangGraph** orchestrates all agents with state management
- **PostgreSQL** stores agent state for persistence
- **Conditional routing** between agents based on outcomes
- **Human approval** checkpoints before submissions
- **Error recovery** with automatic retries

---

## 🛠️ Technology Stack

### Backend & AI
- **Python 3.13+** with UV package manager
- **FastAPI** - REST API framework
- **LangGraph** - Multi-agent orchestration
- **LangChain** - LLM tools and components
- **PostgreSQL + pgvector** - Database with vector similarity
- **SQLAlchemy 2.0** - ORM
- **Playwright** - Web automation
- **Multi-Provider LLMs** - OpenAI, Anthropic, Google, Groq

### Frontend (Planned)
- **React 18+** + **TypeScript 5+**
- **Vite** - Fast bundler
- **Tailwind CSS** - Styling
- **React Query** - Server state
- **Zustand** - Client state

### Monitoring
- **LangSmith** - Agent observability
- **Prometheus** - Metrics collection
- **Grafana** - Visualization dashboards

---

## 📊 Database Schema

### Core Tables

1. **users** - User authentication
2. **user_profiles** - User info, job preferences, auto-apply settings
3. **jobs** - Scraped jobs with pgvector embeddings and match scores
4. **applications** - Application history with screenshots and status
5. **documents** - Resumes and cover letters (PDF + markdown)
6. **agent_runs** - Agent execution tracking
7. **sync_logs** - Google Sheets sync logs

**Key Features:**
- pgvector extension for AI-powered job matching
- JSONB columns for flexible agent metrics
- Strategic indexes for performance

---

## 📋 Development Roadmap

### Phase 1: Foundation (Week 1-2) - **CURRENT** ✅
- Project structure ✅
- Core configuration ✅
- Database setup
- Authentication system
- Basic API endpoints

### Phase 2: Content Generation (Week 2-3)
- Content Generator Agent
- Resume customization
- Cover letter generation

### Phase 3: Job Scraping (Week 3-4)
- Job Hunter Agent
- Job board scrapers
- Vector embeddings and matching

### Phase 4: Application Automation (Week 4-5)
- Application Agent
- Form filling
- Screenshot capture

### Phase 5: Multi-Agent Orchestration (Week 5-6)
- LangGraph workflow
- All 6 agents coordinated
- Human approval system

### Phase 6: Integration & Monitoring (Week 6-7)
- Communication Agent
- Google Sheets sync
- Prometheus + Grafana

### Phase 7: Frontend (Week 7-9)
- React UI
- Agent monitoring dashboard
- Job listing and application pages

### Phase 8: Testing & Refinement (Week 9-10)
- Comprehensive testing
- Performance optimization
- Production deployment

---

## 📚 Documentation

- **README.md** (this file) - Overall project overview
- **applier/README.md** - Backend and AI system details
- **CLAUDE.md** - Comprehensive development guide with patterns and best practices
- **LOGS.md** - Implementation history and changes

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in `applier/` directory. See `CLAUDE.md` for complete template.

**Required:**
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- At least one LLM API key (OpenAI, Anthropic, Google, or Groq)

**Optional:**
- `LANGCHAIN_API_KEY` - For LangSmith observability
- `GOOGLE_SHEETS_CREDENTIALS_PATH` - For Google Sheets sync
- CAPTCHA service keys

---

## 🎯 Current Status

### ✅ Completed (Phase 1 - Foundation)
- ✅ Project structure setup
- ✅ Core configuration system (`app/core/config.py`)
- ✅ Custom exception hierarchy (`app/core/exceptions.py`)
- ✅ Logging configuration (`app/core/logging.py`)
- ✅ Database connection layer (`app/db/base.py`, `app/db/session.py`)
- ✅ API route stubs (all 6 route files created)
- ✅ API middleware setup
- ✅ Requirements.txt with multi-provider LLM support
- ✅ Alembic configuration

### 🚧 In Progress
- Database models (to be created)
- Authentication system (to be created)
- Initial migrations (to be created)

### 📅 Next Steps
1. Create database models (users, user_profiles, jobs, applications, etc.)
2. Create initial Alembic migration
3. Implement authentication (JWT)
4. Implement API endpoints (replace stubs)
5. Implement first agent (Job Hunter)

---

## 🤝 Contributing

This is a personal project. Contributions welcome after MVP completion.

---

## 📄 License

MIT License

---

**Built with LangGraph, FastAPI, PostgreSQL, and Multi-Provider LLMs**  
**Monitored with LangSmith, Prometheus, and Grafana**

