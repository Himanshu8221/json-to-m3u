import requests
import json
import time

# 🔼 List of source URLs (.php, .json, etc.)
JSON_URLS = [
    "https://allinonereborn.fun/jstrweb2/index.php",
    "https://raw.githubusercontent.com/Himanshu8221/m3u-to-json/refs/heads/main/playlist.json"
]

WAIT_BETWEEN_REQUESTS = 2  # Seconds

def fetch_channels(url):
    print(f"🌐 Fetching from: {url}")
    try:
        time.sleep(WAIT_BETWEEN_REQUESTS)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Handle different possible formats
        if isinstance(data, dict) and "channels" in data:
            return data["channels"]
        elif isinstance(data, list):
            return data
        else:
            print(f"⚠️ Unexpected format in {url}, skipping.")
            return []
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return []

def convert_to_m3u(channels):
    m3u_lines = ['#EXTM3U']
    for channel in channels:
        name = channel.get("display-name") or channel.get("name", "Unknown")
        url = channel.get("url")
        if not url:
            continue

        tvg_id = channel.get("tvg-id", "")
        tvg_name = channel.get("tvg-name", name)
        tvg_logo = channel.get("tvg-logo", "")
        group = channel.get("group-title", "Others")

        # Optional Kodi props
        props = []
        if "user_agent" in channel:
            props.append(f'#KODIPROP:user-agent={channel["user_agent"]}')
        if "license_key" in channel:
            props.append(f'#KODIPROP:inputstream.adaptive.license_key={channel["license_key"]}')
        if "cookie" in channel:
            props.append(f'#KODIPROP:cookie={channel["cookie"]}')

        extinf = f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" tvg-logo="{tvg_logo}" group-title="{group}", {name}'
        m3u_lines.extend(props + [extinf, url])
    
    return "\n".join(m3u_lines)

def main():
    all_channels = []
    for url in JSON_URLS:
        channels = fetch_channels(url)
        print(f"✅ Found {len(channels)} channels in {url}")
        all_channels.extend(channels)

    print(f"\n📦 Total combined channels: {len(all_channels)}")
    m3u_output = convert_to_m3u(all_channels)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)
    print("🎉 M3U file generated: playlist.m3u")

if __name__ == "__main__":
    main()
