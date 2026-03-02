---
id: skill_feature_interrogator
name: Feature Requirement Architect
version: 1.0.0
description: Intercepts requests for new major features (Auth, Payments, Chat, etc.) and triggers a structured interview to eliminate ambiguity before coding begins.
tags: [requirements, architecture, planning, product-management]
permissions: [read_history, write_file]
---

# Feature Requirement Architect

## Overview
Coding without a spec leads to refactoring. This skill acts as a gatekeeper. When a user asks to "implement X," this skill pauses execution to ask critical architectural questions tailored to the specific domain (Authentication, Data, UI, etc.).

## Triggers
* **Phrase Detection:** "Implement [Feature]", "Create a [Feature] system", "Add [Feature]".
* **Condition:** The request lacks specific technical constraints (e.g., "Add login" vs "Add Firebase Google Login with JWT").

## Domain Question Matrices

### 1. Authentication & Identity
* **Primary Method:** Email/Password, OTP (SMS/WhatsApp), or Social (Google/Apple)?
* **Backend Strategy:** Laravel Sanctum (Stateful vs Token) or Firebase Auth?
* **Session Management:** Single device login or Multi-device?
* **Persistence:** `flutter_secure_storage` or `SharedPreferences`?
* **Recovery:** Link-based reset or OTP reset?

### 2. CRUD / Data Features
* **Storage:** Local (SQLite/Hive) or Remote (API)?
* **Offline Policy:** Optimistic UI (show now, sync later) or blocking loader?
* **Pagination:** Infinite Scroll or Page Numbers?
* **Destruction:** Hard delete or Soft delete (`deleted_at`)?

### 3. File/Media Uploads
* **Hosting:** AWS S3, local server storage, or Cloudinary?
* **Processing:** Client-side compression or Server-side resizing?
* **Restrictions:** Max file size? Allowed types?

## Prompts

### `conduct_interview`
**Input:** Feature Name (e.g., "Notifications")
**Logic:**
1.  Identify the domain.
2.  Select relevant questions from the Matrix.
3.  Add context-specific questions based on the current tech stack (Flutter/Laravel).

**Template Output:**
> "Before we start coding the **Notification System**, I need to clarify a few architectural details to ensure it fits your stack:
>
> 1.  **Provider:** Are we using Firebase Cloud Messaging (FCM) or a custom WebSocket solution?
> 2.  **Targeting:** Is this for individual users, topics, or geofencing?
> 3.  **Interaction:** What happens when the user taps a notification? (Deep link to specific screen?)
> 4.  **History:** Should notifications be saved in a local database for an 'Inbox' view?"

### `generate_spec`
**Trigger:** User answers the interview questions.
**Action:** Compiles the answers into a formal Requirement Spec file.
**Target Path:** `docs/specs/[Feature_Name]_Requirements.md`

**Template Output:**
```markdown
# Authentication Requirements

## Technical Decisions
- **Provider:** Laravel Sanctum (API Tokens)
- **Client:** Email & Password + Google OAuth
- **Session:** Multi-device allowed; Tokens expire in 30 days.

## Implementation Plan
1.  [Backend] Install Sanctum & Configure Socialite.
2.  [Flutter] Implement `AuthRepository` with `dio` interceptors.
3.  [UI] Create Login Screen with 'Continue with Google' button.