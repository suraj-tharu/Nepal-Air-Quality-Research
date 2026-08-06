"""
Update all GEE scripts and config to use 2019-2026 time period.
"""
import glob

files = glob.glob('gee_scripts/*.js')

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Update END_DATE
    content = content.replace("var END_DATE = '2024-12-31';", "var END_DATE = '2026-12-31';")
    content = content.replace("var END_DATE = '2025-12-31';", "var END_DATE = '2026-12-31';")
    
    # Update year sequence
    content = content.replace("ee.List.sequence(2019, 2024)", "ee.List.sequence(2019, 2026)")
    content = content.replace("ee.List.sequence(2019, 2025)", "ee.List.sequence(2019, 2026)")
    
    # Update export for loops
    content = content.replace("yr <= 2024", "yr <= 2026")
    content = content.replace("yr <= 2025", "yr <= 2026")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated: {filepath}')
    else:
        print(f'No changes: {filepath}')

# Update Python config
config_path = 'analysis/config.py'
with open(config_path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("END_YEAR = 2024", "END_YEAR = 2026")
content = content.replace("END_YEAR = 2025", "END_YEAR = 2026")
with open(config_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'Updated: {config_path}')
