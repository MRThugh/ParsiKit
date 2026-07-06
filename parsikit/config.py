"""
parsikit.config
~~~~~~~~~~~~~~~
Global configuration manager for ParsiKit 3.0.0.
"""

from __future__ import annotations


class ParsiKitConfig:
    """Global configuration manager to alter default behaviors across the framework."""
    def __init__(self) -> None:
        self.default_tax_rate: float = 0.10
        self.default_currency: str = "toman"
        self.enable_cache: bool = True

    def reset_defaults(self) -> None:
        """Reset configuration to initial state."""
        self.default_tax_rate = 0.10
        self.default_currency = "toman"
        self.enable_cache = True


config = ParsiKitConfig()