"""Constants for Local File Camera integration."""

from homeassistant.components.camera import DOMAIN as CAMERA_DOMAIN
from homeassistant.const import CONF_NAME, CONF_FILE_PATH

DOMAIN = "local_file_camera"
CONF_REFRESH_INTERVAL = "refresh_interval"

DEFAULT_REFRESH_INTERVAL = 30  # seconds

# Valid image file extensions
VALID_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}

# Config entry data keys
CONF_DEVICE_ID = "device_id"
