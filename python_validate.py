"""
Find which class create_grid_2x2 belongs to
"""

with open('lightweight_charts/abstract.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("="*70)
print("FINDING create_grid_2x2 LOCATION")
print("="*70)

# Find all class definitions
classes = []
for i, line in enumerate(lines):
    stripped = line.lstrip()
    if stripped.startswith('class '):
        class_name = stripped.split('(')[0].replace('class ', '').strip(':').strip()
        indent = len(line) - len(stripped)
        classes.append((i+1, class_name, indent))

print(f"\nFound {len(classes)} classes in file")
print(f"AbstractChart is at line 798")

# Find create_grid_2x2
print("\n" + "="*70)
for i, line in enumerate(lines):
    if 'def create_grid_2x2' in line:
        indent = len(line) - len(line.lstrip())
        print(f"❌ create_grid_2x2 found at line {i+1}, indent={indent}")
        
        # Find which class it belongs to
        belongs_to = None
        for class_line, class_name, class_indent in reversed(classes):
            if class_line < i+1:
                if indent == class_indent + 4:
                    belongs_to = class_name
                    print(f"   Currently in class: {class_name} (line {class_line})")
                    break
        
        if belongs_to != 'AbstractChart':
            print(f"\n❌ WRONG CLASS!")
            print(f"   It's in: {belongs_to}")
            print(f"   Should be in: AbstractChart (starting at line 798)")
        
        # Show context
        print(f"\nContext:")
        for j in range(max(0, i-3), min(len(lines), i+3)):
            marker = ">>> " if j == i else "    "
            print(f"{marker}{j+1:4d}: {lines[j].rstrip()[:70]}")
        break

print("\n" + "="*70)
print("SOLUTION:")
print("="*70)
print("You need to MOVE create_grid_2x2 method to inside AbstractChart class!")
print(f"Cut lines 129-231")
print(f"Paste them around line 798+ (inside AbstractChart class)")