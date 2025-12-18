# Add sides_printed and lamination options to product template

file_path = r'd:\fiverr\Tradeprint_eco\tradeprint_app\templates\frontend\product-full-width.html'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with "<!-- 3. Quantity Selection -->" and insert before it
insert_code = '''                        <!-- 2.5. Sides Printed -->
                        {% if product.sides_printed and product.sides_printed != 'both' %}
                        <div class="config-section">
                            <label class="config-label">Sides Printed</label>
                            <div class="option-buttons">
                                <button class="option-btn active" onclick="selectOption(this)">
                                    {{ product.get_sides_printed_display }}
                                </button>
                            </div>
                        </div>
                        {% elif product.sides_printed == 'both' %}
                        <div class="config-section">
                            <label class="config-label">Sides Printed</label>
                            <div class="option-buttons">
                                <button class="option-btn active" onclick="selectOption(this)" data-price="0">
                                    Single Sided
                                </button>
                                <button class="option-btn" onclick="selectOption(this)" data-price="{{ product.double_sided_price }}">
                                    Double Sided
                                </button>
                            </div>
                        </div>
                        {% endif %}

                        <!-- 2.6. Lamination -->
                        {% if product.lamination_options %}
                        <div class="config-section">
                            <label class="config-label">Lamination</label>
                            <div class="option-buttons">
                                {% for lamination in product.lamination_options %}
                                <button class="option-btn {% if forloop.first %}active{% endif %}"
                                    onclick="selectOption(this)" data-price="{{ lamination.price_modifier }}">
                                    {{ lamination.name }}
                                </button>
                                {% endfor %}
                            </div>
                        </div>
                        {% endif %}

'''

# Find the insertion point
for i, line in enumerate(lines):
    if '<!-- 3. Quantity Selection -->' in line:
        # Insert before this line
        lines.insert(i, insert_code)
        break

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Added sides_printed and lamination options!")
print("Inserted before '<!-- 3. Quantity Selection -->'")
