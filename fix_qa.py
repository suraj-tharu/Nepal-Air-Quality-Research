import glob
import re

fixes = {
    '01_no2_extraction.js': ("img.select('tropospheric_NO2_column_number_density_amf')", "img.select('qa_value')"),
    '02_so2_extraction.js': ("img.select('SO2_column_number_density_amf')", "img.select('qa_value')"),
    '03_co_extraction.js': ("img.select('H2O_column_number_density')", "img.select('qa_value')"),
    '04_o3_extraction.js': ("img.select('O3_effective_temperature')", "img.select('qa_value')"),
    '05_hcho_extraction.js': ("img.select('tropospheric_HCHO_column_number_density_amf')", "img.select('qa_value')"),
    '06_uvai_extraction.js': ("img.select('absorbing_aerosol_index')", "img.select('absorbing_aerosol_index')") # UVAI doesn't have qa_value, keep as is but no mask
}

for file, (old, new) in fixes.items():
    filepath = f"gee_scripts/{file}"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the bad selector
        content = content.replace(old, new)
        
        # If it's UVAI, remove the mask completely because any index > 0 is just positive UVAI
        if file == '06_uvai_extraction.js':
            content = content.replace("var mask = qa.gt(0);", "var mask = qa.gt(-100);")
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed QA band in {file}')
    except FileNotFoundError:
        print(f'{file} not found')
