import os
import re

directory = 'content/post'

bad_files = []

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parts = content.split('---', 2)
            if len(parts) >= 3:
                body = parts[2]
            else:
                body = content
                
            # Find all headings
            headings = re.findall(r'^#{1,6}\s+.*', body, re.MULTILINE)
            if headings:
                # If the first heading is level 3 or more, it's bad
                first_heading = headings[0]
                if first_heading.startswith('###'):
                    bad_files.append((filepath, first_heading))

for b, h in bad_files:
    print(f"{b}: {h}")

