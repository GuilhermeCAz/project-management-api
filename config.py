"""Application configuration settings.

This module defines configuration classes for different environments.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


basedir = Path(__file__).resolve().parent


class Config:
    """Base configuration class with common settings."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{basedir / "project_management.db"}',
    )
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
