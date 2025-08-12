"""Configuration management for SG Money Buddy"""

import os
from typing import Optional


class Config:
    """Application configuration"""
    
    def __init__(self):
        self.telegram_token: Optional[str] = os.getenv('TELEGRAM_BOT_TOKEN')
        self.webhook_url: Optional[str] = os.getenv('WEBHOOK_URL')
        self.database_url: str = os.getenv('DATABASE_URL', 'sqlite:///./sg_finance_bot.db')
        self.openai_api_key: Optional[str] = os.getenv('OPENAI_API_KEY')
        self.secret_key: str = os.getenv('SECRET_KEY', 'dev-secret-key')
        self.app_env: str = os.getenv('APP_ENV', 'development')
        self.default_currency: str = os.getenv('DEFAULT_CURRENCY', 'SGD')
        self.timezone: str = os.getenv('TIMEZONE', 'Asia/Singapore')
    
    @property
    def is_production(self) -> bool:
        return self.app_env == 'production'
    
    @property
    def is_development(self) -> bool:
        return self.app_env == 'development'
