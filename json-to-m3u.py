import requests
import time
import json

# === INPUT SECTION (EDIT THESE) ===
JSON_URLS = [
    "https://allinonereborn.fun/jstrweb2/index.php",
    "https://raw.githubusercontent.com/himanshu-temp/Z-playlist/refs/heads/main/Zee.m3u"
]
output_file = "playlist.m3u"
request_timeout = 5  # seconds
delay_between_requests = 1  # seconds


# === MAIN CONVERSION FUNCTION ===
def convert_channel_to_m3u_entry(channel):
    name = channel.get("name", "Unknown")
    logo = channel.get("logo", "")
    group = channel.get("category", "Others")
    stream_url = channel.get("mpd") or channel.get("url") or channel.get("stream") or ""

    if not stream_url:
        return None  # skip if no playable URL

    token = channel.get("token", "")
    user_agent = channel.get("userAgent", "")
    referer = channel.get("referer", "")
    drm = channel.get("drm", {})

    # Construct stream with appended token if needed
    if token and token not in stream_url:
        stream_url += f"?{token}" if "?" not in stream_url else f"&{token}"

    # Start building M3U entry
    m3u = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}", {name}\n'

    # Add Kodi props
    if user_agent:
        m3u += f'#KODIPROP:user-agent={user_agent}\n'
    if referer:
        m3u += f'#KODIPROP:inputstream.adaptive.license_key={referer}\n'
    if drm:
        for key, value in drm.items():
            m3u += f'#KODIPROP:inputstream.adaptive.license_type=com.widevine.alpha\n'
            m3u += f'#KODIPROP:inputstream.adaptive.license_key=https://license-server.com/{key}|{value}|R\n'

    # Add the final stream URL
    m3u += stream_url + "\n"
    return m3u


# === URL FETCHER WITH MERGE ===
def fetch_all_channels(urls):
    merged_channels = []
    for url in urls:
        print(f"Fetching: {url}")
        try:
            resp = requests.get(url, timeout=request_timeout)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, dict):
                    channels = data.get("channels") or data.get("data") or []
                elif isinstance(data, list):
                    channels = data
                else:
                    print(f"⚠️ Skipped: Unknown structure at {url}")
                    continue
                if channels:
                    merged_channels.extend(channels)
                    print(f"✅ Fetched {len(channels)} channels from {url}")
                else:
                    print(f"⚠️ No channels found in {url}")
            else:
                print(f"❌ Failed to fetch {url} (Status {resp.status_code})")
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
        time.sleep(delay_between_requests)
    return merged_channels


# === M3U GENERATOR ===
def generate_m3u(channels, output_path):
    print(f"\nWriting to: {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for channel in channels:
            m3u_entry = convert_channel_to_m3u_entry(channel)
            if m3u_entry:
                f.write(m3u_entry)
    print("✅ M3U generation completed.")


# === RUN SCRIPT ===
if __name__ == "__main__":
    print("🔄 Starting JSON to M3U conversion...")
    all_channels = fetch_all_channels(input_urls)
    generate_m3u(all_channels, output_file)
