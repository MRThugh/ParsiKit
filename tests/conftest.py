"""
Pytest configuration and shared fixtures for ParsiKit tests.
"""
import pytest
import parsikit


@pytest.fixture(autouse=True)
def reset_parsikit_config():
    """Reset configuration before each test execution."""
    parsikit.config.reset_defaults()
    yield
    parsikit.config.reset_defaults()
