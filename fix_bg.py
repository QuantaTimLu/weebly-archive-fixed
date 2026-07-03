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

# 1. Find all background images in HTML and CSS
bg_urls = set()
for file_path in root_dir.rglob('*'):
    if file_path.suffix in ['.html', '.css']:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                urls = re.findall(r'url\([\'"]?(.*?)[\'"]?\)', content)
                for url in urls:
                    if 'editmysite.com' in url or 'weebly.com' in url or '/uploads/' in url:
                        bg_urls.add(url)
        except:
            pass

print(f"Found {len(bg_urls)} background URLs.")

# 2. Download and localize them
for url in bg_urls:
    actual_url = url
    if url.startswith('//'):
        actual_url = 'https:' + url
    elif '/uploads/' in url and not url.startswith('http'):
        actual_url = base_url + url.lstrip('/')
    
    filename = url.split('/')[-1].split('?')[0]
    local_path = root_dir / 'assets' / 'images' / filename
    
    print(f"Downloading {actual_url} to {local_path}...")
    if download_image(actual_url, local_path):
        # 3. Update the files to use the local path
        for file_path in root_dir.rglob('*'):
            if file_path.suffix in ['.html', '.css']:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Simple relative path for the assets folder
                    # Since files are in root, assets/images/... works
                    new_content = content.replace(url, f"assets/images/{filename}")
                    
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except:
                    pass

print("Background images processed.")
