# 🎬 Universal JSON-to-M3U Converter

This tool converts a list of IPTV channels (in JSON format) into a proper `.m3u` playlist, supporting Widevine DRM, user-agent headers, referers, and tokenized URLs.

## ✅ Features

- 🔄 Converts multiple JSON sources (local files or remote `.json` / `.php` URLs).
- 📦 Supports complex formats including:
  - DASH `.mpd` stream links
  - Token-based URLs
  - Widevine DRM license details
  - Custom HTTP headers like Referer and User-Agent
- ⚠ Gracefully skips invalid URLs and non-conforming entries
- 💤 Includes wait time for websites that load slowly
- 🔐 Outputs fully Kodi- and VLC-compatible `.m3u` playlist with `#KODIPROP` and `#EXTVLCOPT`

---

## 📁 Input Format

Each channel object in your JSON file should follow a structure like:

```json
{
  "name": "Disney Channel",
  "logo": "https://example.com/logo.png",
  "category": "Entertainment",
  "mpd": "https://example.com/disney.mpd",
  "token": "your_token_here",
  "referer": "https://example.com/",
  "userAgent": "Custom-UA/1.0",
  "drm": {
    "key_id_here": "license_key_here"
  }
}
