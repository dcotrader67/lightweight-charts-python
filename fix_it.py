"""
Automatically fix the positioning conflict
"""

with open('lightweight_charts/abstract.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("="*70)
print("FIXING POSITIONING CONFLICT")
print("="*70)

changes = []

# Step 1: Add skip_positioning parameter to create_subchart
for i, line in enumerate(lines):
    if i > 970 and i < 990 and 'def create_subchart(' in line:
        # Find the closing paren of parameters
        for j in range(i, min(i+20, len(lines))):
            if 'toolbox: bool = False' in lines[j]:
                # Add skip_positioning parameter
                lines[j] = lines[j].rstrip() + ',\n'
                lines.insert(j+1, '        skip_positioning: bool = False\n')
                changes.append(f"Added skip_positioning parameter at line {j+1}")
                break
        break

# Step 2: Wrap positioning code in 'if not skip_positioning:'
for i, line in enumerate(lines):
    if i > 1020 and i < 1030 and 'first_subchart_from_root = ' in line:
        # Insert the if statement before the positioning block
        indent = '        '
        lines.insert(i+1, f'{indent}if not skip_positioning:\n')
        
        # Find the end of the positioning block (before 'if not sync_id:')
        for j in range(i+2, len(lines)):
            if 'if not sync_id:' in lines[j]:
                # Indent everything between
                for k in range(i+2, j):
                    if lines[k].strip():  # Don't indent empty lines more
                        lines[k] = '    ' + lines[k]
                changes.append(f"Wrapped positioning code (lines {i+1} to {j})")
                break
        break

# Step 3: Add skip_positioning=True to layout method calls
patterns_to_fix = [
    ('_layout_horizontal', 1395, 1405),
    ('_layout_vertical', 1426, 1436),
    ('_layout_main_right_stack', 1280, 1300),
    ('_layout_main_bottom_row', 1335, 1355)
]

for method_name, start, end in patterns_to_fix:
    for i in range(start, min(end, len(lines))):
        if 'self.create_subchart(' in lines[i]:
            # Find the closing paren
            for j in range(i, min(i+10, len(lines))):
                if 'sync_crosshairs_only=True' in lines[j]:
                    lines[j] = lines[j].replace(
                        'sync_crosshairs_only=True',
                        'sync_crosshairs_only=True,\n                skip_positioning=True'
                    )
                    changes.append(f"Added skip_positioning=True in {method_name}")
                    break
            break

if changes:
    # Write back
    with open('lightweight_charts/abstract.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("\n✅ SUCCESS! Applied fixes:")
    for change in changes:
        print(f"  - {change}")
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("1. Close ALL terminals")
    print("2. Open fresh terminal")
    print("3. pip uninstall -y lightweight-charts && pip install -e .")
    print("4. python test_layout_FIXED.py")
else:
    print("\n⚠️  Could not apply all fixes automatically")
    print("Please apply manually using POSITIONING_FIX.txt")