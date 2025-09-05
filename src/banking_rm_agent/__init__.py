"""
Banking RM Agent - Main Package

A comprehensive AI-powered banking relationship manager system built with CrewAI.
"""

__version__ = "1.0.0"
__author__ = "Banking RM Agent Team"
__email__ = "support@bankingrmagent.com"

from .core.banking_rm_agent import BankingRMAgent
from .core.config import Config
from .agents.authentication_agent import AuthenticationAgent, CustomerProfile, AuthResult, CustomerTier, AccountStatus

__all__ = ["BankingRMAgent", "Config", "AuthenticationAgent", "CustomerProfile", "AuthResult", "CustomerTier", "AccountStatus"]