# Privacy & Security

## Data Minimization

ECG-QI is designed with minimal data collection:

- **No Direct Identifiers Stored**: No names, health card numbers, addresses, dates of birth, phone numbers
- **Anonymized Patient ID**: System-generated reference only
- **Age Range**: Stored as ranges (e.g., "30-40") not exact birth dates
- **Clinical Context**: De-identified presentation only
- **No Healthcare Numbers**: Regional health identification numbers not stored

## De-identification Assumptions

This MVP assumes:
1. Hospital has already de-identified cases before upload
2. Clinicians understand not to include identifiers in clinical_context
3. ECG images themselves do not contain patient demographics
4. No metadata from ECG files is preserved

**For production:** Automated de-identification scanning and masking would be required, potentially using third-party privacy libraries.

## File Security

### Upload Handling
- **UUID Filenames**: Original filenames never used; files stored with UUIDs
- **MIME Type Validation**: Only PNG, JPG, JPEG, PDF accepted
- **File Size Limits**: Configurable max upload (MVP: 50MB)
- **Path Traversal Protection**: Uploaded files restricted to designated directory
- **Malware Scanning Placeholder**: Stub for future ClamAV or similar integration

### File Storage (MVP)
- Local Docker volume (not production-grade)
- Files not exposed via public URLs
- Backend serves files only to authorized users
- Future: S3/Azure Blob adapter pattern ready for production cloud storage

## Auditability

Every sensitive action creates an audit log entry:
- Case creation
- Interpretation submission
- AI analysis
- Expert review completion
- User authentication

**Audit logs include:**
- WHO (user_id, email)
- WHEN (timestamp, timezone)
- WHAT (action type, resource affected)
- METADATA (no PHI) - e.g., old vs. new status

**Audit logs exclude:**
- Patient identifiers
- Clinical content (not needed for audit)
- Passwords or tokens

## Role-Based Access Control

### Clinician
- Create cases
- View only own cases
- Enter interpretations
- View comparison results
- View expert feedback
- Access learning dashboard (own cases only)

### Expert Reviewer
- View review queue (major disagreements + high-confidence minor)
- Access assigned cases
- View clinician + AI interpretations
- Enter final assessment + feedback
- Complete reviews
- View basic analytics (anonymized)

### Administrator
- View all cases and users
- View system analytics (concordance trends, performance metrics)
- Manage demo accounts
- View audit logs
- Configure comparison thresholds
- Access system settings

### Authorization Enforcement
- Every API endpoint checks user.role
- Queries filtered by user ID (clinicians) or role (experts/admins)
- Front-end hides UI elements based on role
- Back-end returns 403 Forbidden for unauthorized access

## Input Validation

- **Pydantic Schemas**: All request/response data validated
- **Type Checking**: TypeScript frontend + Python type hints
- **Content Length Limits**: Text fields have max lengths
- **Enum Constraints**: Status, role, priority enforced at database level
- **Email Validation**: RFC 5322 format checks
- **No SQL Injection**: SQLAlchemy ORM used throughout

## Secure Passwords

- **Hashing**: bcrypt with salt (Passlib library)
- **Requirements** (configurable):
  - Minimum length
  - Demo accounts clearly marked development-only
- **Token Security**:
  - JWT with HS256 algorithm
  - Short access token expiry (30 min default)
  - Refresh tokens with longer expiry (7 days)
  - Tokens stored in httpOnly cookies (frontend can be improved)

## Authentication Error Messages

- Generic error: "Invalid email or password"
- Does not reveal whether email exists in system
- Prevents user enumeration attacks

## Secure Headers

- CORS configured via environment variables
- Content-Type validation
- No sensitive information in response headers
- No server software version disclosure

## Logging

- **Structured Logging**: JSON format for machine readability
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **PHI Protection**: Clinical content not logged
- **Error Handling**: Specific errors logged server-side, generic messages to client

## Exception Handling

- No raw Python tracebacks returned to frontend
- Detailed errors logged server-side with context
- Client receives structured error responses:
  ```json
  {
    "error": "Case not found",
    "code": "CASE_NOT_FOUND",
    "details": null
  }
  ```

## Database Security

- **Parameterized Queries**: SQLAlchemy prevents SQL injection
- **Indexes**: On common queries (user lookups, status filters)
- **Transactions**: ACID compliance for data integrity
- **Connection Pooling**: Secure reuse of database connections
- **Password in Environment**: Database credentials never in code

## MVP Limitations & Production Gaps

### Not Implemented in MVP
- ❌ PHIPA Compliance audit (required for Canadian hospitals)
- ❌ HIPAA compliance (required for US hospitals)
- ❌ Medical device certification
- ❌ Formal penetration testing
- ❌ Encryption at rest
- ❌ Encryption in transit (no TLS in dev)
- ❌ Multi-factor authentication
- ❌ Single Sign-On (SSO) integration
- ❌ Advanced threat detection
- ❌ Formal disaster recovery plan
- ❌ Automated backups
- ❌ Real-time monitoring/alerting
- ❌ Hardware security module (HSM) integration

### Production Requirements

Before deploying to a real hospital, you MUST:

1. **Privacy Compliance**
   - PHIPA/HIPAA audit by legal team
   - Privacy impact assessment (PIA)
   - Data processing agreements (DPA)
   - Ethics board approval

2. **Security**
   - Third-party penetration testing
   - Vulnerability assessment
   - SSL/TLS encryption
   - Encryption at rest (database)
   - Secure key management (not in code)
   - MFA enforcement
   - Session management hardening

3. **Clinical**
   - Clinical validation studies
   - Comparison against gold-standard diagnostics
   - Evidence of AI model performance
   - Physician training program

4. **Infrastructure**
   - Production database backups (daily)
   - Disaster recovery plan (RTO/RPO defined)
   - Load balancing and failover
   - Monitoring and alerting
   - Incident response procedures

5. **Audit & Logging**
   - Immutable audit trail (blockchain or certified log system)
   - Tamper detection
   - Regular audit log review
   - Long-term retention policies

6. **Data Handling**
   - Data retention schedules
   - Secure data deletion procedures
   - Export controls (if applicable)
   - Compliance with hospital data governance

## Security Disclaimer

ECG-QI is a proof-of-concept MVP for educational and development purposes only. It is **NOT** production-ready for use with real patient data. Any real hospital deployment requires:
- Formal security and privacy review by qualified professionals
- Compliance with applicable regulations (PHIPA, HIPAA, GDPR, etc.)
- Clinical validation
- Institutional ethics board approval
- Legal review and liability insurance

**Do not use this system with real patient data without these steps.**
