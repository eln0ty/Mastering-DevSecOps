# DevSecOps CI-Security Implementation

## Overview

This project demonstrates a **professional DevSecOps workflow** by implementing automated security quality gates in the CI (Continuous Integration) pipeline using GitHub Actions.

## Project Goals

1. **Shift Security Left**: Catch vulnerabilities before code reaches production
2. **Automation First**: Replace manual security reviews with automated scans
3. **Immutable Gates**: Prevent insecure code from being merged via CI enforcement
4. **Educational**: Demonstrate real-world security vulnerabilities and detection methods

---

## Architecture

### Three-Layered Security Defense

```
┌─────────────────────────────────────────┐
│         GitHub Actions Runner           │
├─────────────────────────────────────────┤
│  Layer 1: Secret Scanning (Gitleaks)    │
│  └─> Detects hardcoded credentials      │
├─────────────────────────────────────────┤
│  Layer 2: SCA - Dependency Scan (Safety)│
│  └─> Finds known CVEs in libraries      │
├─────────────────────────────────────────┤
│  Layer 3: SAST - Code Analysis (Bandit) │
│  └─> Custom rules for PII leaks         │
└─────────────────────────────────────────┘
```

---

## Intentional Vulnerabilities

This codebase contains **three intentional security vulnerabilities** for educational purposes:

### 1. **Hardcoded API Secret** (CRITICAL)

- **File**: `src/gateway.py`, Line 10
- **Issue**: Stripe API key hardcoded in source code
- **Detected By**: Gitleaks
- **Impact**: API key exposure could lead to unauthorized transactions

### 2. **Vulnerable Dependency** (HIGH)

- **File**: `requirements.txt`
- **Issue**: `requests==2.20.0` has CVE-2023-32681
- **Detected By**: Safety (SCA)
- **Impact**: Potential leak of Proxy-Authorization headers

### 3. **PII Leak in Logs** (HIGH)

- **File**: `src/gateway.py`, Line 18
- **Issue**: Authentication token logged in plain text
- **Detected By**: Bandit with custom rule B901
- **Impact**: Sensitive data exposure in log files

---

## How It Works

### The Professional Workflow

```
Developer Push → GitHub Actions Trigger → Security Scans Run
                                              ↓
                                         All Pass?
                                         ↙     ↘
                                      YES      NO
                                       ↓        ↓
                                   Merge OK   PR Blocked
```

### Why CI Pipeline Instead of Pre-Commit Hooks?

| Aspect                | Pre-Commit Hooks      | CI Pipeline     |
| --------------------- | --------------------- | --------------- |
| **Performance** | Slows local dev       | Runs on cloud   |
| **Bypass**      | `--no-verify` works | Cannot bypass   |
| **Consistency** | Dev-dependent         | Always same     |
| **Authority**   | Optional              | Source of truth |

---

## Quick Start

### Prerequisites

- GitHub repository with Actions enabled
- Python 3.8+
- Git

### Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone <your-repo-url>
   cd devsecops-ci-security
   ```
2. **Install dependencies** (optional for local testing):

   ```bash
   pip install -r requirements.txt
   ```
3. **Push code to trigger CI**:

   ```bash
   git add .
   git commit -m "Trigger security scan"
   git push origin main
   ```
4. **Check GitHub Actions**:

   - Go to your repository → Actions tab
   - Watch the security scans execute
   - See the vulnerabilities get caught! ❌

---

## Expected CI Output

When you push this code, the CI pipeline will **FAIL** with the following findings:

### ❌ Layer 1: Gitleaks

```
Finding: sk_live_51MzXjL2e3B4f5g6h7i8j9k0l
RuleID: generic-api-key
File: src/gateway.py:5
```

### ❌ Layer 2: Safety

```
Package: requests 2.20.0
CVE: CVE-2023-32681
Severity: HIGH
```

### ❌ Layer 3: Bandit

```
Issue: [B901] PII Leak detected in logs!
Location: src/gateway.py:13
Severity: HIGH
```

---

## Remediation Guide

### Fix Vulnerability #1: Hardcoded Secret

```python
# ❌ WRONG
STRIPE_API_KEY = "sk_live_51MzXjL2e3B4f5g6h7i8j9k0l"

# ✅ CORRECT
import os
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
```

### Fix Vulnerability #2: Vulnerable Dependency

```bash
# Update requirements.txt
requests==2.31.0  # or higher
```

### Fix Vulnerability #3: PII in Logs

```python
# ❌ WRONG
logger.info(f"User {user_id} initiated payment with token: {auth_token}")

# ✅ CORRECT
logger.info(f"User {user_id} initiated payment successfully")
```

---

## Testing Custom Rules Locally

You can test the custom Bandit rule locally:

```bash
# Install custom rule package
pip install ./security/

# Run Bandit with custom rule
bandit -r src/ -ll -t B901
```

---

# Next Steps

After understanding this basic implementation, consider:

1. **Add more layers**:

   - Container scanning (Trivy)
   - Infrastructure as Code scanning (Checkov)
   - License compliance (FOSSA)
2. **Implement runtime protection**:

   - Add DAST (Dynamic Application Security Testing)
   - Set up RASP (Runtime Application Self-Protection)
   - Configure SIEM for security monitoring
3. **Create security metrics**:

   - Track vulnerability trends
   - Measure mean time to remediation
   - Generate compliance reports

---

### Useful Commands

```bash
# Test Gitleaks locally
gitleaks detect --source . -v

# Test Safety locally
safety check -r requirements.txt

# Test Bandit with custom rules locally
pip install ./security/
bandit -r src/ -ll -t B901

# Run all scans locally (requires tools installed)
./gitleaks detect --source . -v && \
safety check -r requirements.txt && \
bandit -r src/ -ll -t B901
```
