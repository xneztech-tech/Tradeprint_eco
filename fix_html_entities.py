# Quick fix script to replace HTML entities in JavaScript
import re

file_path = r'd:\fiverr\Tradeprint_eco\tradeprint_app\templates\frontend\product-full-width.html'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace HTML entities in JavaScript
content = content.replace('&amp;&amp;', '&&')
content = content.replace('&lt;', '<')
content = content.replace('&gt;', '>')

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed HTML entities in JavaScript!")
print("Refresh the page to see the changes.")
