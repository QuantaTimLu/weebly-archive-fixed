import os
from pathlib import Path

root_dir = Path(r'C:/Users/a8620/Downloads/Picture/weebly_archive_fixed')
target_class = 'class="banner-wrap wsite-background"'
replacement = 'class="banner-wrap wsite-background" style="background-image: url(\'assets/images/713029954.jpg\'); background-size: cover; background-position: center;"'

html_files = list(root_dir.glob('*.html'))
count = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if target_class in content:
        new_content = content.replace(target_class, replacement)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Updated {count} files with inline background styles.")
