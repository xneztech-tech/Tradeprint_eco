
import os

file_path = r"d:\fiverr\Tradeprint_eco\tradeprint_backend\templates\backend\order-list.html"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_next = False

for i in range(len(lines)):
    if skip_next:
        skip_next = False
        continue
        
    line = lines[i]
    # Check for the broken line 111
    if '{{ order.assigned_shop.shop_name' in line and '}}' not in line:
        # Check if next line has the closing braces
        if i + 1 < len(lines) and '}}</span>' in lines[i+1]:
            # Construct the fixed line
            # We preserve indentation from the first line
            fixed_line = line.rstrip() + ' }}\n' # Correction: wait, the next line has '}}</span>'
            # Actually, let's just hardcode the fix based on indentation
            # The line usually looks like: <space><span class...
            
            # Extract indentation
            indent = line[:line.find('<span')]
            
            # Verify checking
            # line: "                                            <span class="badge badge-secondary">{{ order.assigned_shop.shop_name\n"
            # next: "                                                }}</span>\n"
            
            # We want: "                                            <span class="badge badge-secondary">{{ order.assigned_shop.shop_name }}</span>\n"
            
            fixed_line = indent + '<span class="badge badge-secondary">{{ order.assigned_shop.shop_name }}</span>\n'
            new_lines.append(fixed_line)
            skip_next = True
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed broken template tag.")
