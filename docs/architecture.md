# Architecture

## System Overview

ECG-QI is a three-tier healthcare quality improvement platform:

### Layers

1. **Frontend (React + TypeScript)** - Professional healthcare UI with role-based views
2. **Backend (FastAPI + Python)** - REST API with business logic and AI orchestration
3. **Database (PostgreSQL)** - Persistent data storage with audit logging

### Data Flow

```
Clinician → Frontend UI → Backend API → Database
                ↓
            Mock AI Service
                ↓
         Comparison Engine
                ↓
         Expert Review Queue
                ↓
         Analytics & Audit
```

## Authentication Flow

1. User submits email/password
2. Backend validates and creates JWT access token (30 min) + refresh token (7 days)
3. Frontend stores tokens and includes in Authorization header
4. Refresh endpoint provides new access token before expiration
5. Logout invalidates tokens server-side

## ECG Processing Workflow

```
Case Created → Clinician Interprets → AI Analysis → Comparison
    ↓              ↓                      ↓             ↓
 Draft        Submitted            Processed      Agreement/Disagreement
                                        ↓
                                   Major Diff?
                                        ↓
                              → Expert Review Queue
```

## Expert Review Flow

1. Major disagreements auto-route to review queue
2. Expert reviewer accesses pending cases
3. Expert enters final assessment + feedback
4. System generates educational takeaways
5. Case transitions to "Completed"
6. Clinician views feedback in learning dashboard

## Database Schema

- **Users**: Clinicians, experts, administrators
- **ECGCases**: Anonymized patient cases with status tracking
- **ClinicianInterpretation**: Original clinician assessment
- **AIInterpretation**: Simulated AI-assisted analysis
- **ComparisonResult**: Automated comparison logic
- **ExpertReview**: Final expert assessment
- **AuditLog**: Complete action trail
- **Notifications**: User notifications

## Security Model

- Role-Based Access Control (RBAC)
  - Clinician: View own cases, enter interpretations, view feedback
  - Expert: Access review queue, complete reviews
  - Admin: View all cases, manage users, access analytics
- Data minimization: No patient identifiers stored
- Audit trail: All sensitive actions logged
- File security: UUID filenames, MIME type validation, size limits

## Deployment Architecture (Docker)

```
Docker Network
├── PostgreSQL (port 5432)
├── Backend (port 8000) → Uvicorn + FastAPI
└── Frontend (port 5173) → React Dev Server
```

## Future Scaling Considerations

- External AI service integration (stub implemented)
- Cloud file storage (S3/Azure Blob adapter pattern)
- Message queue for async processing (Celery/RabbitMQ)
- Redis for caching and sessions
- Multi-hospital support with data isolation
- Real EMR integration
