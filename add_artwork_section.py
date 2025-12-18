# Add Artwork section to product template

file_path = r'd:\fiverr\Tradeprint_eco\tradeprint_app\templates\frontend\product-full-width.html'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Artwork section HTML
artwork_section = '''
                        <!-- 2.7. Artwork Options -->
                        <div class="config-section">
                            <label class="config-label">How can we help you get your order designed, printed, and sent?</label>
                            <div class="artwork-options" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px;">
                                <div class="artwork-card active" onclick="selectArtwork(this)" style="padding: 20px; border: 2px solid #ddd; border-radius: 8px; text-align: center; cursor: pointer; transition: all 0.3s; background: white;">
                                    <div style="font-size: 32px; margin-bottom: 10px;">📤</div>
                                    <div style="font-weight: 600; margin-bottom: 5px;">Upload Artwork</div>
                                    <div style="font-size: 12px; color: #666;">I'll upload my own artwork</div>
                                </div>
                                <div class="artwork-card" onclick="selectArtwork(this)" style="padding: 20px; border: 2px solid #ddd; border-radius: 8px; text-align: center; cursor: pointer; transition: all 0.3s; background: white;">
                                    <div style="font-size: 32px; margin-bottom: 10px;">🎨</div>
                                    <div style="font-weight: 600; margin-bottom: 5px;">Online Designer</div>
                                    <div style="font-size: 12px; color: #666;">FREE - I'll design it myself</div>
                                </div>
                                <div class="artwork-card" onclick="selectArtwork(this)" style="padding: 20px; border: 2px solid #ddd; border-radius: 8px; text-align: center; cursor: pointer; transition: all 0.3s; background: white;">
                                    <div style="font-size: 32px; margin-bottom: 10px;">💼</div>
                                    <div style="font-weight: 600; margin-bottom: 5px;">Design Services</div>
                                    <div style="font-size: 12px; color: #666;">£46.00 - Professional design</div>
                                </div>
                            </div>
                        </div>
'''

# Find where to insert (before quantity selection)
insert_marker = '<!-- 3. Quantity Selection -->'
if insert_marker in content:
    # Check if artwork section already exists
    if 'Artwork Options' not in content:
        content = content.replace(insert_marker, artwork_section + '\n                        ' + insert_marker)
        print("✓ Added Artwork section")
    else:
        print("✓ Artwork section already exists")
else:
    print("✗ Could not find insertion point")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nCompleted! Added sections:")
print("  1. Sides Printed")
print("  2. Lamination")
print("  3. Artwork Options")
