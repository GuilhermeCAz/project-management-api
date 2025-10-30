"""Application configuration settings.

This module defines configuration classes for different environments.
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
basedir = Path(__file__).resolve().parent


class Config:
    """Base configuration class with common settings."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{basedir / "project_management.db"}',
    )
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    """Testing environment configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret-key'  # noqa: S105


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
