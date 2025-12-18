# Fix price field names in template
file_path = r'd:\fiverr\Tradeprint_eco\tradeprint_app\templates\frontend\product-full-width.html'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the field names
content = content.replace('tier.saver_price', 'tier.saver')
content = content.replace('tier.standard_price', 'tier.standard')
content = content.replace('tier.express_price', 'tier.express')

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed price field names!")
print("Changed:")
print("  tier.saver_price -> tier.saver")
print("  tier.standard_price -> tier.standard")
print("  tier.express_price -> tier.express")
