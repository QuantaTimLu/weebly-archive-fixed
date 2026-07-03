import os
import re
from pathlib import Path

root_dir = Path(r'C:/Users/a8620/Downloads/Picture/weebly_archive_fixed')

# Regex to find the slideshow div and the following script block
# We look for the <div id="...-slideshow"> and the script that renders it.
slideshow_pattern = re.compile(
    r'<div id="(\d+)-slideshow">.*?</div>\s*<script type="text/javascript">.*?'
    r'wSlideshow\.render\(\{elementID:"\1",.*?images:\s*\[\s*\{\s*"url":"(.*?)"', 
    re.DOTALL
)

html_files = list(root_dir.glob('*.html'))
processed_count = 0
replacement_count = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    matches = list(slideshow_pattern.finditer(content))
    if not matches:
        continue
    
    processed_count += 1
    
    # Work backwards to maintain offsets
    for match in reversed(matches):
        div_id = match.group(1)
        img_url_raw = match.group(2)
        
        # Clean Weebly's escaped slashes \/ -> /
        img_url = img_url_raw.replace('\\/', '/')
        
        # Define the replacement: A simple img tag
        replacement = f'<div id="{div_id}-slideshow" style="text-align:center; margin: 10px 0;"><img src="assets/uploads/{img_url}" style="width:100%; max-width:800px; height:auto; border:1px solid #ddd; display:block; margin: 0 auto;"></div>'
        
        # Find where the script block ends
        start_idx = match.start()
        end_idx = content.find('</script>', match.end())
        if end_idx == -1:
            continue
        end_idx += len('</script>')
        
        content = content[:start_idx] + replacement + content[end_idx:]
        replacement_count += 1

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Processed {processed_count} files, replaced {replacement_count} slideshows.")
