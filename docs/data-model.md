# Data Model

## Entity Descriptions

### User
Represents a platform user with role-based permissions.

**Fields:**
- `id` (UUID): Primary key
- `full_name` (str): User's name
- `email` (str): Unique email address
- `hashed_password` (str): bcrypt hashed password
- `role` (Enum): CLINICIAN, EXPERT, ADMIN
- `organization` (str): Hospital/clinic name
- `is_active` (bool): Account status
- `created_at` (datetime): Account creation
- `updated_at` (datetime): Last modification

**Constraints:** Email is unique, password must meet requirements

---

### ECGCase
Represents an anonymized ECG case awaiting or under review.

**Fields:**
- `id` (UUID): Primary key
- `case_number` (str): Human-readable identifier
- `anonymized_patient_id` (str): De-identified patient reference
- `patient_age_range` (str): e.g., "30-40", "40-50"
- `patient_sex` (Enum): M/F/Other
- `clinical_context` (text): Clinical presentation without identifiers
- `ecg_file_path` (str): Path to uploaded ECG (PNG/JPG/PDF)
- `ecg_file_type` (str): MIME type
- `uploaded_by` (FK: User): Uploading clinician
- `status` (Enum): DRAFT, SUBMITTED, AI_PROCESSING, COMPARED, REVIEW_REQUIRED, UNDER_EXPERT_REVIEW, EXPERT_REVIEW_COMPLETED, CLOSED
- `priority` (Enum): ROUTINE, URGENT, CRITICAL
- `created_at` (datetime): Case creation
- `updated_at` (datetime): Last status change

**Constraints:** Status follows defined workflow, clinician interpretation required before AI processing

---

### ClinicianInterpretation
Clinician's original ECG interpretation (preserved for audit).

**Fields:**
- `id` (UUID): Primary key
- `case_id` (FK: ECGCase): Associated case
- `clinician_id` (FK: User): Interpreting clinician
- `primary_diagnosis` (str): Main diagnosis
- `rhythm` (str): Cardiac rhythm (e.g., "Normal sinus rhythm", "Atrial fibrillation")
- `heart_rate` (int): BPM
- `findings` (list): Array of findings (e.g., ["ST elevation", "T wave inversion"])
- `interpretation_notes` (text): Free-text clinical notes
- `submitted_at` (datetime): Submission timestamp

**Constraints:** One per case, immutable after submission for audit purposes

---

### AIInterpretation
AI-assisted interpretation (for comparison, not diagnosis).

**Fields:**
- `id` (UUID): Primary key
- `case_id` (FK: ECGCase): Associated case
- `model_name` (str): e.g., "ECG-Mock-v1"
- `model_version` (str): Version number
- `primary_diagnosis` (str): Suggested diagnosis
- `rhythm` (str): Detected rhythm
- `heart_rate` (int): Calculated BPM
- `confidence_score` (float): 0.0-1.0
- `findings` (list): Detected findings
- `explanation` (text): How result was derived
- `raw_output` (json): Full AI model output
- `processing_status` (Enum): PENDING, COMPLETED, FAILED
- `created_at` (datetime): Analysis timestamp

**Constraints:** Clearly labeled as "AI-assisted preliminary analysis"

---

### ComparisonResult
Automated comparison between clinician and AI interpretations.

**Fields:**
- `id` (UUID): Primary key
- `case_id` (FK: ECGCase): Associated case
- `agreement_level` (Enum): AGREEMENT, MINOR_DIFFERENCE, MAJOR_DIFFERENCE
- `agreement_score` (float): 0.0-1.0 match percentage
- `diagnosis_match` (bool): Primary diagnoses match?
- `rhythm_match` (bool): Rhythms match?
- `heart_rate_difference` (int): BPM delta
- `differing_findings` (list): Fields that don't match
- `comparison_summary` (text): Human-readable summary
- `requires_expert_review` (bool): Auto-routed?
- `created_at` (datetime): Comparison timestamp

**Constraints:** Comparison rules stored in configuration

---

### ExpertReview
Expert reviewer's final assessment.

**Fields:**
- `id` (UUID): Primary key
- `case_id` (FK: ECGCase): Associated case (one per case)
- `reviewer_id` (FK: User): Expert reviewer
- `final_diagnosis` (str): Expert's final diagnosis
- `final_rhythm` (str): Expert's final rhythm
- `final_findings` (list): Expert's findings
- `discrepancy_category` (str): Root cause classification
- `severity` (Enum): MINOR, MODERATE, MAJOR
- `feedback` (text): Educational feedback for clinician
- `educational_takeaway` (text): Learning point
- `review_status` (Enum): PENDING, IN_PROGRESS, COMPLETED
- `started_at` (datetime): Review start time
- `completed_at` (datetime): Review completion time

**Constraints:** Only one review per case, initiated after major disagreements

---

### AuditLog
Complete audit trail of all sensitive actions.

**Fields:**
- `id` (UUID): Primary key
- `user_id` (FK: User): Acting user
- `action` (str): e.g., "case_created", "interpretation_submitted", "review_completed"
- `resource_type` (str): e.g., "ECGCase", "ExpertReview"
- `resource_id` (UUID): Affected resource ID
- `metadata` (json): Additional context (no PHI)
- `timestamp` (datetime): Action time
- `ip_address` (str, nullable): Source IP (privacy-respecting)

**Constraints:** Immutable, no PHI in metadata

---

### Notification
User notifications for case updates and reviews.

**Fields:**
- `id` (UUID): Primary key
- `user_id` (FK: User): Recipient
- `title` (str): Notification title
- `message` (text): Notification content
- `related_case_id` (UUID, nullable): Associated case
- `read` (bool): Read status
- `created_at` (datetime): Creation time

**Constraints:** One-way delivery (no email in MVP)

---

## ER Diagram

```
User (1) ──── (n) ECGCase
 |
 ├──── (1) ClinicianInterpretation (n)
 ├──── (1) ExpertReview (n)
 ├──── (1) AuditLog (n)
 └──── (1) Notification (n)

ECGCase (1) ──── (1) ClinicianInterpretation
ECGCase (1) ──── (1) AIInterpretation
ECGCase (1) ──── (1) ComparisonResult
ECGCase (1) ──── (1) ExpertReview
```

## Key Design Decisions

1. **Immutable Interpretations**: Clinician interpretations cannot be changed after submission (audit trail)
2. **Separate Expert Assessment**: Expert review stored separately to preserve original interpretations
3. **Timestamps on Everything**: `created_at` and `updated_at` for audit and analytics
4. **Enums for Status**: Database-level enforcement of valid state transitions
5. **UUID Primary Keys**: Better for distributed systems and privacy
6. **No Direct Patient Identifiers**: Anonymization enforced at schema level
7. **Role-Based Filtering**: Queries differ by user role (clinicians see own cases, admins see all)

## Indexes

- `ECGCase`: (status, priority, created_at), (uploaded_by, status)
- `AuditLog`: (user_id, timestamp), (resource_type, resource_id)
- `ClinicianInterpretation`: (case_id), (clinician_id)
- `ExpertReview`: (case_id), (reviewer_id), (review_status)
- `User`: (email), (organization)
