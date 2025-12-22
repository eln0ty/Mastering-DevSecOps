"""
Custom Security Check: B901 - PII Leak Detection
=================================================
This module implements a custom Bandit security rule that detects when
sensitive information (tokens, secrets, passwords) is being logged.

Rule ID: B901
Severity: HIGH
Confidence: HIGH
"""

import bandit
from bandit.core import test_properties as test


@test.checks('Call')
@test.test_id('B901')
def enterprise_pii_check(context):
    """
    Custom Bandit Rule: Detects PII leaks in logging statements.
    
    This rule scans for logging calls that contain sensitive variable names
    such as 'token', 'secret', or 'password' in their arguments.
    """
    
    # Define logging sinks to monitor
    logging_sinks = [
        'logger.info',
        'logger.error',
        'logger.warning',
        'logger.debug',
        'logger.critical',
        'print',
        'log.info',
        'log.error'
    ]
    
    # Check if this is a call to a logging function
    if context.call_function_name_qual in logging_sinks:
        
        # Analyze each argument passed to the logging function
        for arg in context.call_args:
            arg_string = str(arg).lower()
            
            # Define sensitive keywords that should not be logged
            sensitive_keywords = [
                'token', 'secret', 'password', 'api_key', 'apikey', 'auth', 'credential'
            ]
            
            # Check if any sensitive keyword appears in the logging call
            for keyword in sensitive_keywords:
                if keyword in arg_string:
                    return bandit.Issue(
                        severity=bandit.HIGH,
                        confidence=bandit.HIGH,
                        text=f"CRITICAL: PII/Secret Leak detected in logs! "
                             f"Sensitive data '{keyword}' found in logging statement. "
                             f"Never log authentication tokens, passwords, or secrets.",
                        lineno=context.node.lineno,
                        col_offset=context.node.col_offset
                    )
    
    # No vulnerability found
    return None