import requests
import time
import json

# === ✅ INPUT: Channel JSON/PHP URLs ===
input_urls = [
    "https://allinonereborn.fun/jstrweb2/index.php",
    "https://raw.githubusercontent.com/himanshu-temp/Z-playlist/refs/heads/main/Zee.m3u"
]

output_file = "playlist.m3u"
request_timeout = 5
delay_between_requests = 1  # seconds between URLs


# === 🔁 Convert each channel entry ===
def convert_channel_to_m3u_entry(channel):
    name = channel.get("name", "Unknown")
    logo = channel.get("logo", "")
    group = channel.get("category", "Others")
    stream_url = channel.get("mpd") or channel.get("url") or channel.get("stream") or ""

    if not stream_url:
        return None  # Skip invalid entries

    # Append token if needed
    token = channel.get("token", "")
    if token and token not in stream_url:
        stream_url += f"?{token}" if "?" not in stream_url else f"&{token}"

    user_agent = channel.get("userAgent", "")
    referer = channel.get("referer", "")
    drm = channel.get("drm", {})

    m3u = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}", {name}\n'

    if user_agent:
        m3u += f'#KODIPROP:user-agent={user_agent}\n'
    if referer:
        m3u += f'#KODIPROP:inputstream.adaptive.license_key={referer}\n'
    if isinstance(drm, dict):
        for key, value in drm.items():
            m3u += '#KODIPROP:inputstream.adaptive.license_type=com.widevine.alpha\n'
            m3u += f'#KODIPROP:inputstream.adaptive.license_key=https://license-server.com/{key}|{value}|R\n'

    m3u += stream_url + "\n"
    return m3u


# === 🌐 Fetch and parse all URLs ===
def fetch_all_channels(urls):
    all_channels = []
    for url in urls:
        print(f"🔗 Fetching: {url}")
        try:
            response = requests.get(url, timeout=request_timeout)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                all_channels.extend(data)
            elif isinstance(data, dict):
                channels = data.get("channels") or data.get("data") or []
                if isinstance(channels, list):
                    all_channels.extend(channels)
            else:
                print(f"⚠️ Unexpected format at {url}")

        except Exception as e:
            print(f"❌ Error loading {url}: {e}")
        time.sleep(delay_between_requests)
    return all_channels


# === 🧾 Write to .m3u file ===
def generate_m3u(channels, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            entry = convert_channel_to_m3u_entry(ch)
            if entry:
                f.write(entry)
    print(f"✅ Saved: {output_path}")


# === 🚀 Main Execution ===
if __name__ == "__main__":
    print("🔄 Starting JSON to M3U conversion...\n")
    all_channels = fetch_all_channels(input_urls)
    print(f"📦 Total channels collected: {len(all_channels)}")
    generate_m3u(all_channels, output_file)
