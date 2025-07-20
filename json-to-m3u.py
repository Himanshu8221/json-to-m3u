import requests
import json

# 🔼 Add your URLs (can be .json, .php, etc.)
JSON_URLS = [
    "https://allinonereborn.fun/jstrweb2/index.php",
    "https://raw.githubusercontent.com/himanshu-temp/Z-playlist/refs/heads/main/Zee.m3u"
]

def fetch_channels(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Support nested data in case .php returns {"channels": [...]}
        if isinstance(data, dict) and "channels" in data:
            return data["channels"]
        elif isinstance(data, list):
            return data
        else:
            return []
    except Exception as e:
        print(f"❌ Failed to fetch or parse {url}: {e}")
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

        # Kodi props
        props = []
        if "user_agent" in channel:
            props.append(f'#KODIPROP:user-agent={channel["user_agent"]}')
        if "license_key" in channel:
            props.append(f'#KODIPROP:inputstream.adaptive.license_key={channel["license_key"]}')
        if "cookie" in channel:
            props.append(f'#KODIPROP:cookie={channel["cookie"]}')

        # EXTINF line
        extinf = f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" tvg-logo="{tvg_logo}" group-title="{group}", {name}'
        m3u_lines.extend(props + [extinf, url])
    
    return "\n".join(m3u_lines)

def main():
    all_channels = []
    for url in JSON_URLS:
        channels = fetch_channels(url)
        all_channels.extend(channels)

    m3u_output = convert_to_m3u(all_channels)
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)
    print(f"✅ M3U playlist saved as playlist.m3u with {len(all_channels)} channels")

if __name__ == "__main__":
    main()
