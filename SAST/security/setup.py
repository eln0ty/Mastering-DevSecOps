"""
Setup Configuration for Custom Security Rules
==============================================
This setup.py allows the custom Bandit rules to be installed as a package,
making them available to Bandit's plugin system.
"""

from setuptools import setup, find_packages

setup(
    name='enterprise-security-rules',
    version='1.0.0',
    description='Custom Bandit security rules for enterprise PII leak detection',
    author='Security Team',
    author_email='security@company.com',
    packages=find_packages(),
    install_requires=[
        'bandit>=1.7.0',
    ],
    entry_points={
        'bandit.plugins': [
            # Register the custom check with Bandit
            'B901 = security.custom_checks:enterprise_pii_check',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Security',
    ],
    python_requires='>=3.8',
)