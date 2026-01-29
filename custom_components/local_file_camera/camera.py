"""Camera entity for Local File Camera integration.

Generated with ha-integration@aurora-smart-home v1.0.0
https://github.com/tonylofgren/aurora-smart-home
"""

import hashlib
import os
from typing import cast

import aiofiles
from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_FILE_PATH
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.dt import utcnow
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_REFRESH_INTERVAL,
    CONF_DEVICE_ID,
    DEFAULT_REFRESH_INTERVAL,
    DOMAIN,
    VALID_IMAGE_EXTENSIONS,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Local File Camera entities from a config entry."""
    camera = LocalFileCamera(entry)
    async_add_entities([camera])


class LocalFileCamera(Camera):
    """Representation of a local file camera."""

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the camera."""
        super().__init__()
        self._entry = entry
        self._file_path = entry.data[CONF_FILE_PATH]
        self._name = entry.data[CONF_NAME]
        self._device_id = entry.data[CONF_DEVICE_ID]
        self._refresh_interval = entry.data.get(
            CONF_REFRESH_INTERVAL, DEFAULT_REFRESH_INTERVAL
        )

        # Generate unique_id from file path hash
        self._attr_unique_id = f"{DOMAIN}_{self._device_id}"

        # Device info for device registry integration
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._name,
            manufacturer="Local File",
            model="Static Image Camera",
            entry_type=DeviceEntryType.SERVICE,
        )

        self._attr_is_on = True
        self._attr_available = True

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image.

        This method is called by Home Assistant to get the current image.
        Uses async file reading to avoid blocking the event loop.
        """
        try:
            # Use aiofiles for async file reading
            async with aiofiles.open(self._file_path, "rb") as file:
                image_data = await file.read()

            # Update availability state
            self._attr_available = True

            return image_data

        except FileNotFoundError:
            self._attr_available = False
            return None
        except PermissionError:
            self._attr_available = False
            return None
        except Exception as err:
            self._attr_available = False
            return None

    async def async_update(self) -> None:
        """Update camera status.

        Called periodically by Home Assistant to check if the camera is available.
        """
        # Check if file exists and is readable
        if not os.path.exists(self._file_path):
            self._attr_available = False
            return

        if not os.path.isfile(self._file_path):
            self._attr_available = False
            return

        # Check if file is readable
        if not os.access(self._file_path, os.R_OK):
            self._attr_available = False
            return

        self._attr_available = True

    @property
    def name(self) -> str:
        """Return the name of the camera."""
        return self._name
