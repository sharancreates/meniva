# Security Policy

Selene is designed from the ground up as a **privacy-first, zero-knowledge menstrual and hormonal health platform**. We treat user health confidentiality, cryptographic integrity, and data sovereignty as fundamental rights.

---

## Supported Versions

Only the latest release on the default branch receives active security updates and patches.

| Version | Supported          |
| :------ | :----------------- |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

---

## Cryptographic Threat Model & Security Boundaries

Selene enforces a strict client-side envelope encryption architecture:

1. **Client-Side Envelope Encryption**:
   - Health observations, symptom ratings, cycle indicators, and personal notes are encrypted in the client's browser using AES-GCM (256-bit) before transmission over TLS.
   - The Data Encryption Key (DEK) is wrapped client-side using a Key Encryption Key (KEK) derived from the user's PIN using PBKDF2-HMAC-SHA256 (100,000 iterations) with a unique salt.
   - The raw PIN and raw DEK **never touch the server in plaintext**.

2. **Server-Side Zero-Knowledge**:
   - The backend stores and processes ciphertext. A breach of the backend database exposes only encrypted blobs.
   - Session authentication uses HttpOnly, SameSite=Strict cookies with Argon2id PIN verification and JWT revocation tracking backed by Redis (with database fallback).

---

## Reporting a Vulnerability

If you discover a security vulnerability—especially involving cryptographic implementations, key derivation, authentication bypass, or data leakage—**please do NOT report it through a public GitHub issue**.

### Preferred Disclosure Channel

1. **GitHub Security Advisories (Recommended)**:
   Navigate to the [Security Tab](../../security/advisories/new) of this repository and select **"Report a vulnerability"** to open a confidential draft advisory.
2. **Email Disclosure**:
   If private GitHub advisories are unavailable, please email the project maintainer at `security@selenehealth.org` (or open a minimal issue requesting private contact).

### What to Include in Your Report

To help us triage and resolve the issue quickly, please provide:
- A clear description of the vulnerability and its potential impact.
- Step-by-step reproduction instructions or a minimal Proof of Concept (PoC).
- Affected components (backend endpoints, client crypto utility, database models).
- Any proposed remediation or patches, if available.

### Response Timeframes

- **Initial Response & Acknowledgment**: Within 48 hours of receipt.
- **Triage & Severity Assessment**: Within 5 business days.
- **Fix & Public Advisory**: Coordinated disclosure within 30 to 60 days, depending on severity and complexity.

---

## In-Scope vs. Out-of-Scope

### In-Scope
- Compromise of client-side envelope encryption or cryptographic key derivation.
- Leakage of plaintext health data in backend logs, API responses, or error traces.
- Authentication bypass, session fixation, or token forgery.
- SQL injection, remote code execution, or path traversal.
- Cross-Site Request Forgery (CSRF) or Cross-Site Scripting (XSS).
- Bypasses of K-anonymity (K < 5) on public health aggregation endpoints.

### Out-of-Scope
- Attacks requiring physical access to an unlocked client device.
- Social engineering against users or maintainers.
- Distributed Denial of Service (DDoS) or network-layer volumetric attacks.
- Theoretical vulnerabilities without practical exploitability.

---

## Safe Harbor

We consider activities conducted in accordance with this policy to be authorized conduct. We will not pursue legal action against researchers who:
- Make a good-faith effort to avoid privacy violations, data destruction, and service interruption.
- Give us reasonable time to remediate the vulnerability before publicly disclosing details.
- Do not exploit a discovered vulnerability beyond the minimum necessary to demonstrate proof-of-concept.
