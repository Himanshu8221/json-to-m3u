import requests
import time

# Configurable input URLs (add .json or .php URLs here)
JSON_URLS = [
    "https://allinonereborn.fun/jstrweb2/index.php",
    "https://raw.githubusercontent.com/himanshu-temp/Z-playlist/refs/heads/main/Zee.m3u"
]

OUTPUT_M3U = "merged_playlist.m3u"
TIMEOUT = 10  # seconds
RETRY_WAIT = 3  # wait between retries

def fetch_json(url):
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[❌] Error loading {url}: {e}")
        return []

def convert_channel_to_m3u(channel):
    name = channel.get("name") or channel.get("display-name", "Unknown")
    logo = channel.get("logo", "")
    group = channel.get("category") or channel.get("group-title", "Others")
    tvg_id = channel.get("tvg-id", "")
    tvg_name = channel.get("tvg-name", name)
    stream_url = channel.get("url") or channel.get("mpd")

    if not stream_url:
        return None  # skip empty URLs

    # Append token if available
    token = channel.get("token", "")
    if token and "?" not in stream_url:
        stream_url += "?" + token
    elif token:
        stream_url += "&" + token

    # DRM + headers
    license_key = ""
    drm = channel.get("drm", {})
    if isinstance(drm, dict) and drm:
        for key, value in drm.items():
            license_key = f"https://license-url.com/{key}|{value}|R{'\n'}"

    user_agent = channel.get("userAgent", "")
    referer = channel.get("referer", "")
    cookie = channel.get("cookie", "")

    extinf = f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" tvg-logo="{logo}" group-title="{group}",{name}'

    # KODIPROP block for DRM streams
    kodiprop = ""
    if license_key:
        kodiprop += f'#KODIPROP:inputstream.adaptive.license_type=com.widevine.alpha\n'
        kodiprop += f'#KODIPROP:inputstream.adaptive.license_key={license_key}\n'
    if user_agent:
        kodiprop += f'#KODIPROP:http-user-agent={user_agent}\n'
    if referer:
        kodiprop += f'#KODIPROP:referer={referer}\n'
    if cookie:
        kodiprop += f'#KODIPROP:cookie={cookie}\n'

    return f"{kodiprop}{extinf}\n{stream_url}"

def main():
    print("📥 Fetching channels from all sources...\n")
    all_channels = []

    for url in JSON_URLS:
        print(f"🔗 Loading: {url}")
        time.sleep(RETRY_WAIT)
        data = fetch_json(url)
        if isinstance(data, list):
            all_channels.extend(data)
        elif isinstance(data, dict) and "channels" in data:
            all_channels.extend(data["channels"])
        else:
            print(f"⚠️ Unexpected format in {url}")

    print(f"\n✅ Total channels fetched: {len(all_channels)}")

    lines = ["#EXTM3U"]
    for channel in all_channels:
        line = convert_channel_to_m3u(channel)
        if line:
            lines.append(line)

    with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n🎉 M3U playlist created: {OUTPUT_M3U}")

if __name__ == "__main__":
    main()
