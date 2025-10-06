"""Configuration manager for loading and managing application configs."""

import os
from typing import Dict, Any, Optional
from modules.paths import SAM2_CONFIGS_DIR
from modules.exceptions import ConfigurationError
from modules.logger_util import get_logger

logger = get_logger()


class ConfigManager:
    """Singleton configuration manager for the application."""

    _instance: Optional['ConfigManager'] = None

    def __new__(cls) -> 'ConfigManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._configs: Dict[str, Any] = {}
        self._load_configs()
        self._initialized = True

    def _load_configs(self) -> None:
        """Load all configuration files."""
        try:
            import yaml
        except ImportError:
            raise ConfigurationError(
                "PyYAML is required for configuration management. "
                "Install it with: pip install PyYAML"
            )
        
        try:
            # Load default hyperparameters
            default_hparam_path = os.path.join(
                SAM2_CONFIGS_DIR, "default_hparams.yaml")
            with open(default_hparam_path, 'r') as f:
                self._configs['default_hparams'] = yaml.safe_load(f)
                logger.info(
                    f"Loaded default hyperparameters from {default_hparam_path}")
        except FileNotFoundError as e:
            raise ConfigurationError(f"Configuration file not found: {e}")
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Error parsing YAML configuration: {e}")
        except Exception as e:
            raise ConfigurationError(
                f"Unexpected error loading configuration: {e}")

    @property
    def default_hparams(self) -> Dict[str, Any]:
        """Get default hyperparameters."""
        return self._configs.get('default_hparams', {})

    @property
    def mask_hparams(self) -> Dict[str, Any]:
        """Get mask generation hyperparameters."""
        return self.default_hparams.get("mask_hparams", {})

    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.

        Args:
            key: Configuration key (supports dot notation, e.g., 'mask_hparams.points_per_side')
            default: Default value if key is not found

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._configs

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def reload_configs(self) -> None:
        """Reload all configuration files."""
        self._configs.clear()
        self._load_configs()
        logger.info("Configuration reloaded")


# Convenience function to get the singleton instance
def get_config_manager() -> ConfigManager:
    """Get the ConfigManager singleton instance."""
    return ConfigManager()
