# app/core/config.py
"""
Configuration settings for the PetCare API.

This file centralizes all configuration so you can easily change settings
for different environments (development, testing, production) without
touching your actual code.
"""

from pydantic_settings import BaseSettings,SettingsConfigDict
#pydantic_settings is a library that reads settings from two places:
  #Your .env file (a private file you never share)
  #Default values you define in code
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Think of this like a control panel for your entire application.
    Instead of hardcoding values throughout your code, you define them
    once here and reference them everywhere else.
    """

    # Application metadata
    app_name: str = "PetCare API"
    app_version: str = "1.0.0"

    # Database configuration
    # For development, we'll use SQLite (a simple file-based database)
    # In production, you'd use PostgreSQL or MySQL
    database_url: str = "sqlite:///./fallback.db"  #fallback value

    # API configuration
    api_prefix: str = "/api/v1"
    # In production, you'd set this to False so you don't accidentally expose sensitive info in logs.
    debug: bool = True  # controls whether extra information (like SQL queries) gets printed to the terminal


    class Config:
        # This tells Pydantic to load values from a .env file
        # env_file = ".env"
        # Pydantic V2 configuration
        model_config = SettingsConfigDict(env_file=".env")


@lru_cache()# allows you to quickly add a cache to your functions.
# When applied, it stores the results of function calls with particular arguments, and if the function is called again with those same arguments,
# it returns the cached result instead of recomputing.
def get_settings() -> Settings:
    """
    Create and cache settings instance.

    The @lru_cache decorator ensures we only create one Settings object
    and reuse it everywhere. This is more efficient than creating a new
    Settings object every time we need configuration.

    Returns:
        Settings: The application configuration object
    """
    return Settings()