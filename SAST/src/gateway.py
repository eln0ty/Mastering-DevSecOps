"""
Payment Gateway Module - VULNERABLE VERSION
============================================
This module contains intentional security vulnerabilities for demonstration purposes.

Vulnerabilities Included:
1. Hardcoded API Secret (Line 10)
2. PII Leak in Logs (Line 18)
3. SQL Injection (Line 22)
"""

import logging
import sqlite3

# [VULNERABILITY 1] SECRET LEAK: Hardcoded API Key
# Severity: CRITICAL
# Issue: API credentials should never be hardcoded in source code
# Solution: Use environment variables or secure vault services
STRIPE_API_KEY = "sk_live_51MzXjL2e3B4f5g6h7i8j9k0l"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PaymentGateway")


def process_payment(user_id, auth_token):    
    # [VULNERABILITY 2] PII LEAK: Logging Sensitive Data
    # Severity: HIGH
    # Issue: Authentication tokens should never be logged
    # Solution: Sanitize logs by masking sensitive data
    # This will be caught by custom rule B901
    logger.info(f"User {user_id} initiated payment with token: {auth_token}")
    
    # [VULNERABILITY 3] SQL INJECTION
    # Severity: CRITICAL
    # Issue: User input directly concatenated into SQL query
    # Solution: Use parameterized queries or ORM
    db = sqlite3.connect("payments.db")
    query = f"SELECT * FROM transactions WHERE user_id = '{user_id}'"
    cursor = db.execute(query)
    
    # Simulate payment processing
    result = cursor.fetchall()
    db.close()
    
    return True


def validate_payment_card(card_number):
    # Additional vulnerable code could go here
    return len(card_number) == 16


if __name__ == "__main__":
    # Example usage - DO NOT RUN IN PRODUCTION
    process_payment("user_123", 5000, "tok_visa_4242")