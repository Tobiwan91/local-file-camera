"""Config flow for Local File Camera integration.

Generated with ha-integration@aurora-smart-home v1.0.0
https://github.com/tonylofgren/aurora-smart-home
"""

import hashlib
import os
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_NAME, CONF_FILE_PATH
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_REFRESH_INTERVAL,
    CONF_DEVICE_ID,
    DEFAULT_REFRESH_INTERVAL,
    DOMAIN,
    VALID_IMAGE_EXTENSIONS,
)


def _validate_file_path(hass: HomeAssistant, file_path: str) -> tuple[bool, str | None]:
    """Validate a file path.

    Returns:
        Tuple of (is_valid, error_key)
        error_key is None if valid, otherwise contains error message key
    """
    # Prevent directory traversal attacks
    if ".." in file_path:
        return False, "directory_traversal"

    # Must be absolute path
    if not os.path.isabs(file_path):
        return False, "not_absolute_path"

    # Check if file exists
    if not os.path.exists(file_path):
        return False, "file_not_found"

    # Check if it's a file (not a directory)
    if not os.path.isfile(file_path):
        return False, "not_a_file"

    # Check if file is readable
    if not os.access(file_path, os.R_OK):
        return False, "file_not_readable"

    # Check file extension
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in VALID_IMAGE_EXTENSIONS:
        return False, "invalid_image_format"

    # Try to read file header to validate it's actually an image
    try:
        with open(file_path, "rb") as f:
            header = f.read(2)

        # JPEG files should start with FF D8
        if ext.lower() in {".jpg", ".jpeg"} and header != b"\xff\xd8":
            return False, "invalid_image_file"
    except Exception:
        return False, "file_not_readable"

    return True, None


def _generate_device_id(file_path: str) -> str:
    """Generate a unique device ID from file path.

    Uses MD5 hash of the file path to create a stable, unique identifier.
    """
    return hashlib.md5(file_path.encode()).hexdigest()[:16]


class LocalFileCameraConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Local File Camera."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the file path
            is_valid, error_key = _validate_file_path(
                self.hass, user_input[CONF_FILE_PATH]
            )

            if is_valid:
                # Check if this file path is already configured
                device_id = _generate_device_id(user_input[CONF_FILE_PATH])

                await self.async_set_unique_id(f"{DOMAIN}_{device_id}")
                self._abort_if_unique_id_configured()

                # Create the config entry
                data = {
                    CONF_FILE_PATH: user_input[CONF_FILE_PATH],
                    CONF_NAME: user_input[CONF_NAME],
                    CONF_DEVICE_ID: device_id,
                    CONF_REFRESH_INTERVAL: user_input.get(
                        CONF_REFRESH_INTERVAL, DEFAULT_REFRESH_INTERVAL
                    ),
                }

                return self.async_create_entry(title=user_input[CONF_NAME], data=data)
            else:
                errors[CONF_FILE_PATH] = error_key

        # Show the form
        data_schema = vol.Schema(
            {
                vol.Required(CONF_FILE_PATH): str,
                vol.Required(CONF_NAME): str,
                vol.Optional(
                    CONF_REFRESH_INTERVAL, default=DEFAULT_REFRESH_INTERVAL
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=3600)),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return LocalFileCameraOptionsFlow(config_entry)


class LocalFileCameraOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Local File Camera."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle options flow."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_REFRESH_INTERVAL,
                    default=options.get(
                        CONF_REFRESH_INTERVAL,
                        self.config_entry.data.get(
                            CONF_REFRESH_INTERVAL, DEFAULT_REFRESH_INTERVAL
                        ),
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=3600)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema)
