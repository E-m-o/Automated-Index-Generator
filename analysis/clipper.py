import rasterio
from rasterio.plot import show, show_hist
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg
from pycrs import parse

from crawlers.csv_reader import csv_crawler

fp = "/home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.2/Start_date/mosaics/Start_date_mosaic_msavi.tiff"
out_tif = "/home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.2/Start_date/mosaics/start_clipped_msavi.tiff"

data = rasterio.open(fp)

show(data, cmap="terrain")

[minx, miny, maxx, maxy] = csv_crawler(test=True, clipper=True)
print(minx, miny, maxx, maxy)

bbox = box(minx, miny, maxx, maxy)

geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(4326))

geo = geo.to_crs(crs=data.crs.data)

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

coords = getFeatures(geo)

print(coords)

out_img, out_transform = mask(data, shapes=coords, crop=True)

out_meta = data.meta.copy()
print(out_meta)

epsg_code = int(data.crs.data['init'][5:])
print(epsg_code)

out_meta.update({"driver": "GTiff",
                 "height": out_img.shape[1],
                 "width": out_img.shape[2],
                 "transform": out_transform,
                 "crs": parse.from_epsg_code(epsg_code).to_proj4()})

with rasterio.open(out_tif, "w", **out_meta) as destination:
    destination.write(out_img)

clipped = rasterio.open(out_tif)
show(clipped, cmap="terrain")
