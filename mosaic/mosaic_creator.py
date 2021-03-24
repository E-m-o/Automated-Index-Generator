import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os

paths = [
    '/home/emo/Storage/Projects/Raster_Image_Calculator/Test_files/Temp/Start_date/LC08_L1TP_143044_20210122_20210307_01_T1',
    '/home/emo/Storage/Projects/Raster_Image_Calculator/Test_files/Temp/Start_date/LC08_L1TP_143045_20210122_20210307_01_T1']

files = {}
for path in paths:
    file = glob.glob(os.path.join(path, '*.TIF'))
    file.sort()
    files[path] = file

b4 = []
for key, value in files.items():
    for val in value:
        if 'B4.TIF' in val:
            b4.append(val)

src_files_to_mosaic = []
for file in b4:
    src = rasterio.open(file)
    src_files_to_mosaic.append(src)

mosaic, out_trans = merge(src_files_to_mosaic)
show(mosaic, cmap='terrain')

out_meta = src_files_to_mosaic[0].meta.copy()
out_meta.update({"driver": "GTiff",
                 "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": out_trans
                 }
                )

with rasterio.open('mosaic.tiff', "w", **out_meta) as destination:
    destination.write(mosaic)
# print(b4)
