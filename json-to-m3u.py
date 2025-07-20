import requests
import json
import time

# ✅ Input URLs at the top
input_urls = [
    "https://allinonereborn.fun/jstrweb2/index.php",
    "https://raw.githubusercontent.com/himanshu-temp/Z-playlist/refs/heads/main/Zee.m3u"
]

# ✅ Output M3U file
output_file = "playlist.m3u"

# ✅ Wait time for URLs to respond (in seconds)
REQUEST_TIMEOUT = 10
WAIT_BETWEEN_REQUESTS = 1

# ✅ Logger
def log(msg):
    print(f"[INFO] {msg}")

# ✅ Fetch JSON from a given URL, handle PHP and JSON endpoints
def fetch_json(url):
    try:
        time.sleep(WAIT_BETWEEN_REQUESTS)
        res = requests.get(url, timeout=REQUEST_TIMEOUT)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        log(f"❌ Failed to fetch {url}: {e}")
        return []

# ✅ Combine and normalize all channels
def get_all_channels(urls):
    channels = []
    for url in urls:
        data = fetch_json(url)
        if isinstance(data, dict):  # in case JSON is in {"channels": [...]}
            data = data.get("channels", [])
        if isinstance(data, list):
            channels.extend(data)
    return channels

# ✅ Build stream URL
def build_stream_url(channel):
    url = channel.get("mpd", "")
    token = channel.get("token", "")
    if token and "?" not in url:
        url += "?" + token
    return url

# ✅ Build KODIPROP tag if needed
def build_kodiprop(channel):
    props = []
    if channel.get("referer"):
        props.append(f"#KODIPROP:inputstream.adaptive.license_key=https://license-url|Referer={channel['referer']}|")
    if channel.get("userAgent"):
        props.append(f"#KODIPROP:User-Agent={channel['userAgent']}")
    if "drm" in channel:
        for keyid, key in channel["drm"].items():
            props.append(f"#KODIPROP:inputstream.adaptive.license_type=com.widevine.alpha")
            props.append(f"#KODIPROP:inputstream.adaptive.license_key=https://license-url/{keyid}|{key}|")
    return "\n".join(props)

# ✅ Convert to M3U
def convert_to_m3u(channels):
    m3u = "#EXTM3U\n"
    for ch in channels:
        name = ch.get("name", "Unknown")
        logo = ch.get("logo", "")
        group = ch.get("category", "Others")
        stream_url = build_stream_url(ch)
        kodiprop = build_kodiprop(ch)

        m3u += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}", {name}\n'
        if kodiprop:
            m3u += f"{kodiprop}\n"
        m3u += f"{stream_url}\n"
    return m3u

# ✅ Main execution
if __name__ == "__main__":
    print("🔄 Starting JSON to M3U conversion...")
    all_channels = get_all_channels(input_urls)
    final_m3u = convert_to_m3u(all_channels)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_m3u)

    print(f"✅ M3U Playlist created successfully with {len(all_channels)} channels: {output_file}")
