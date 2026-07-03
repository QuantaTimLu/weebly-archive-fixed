import os
import re
import requests
from pathlib import Path

root_dir = Path(r'C:/Users/a8620/Downloads/Picture/weebly_archive_fixed')
base_url = "https://shinjrlu.weebly.com/uploads/"

def download_image(url, local_path):
    try:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

html_files = list(root_dir.glob('*.html'))
missing_images = set()

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        urls = re.findall(r'src="assets/uploads/(.*?)"', content)
        for url in urls:
            local_path = root_dir / 'assets' / 'uploads' / url
            if not local_path.exists():
                missing_images.add(url)

print(f"Found {len(missing_images)} missing images.")

success_count = 0
for img_url in missing_images:
    full_url = base_url + img_url
    local_path = root_dir / 'assets' / 'uploads' / img_url
    print(f"Downloading {full_url}...")
    if download_image(full_url, local_path):
        success_count += 1
    else:
        print(f"Failed to download {full_url}")

print(f"Successfully downloaded {success_count} out of {len(missing_images)} missing images.")
