# Local File Camera

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![GitHub Release](https://img.shields.io/github/release/Tobiwan91/local-file-camera.svg)

A Home Assistant integration that displays static images from local files with proper device registry integration.

## Why This Integration?

The built-in `local_file` integration only creates a camera entity without a device. This integration creates **both a device and camera entity**, enabling better integration with Home Assistant's device registry.

This is particularly useful for:
- Systems that scan the device registry for cameras
- Custom dashboards that organize cameras by device
- Automations that trigger on device events
- Better organization and management of camera entities

## Features

- ✅ **Device Registry Integration** - Creates both device AND camera entity
- ✅ **Config Flow UI** - User-friendly setup through Settings → Integrations
- ✅ **File Validation** - Validates file exists, is readable, and is a valid image
- ✅ **Auto-Refresh** - Configurable update interval (default: 30 seconds)
- ✅ **Error Handling** - Graceful degradation with clear error messages
- ✅ **Security** - Validates paths to prevent directory traversal attacks

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)

## Use Cases

- **Security Cameras** - Display snapshots from IP cameras saved to local storage
- **Webcams** - Show periodic captures from USB cameras
- **Monitoring Systems** - Display still images from surveillance systems
- **Screenshots** - Show periodic screenshots from any system
- **Garden Cameras** - Display wildlife or garden monitoring images
- **Doorbell Cameras** - Show snapshots from doorbell systems

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations → Custom repositories**
3. Click **+ Add Repository**
4. Enter URL: `https://github.com/Tobiwan91/local-file-camera`
5. Select category: **Integration**
6. Click **Add**
7. Search for "Local File Camera" in HACS
8. Click **Download** and restart Home Assistant

### Manual

1. Download the latest release from [GitHub Releases](https://github.com/Tobiwan91/local-file-camera/releases)
2. Extract the archive
3. Copy the `local_file_camera` folder to `/config/custom_components/`
4. Restart Home Assistant

## Configuration

### Via UI

1. Go to **Settings → Devices & Services**
2. Click **+ Add Integration**
3. Search for "Local File Camera"
4. Fill in the configuration form:
   - **File Path**: Absolute path to the image file (e.g., `/config/images/camera.jpg`)
   - **Camera Name**: Name for this camera (e.g., "Front Door Camera")
   - **Refresh Interval**: How often to check for file changes in seconds (5-3600, default: 30)
5. Click **Submit**

### Update Refresh Interval

After setup, you can change the refresh interval:

1. Go to **Settings → Devices & Services**
2. Find your Local File Camera
3. Click **Configure** (gear icon)
4. Adjust the **Refresh Interval**
5. Click **Submit**

## Usage

### Add to Dashboard

1. Edit your Lovelace dashboard
2. Add a new card
3. Select **Camera** card type
4. Choose your Local File Camera entity
5. Save the card

### Update Camera Image

The camera will automatically refresh when you replace the image file:

```bash
# Replace the image with a new one
cp /path/to/new/image.jpg /config/images/camera.jpg

# Wait up to 30 seconds (or your refresh interval)
# The camera will update automatically
```

## File Location Examples

### Home Assistant Supervised (Docker)
```bash
/config/www/images/front_door.jpg
/config/images/garden_camera.jpg
/share/camera/backyard.jpg
```

### Home Assistant Container
```bash
/home/homeassistant/images/camera.jpg
/var/lib/homeassistant/images/camera.jpg
```

### VM or Direct Install
```bash
/var/lib/homeassistant/images/camera.jpg
/home/homeassistant/.homeassistant/images/camera.jpg
```

## Troubleshooting

### Camera Shows "Unavailable"

**Possible causes:**
- File path is incorrect
- File doesn't exist
- File permissions prevent reading
- File is not a valid image

**Solutions:**
1. Verify file path is correct
2. Check file exists: `ls -l /path/to/your/image.jpg`
3. Check file permissions: `chmod 644 /path/to/your/image.jpg`
4. Ensure file is a valid image format

### Camera Not Updating After File Change

**Possible causes:**
- Refresh interval not reached
- File not actually updated

**Solutions:**
1. Wait for the refresh interval (default: 30 seconds)
2. Reduce refresh interval in camera options (minimum: 5 seconds)
3. Restart Home Assistant

### "File Not Found" Error During Setup

**Possible causes:**
- Path doesn't exist
- Using relative path instead of absolute

**Solutions:**
1. Use absolute path (starting with `/`)
2. Verify file exists on the HA filesystem
3. Check file is readable by HA user

### Integration Not Appearing

**Possible causes:**
- Files not in correct location
- Home Assistant not restarted
- Invalid manifest.json

**Solutions:**
1. Verify files are in `/config/custom_components/local_file_camera/`
2. Restart Home Assistant
3. Check logs: **Settings → System → Logs**


**Use this integration when:** You need to display static images from local files with proper device registry integration.

**Use the generic camera integration when:** You need RTSP streaming or network camera support.

## Development

### Project Structure

```
custom_components/local_file_camera/
├── __init__.py              # Setup entry point
├── manifest.json            # Integration metadata
├── const.py                 # Constants
├── config_flow.py           # UI configuration
├── camera.py                # Camera entity
├── strings.json             # UI strings
└── translations/
    └── en.json              # English translations
```

### Technical Details

- **Domain**: `local_file_camera`
- **Platform**: `camera`
- **IoT Class**: `local_polling`
- **Unique ID**: MD5 hash of file path
- **Device Type**: `SERVICE` (virtual device)

## Requirements

- Home Assistant 2024.1.0 or newer
- No external dependencies

## Limitations

By design:
- Static images only (no video streaming)
- Must use local files (no HTTP/HTTPS URLs)
- No motion detection or recording
- Refresh interval minimum: 5 seconds

These limitations are acceptable for the intended use case of displaying static images from local files.

## Security

- ✅ Validates file paths to prevent directory traversal
- ✅ Checks file existence and readability before access
- ✅ Validates image format via extension and header check
- ✅ No credentials or sensitive data logged
- ✅ Input validation with voluptuous schemas

## License

MIT License - see [LICENSE](LICENSE) file

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Generated With

This integration was generated with [ha-integration@aurora-smart-home](https://github.com/tonylofgren/aurora-smart-home)
