import os
import glob

replacement = """var monthlyCollection = ee.ImageCollection.fromImages(monthlyComposites)
  .map(function(img) {
    return img.set('num_bands', img.bandNames().size());
  })
  .filter(ee.Filter.gt('num_bands', 0));"""

target = 'var monthlyCollection = ee.ImageCollection.fromImages(monthlyComposites);'

for file in glob.glob('gee_scripts/*.js'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    if target in content:
        content = content.replace(target, replacement)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {file}')
