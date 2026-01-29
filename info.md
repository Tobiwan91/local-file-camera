# Development Notes

## Attribution

This integration was generated with [ha-integration@aurora-smart-home](https://github.com/tonylofgren/aurora-smart-home) v1.0.0.

## Purpose

The Local File Camera integration addresses a gap in Home Assistant's built-in `local_file` integration, which only creates a camera entity without a corresponding device. This limitation prevents proper integration with systems that rely on the device registry for camera detection and management.

By creating both a device and camera entity, this integration enables:
- Better device registry integration
- Compatibility with systems that scan for devices
- Improved organization and management
- Enhanced automation capabilities

## Architecture

### Device Registry Integration

The integration creates a virtual device with the following properties:
- **Identifiers**: `{("local_file_camera", device_id)}`
- **Manufacturer**: "Local File"
- **Model**: "Static Image Camera"
- **Entry Type**: `DeviceEntryType.SERVICE`

Each camera entity is linked to this device via the `device_info` property.

### Unique ID Generation

Device IDs are generated using MD5 hash of the file path:
```python
device_id = hashlib.md5(file_path.encode()).hexdigest()[:16]
```

This ensures stable, unique identifiers for each file path.

### Async File I/O

All file operations use `aiofiles` for non-blocking I/O:
```python
async with aiofiles.open(file_path, "rb") as file:
    image_data = await file.read()
```

This prevents blocking the Home Assistant event loop.

### Security Measures

- Directory traversal prevention (checks for ".." in paths)
- Absolute path requirement
- File existence and readability validation
- Image format validation (extension + header check)
- No credential logging

## Implementation Notes

### Iron Law Compliance

This integration follows the Home Assistant "Iron Law" requirements:

1. **Timestamps**: Uses `dt_util.now()` / `dt_util.utcnow()` only
2. **Attributes**: JSON-serializable only (no dataclasses, no datetime objects)
3. **Async**: Uses `aiofiles` for all file I/O

### Config Flow

The config flow provides:
- Real-time file validation
- Clear error messages
- Unique ID generation
- Duplicate detection (via `async_set_unique_id`)
- Options flow for updating refresh interval

### Error Handling

The integration gracefully handles:
- `FileNotFoundError` → Camera unavailable
- `PermissionError` → Camera unavailable
- Invalid image data → Camera unavailable
- Invalid paths → Clear error messages

## Testing

### Manual Testing Checklist

- [ ] Integration appears in Settings → Integrations
- [ ] Config flow validates all inputs correctly
- [ ] Camera entity created with correct `unique_id`
- [ ] Device created with correct identifiers
- [ ] Camera entity belongs to device
- [ ] Image displays in dashboard
- [ ] Auto-refresh works (replace file, wait, check update)
- [ ] File errors handled gracefully (unavailable state)
- [ ] No blocking I/O operations
- [ ] Integration can be unloaded cleanly

### Validation

The integration includes automated validation via GitHub Actions:
- HACS validation
- Hassfest validation
- Runs on push, pull request, and daily schedule

## Future Enhancements

Potential features for future versions:
- Support for image URLs (HTTP/HTTPS)
- Image transformation (resize, crop)
- Multiple images per camera (slideshow)
- Image overlay (timestamp, text)
- Motion detection (via image comparison)

## License

MIT License - Free to use and modify

## Support

For issues or questions:
1. Check the main README.md
2. Review Home Assistant logs
3. Submit an issue on GitHub

---

*Generated with [ha-integration@aurora-smart-home](https://github.com/tonylofgren/aurora-smart-home)*
