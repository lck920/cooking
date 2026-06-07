import os
import re

directory = r'content\post\drinks'

for root, dirs, files in os.walk(directory):
    for file in files:
        if not file.endswith('.md'):
            continue
        filepath = os.path.join(root, file)
        
        # skip drink-base-mixtures
        if 'drink-base-mixtures' in filepath:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = content.split('---', 2)
        if len(parts) < 3:
            continue
            
        front_matter = parts[1]
        body = parts[2]
        
        # If body already has **Hot Version**, skip
        if '**Hot Version**' in body:
            continue
            
        # We need to transform:
        # ## Ingredients
        # ...
        # ## Steps
        # ...
        # ### Cold Version
        # ...
        # ## Steps
        #
        # Into:
        # **Hot Version**
        # ## Ingredients
        # ...
        # **Cold Version**
        # ## Ingredients
        # ...
        
        # If it has ### Cold Version
        if '### Cold Version' in body or 'Cold Version:' in body:
            # 1. Add **Hot Version** before the first ## Ingredients
            new_body = re.sub(r'^\s*## Ingredients', r'**Hot Version**\n## Ingredients', body, count=1, flags=re.MULTILINE)
            
            # 2. Replace ### Cold Version or Cold Version: with **Cold Version** \n ## Ingredients
            new_body = re.sub(r'^\s*###\s*Cold Version\s*$', r'**Cold Version**\n## Ingredients', new_body, flags=re.MULTILINE)
            new_body = re.sub(r'^\s*Cold Version:\s*$', r'**Cold Version**\n## Ingredients', new_body, flags=re.MULTILINE)
            
            new_content = parts[0] + '---' + front_matter + '---' + new_body
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file}")
