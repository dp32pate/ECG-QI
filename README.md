# ECG-QI: AI-Assisted ECG Quality Improvement Platform

A professional-grade quality improvement, audit, education, and peer-review platform for hospital ECG analysis.

## 🏥 Overview

ECG-QI is a healthcare quality improvement system that:
- Accepts anonymized ECG cases from clinicians
- Produces AI-assisted interpretations (non-diagnostic)
- Compares clinician and AI results
- Routes major disagreements to expert review
- Provides educational feedback and audit trails

**⚠️ MVP Disclaimer:** This is a proof-of-concept quality-improvement platform for development and testing only. The AI output is simulated, not clinically validated. Real hospital deployment would require formal privacy, security, legal, ethics, and clinical validation review.

## 🛠️ Technology Stack

### Frontend
- React + TypeScript
- Vite
- Tailwind CSS
- React Router
- TanStack Query
- React Hook Form + Zod
- Recharts
- Lucide React

### Backend
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT Authentication

### Infrastructure
- Docker & Docker Compose
- GitHub Actions CI/CD
- Pytest (backend)
- Vitest + React Testing Library (frontend)

## 📋 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+

### Local Installation

1. **Clone and navigate:**
```bash
git clone https://github.com/dp32pate/ECG-QI.git
cd ECG-QI
```

2. **Copy environment file:**
```bash
cp .env.example .env
```

3. **Start with Docker Compose:**
```bash
docker compose up --build
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Without Docker

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m scripts.seed_data
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 👥 Demo Credentials

For local development only:

| Role | Email | Password |
|------|-------|----------|
| Clinician | clinician@ecgqi.local | DemoPass123! |
| Reviewer | reviewer@ecgqi.local | DemoPass123! |
| Admin | admin@ecgqi.local | DemoPass123! |

Use the demo account buttons on the login page for quick testing.

## 📚 Documentation

- [Architecture](docs/architecture.md) - System design, data flow, workflows
- [Data Model](docs/data-model.md) - Database schema with ER diagram
- [Privacy & Security](docs/privacy-and-security.md) - Safeguards and MVP limitations
- [Limitations](docs/limitations.md) - Explicit constraints and non-clinical use

## 🧪 Testing

**Backend:**
```bash
cd backend
pytest --cov=app tests/
```

**Frontend:**
```bash
cd frontend
npm run test
```

**E2E (when implemented):**
```bash
npm run test:e2e
```

## 📊 MVP Completion Checklist

- [x] Repository structure and Docker setup
- [x] Environment configuration
- [ ] Database models and migrations
- [ ] Authentication and RBAC
- [ ] Case creation and file upload
- [ ] Mock AI analysis service
- [ ] Comparison engine
- [ ] Expert review workflow
- [ ] Dashboard and analytics
- [ ] Comprehensive testing
- [ ] Documentation

## 🚀 Implementation Phases

1. **Phase 1:** Repository structure, Docker, environment
2. **Phase 2:** Database models, authentication, seed data
3. **Phase 3:** Case management, file upload
4. **Phase 4:** Mock AI service, comparison logic
5. **Phase 5:** Expert reviews, dashboard, analytics
6. **Phase 6:** Testing, documentation, polish

## 🔐 Security & Privacy

Key safeguards:
- Password hashing with Passlib
- JWT access + refresh tokens
- Role-based access control (RBAC)
- Input validation with Pydantic
- Secure file handling (UUID filenames, MIME type validation)
- Audit logging for sensitive actions
- No patient identifiers in logs
- CORS configuration via environment variables

**Production Considerations:** Real hospital deployment requires:
- Formal PHIPA/HIPAA compliance review
- Medical device certification if applicable
- Clinical validation
- Formal ethics and privacy board approval
- Hospital security audit
- Integration with EMR systems
- Production-grade file storage (S3, Azure Blob)
- Proper database backups and recovery

## 📝 Current Limitations

- AI interpretations are simulated (not real ML models)
- Synthetic anonymized data only
- Local file storage (no cloud integration)
- No email notifications
- No billing or multi-tenant support
- Single-hospital scope

See [docs/limitations.md](docs/limitations.md) for details.

## 🛠️ Development

```bash
# Install dependencies
cd frontend && npm install
cd ../backend && pip install -r requirements.txt

# Run with Docker
docker compose up --build

# Run migrations
docker compose exec backend alembic upgrade head

# Seed demo data
docker compose exec backend python -m scripts.seed_data

# View logs
docker compose logs -f backend
docker compose logs -f frontend
```

## 📞 Support

This is an MVP for educational and demonstration purposes. For issues or questions, refer to the documentation or the project's issue tracker.

---

**Built with ❤️ for healthcare quality improvement.**
ECG Reading Quality Improvement Platform
