"""
Custom Security Rules Package
==============================
This package contains custom Bandit security rules tailored for enterprise compliance.

Rules Included:
- B901: PII Leak Detection in Logging Statements
"""

__version__ = "1.0.0"
__author__ = "Security Team"

# Make custom checks available
from .custom_checks import enterprise_pii_check

__all__ = ['enterprise_pii_check']