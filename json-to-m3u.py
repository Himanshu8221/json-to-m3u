import requests

# 🔗 Add your JSON playlist URLs here
JSON_URLS = [
    "https://allinonereborn.fun/jstrweb2/index.php",
    "https://raw.githubusercontent.com/Himanshu8221/m3u-to-json/refs/heads/main/playlist.json"
]

# 📁 Output M3U filename
OUTPUT_FILE = "playlist.m3u"


def fetch_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Failed to fetch or parse JSON from {url}: {e}")
        return []


def convert_json_list_to_m3u(json_list, output_file="playlist.m3u"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")

        for ch in json_list:
            url = ch.get("url")
            if not url:
                continue

            name = ch.get("display-name") or ch.get("name") or "Untitled"
            tvg_id = ch.get("tvg-id", "")
            tvg_name = ch.get("tvg-name", "")
            tvg_logo = ch.get("tvg-logo", "")
            group = ch.get("group-title", "")
            user_agent = ch.get("user_agent")
            license_key = ch.get("license_key")
            cookie = ch.get("cookie")

            # Write KODIPROP metadata
            if user_agent:
                f.write(f"#KODIPROP:inputstream.adaptive.user_agent={user_agent}\n")
            if license_key:
                f.write(f"#KODIPROP:inputstream.adaptive.license_key={license_key}\n")
            if cookie:
                f.write(f"#KODIPROP:http-cookie={cookie}\n")

            # Write EXTINF
            f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" tvg-logo="{tvg_logo}" group-title="{group}",{name}\n')
            f.write(url + "\n")

    print(f"✅ Final merged M3U saved as: {output_file}")


def main():
    all_channels = []

    for url in JSON_URLS:
        print(f"📥 Fetching: {url}")
        channels = fetch_json_from_url(url)
        all_channels.extend(channels)

    convert_json_list_to_m3u(all_channels, OUTPUT_FILE)


if __name__ == "__main__":
    main()
