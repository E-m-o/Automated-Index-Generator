import rasterio
from rasterio.plot import show, show_hist
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg
from pycrs import parse
import glob
from lib.crawlers.csv_reader import csv_crawler


def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]


def clipper(request, indice_requested=None, show_flag=False, base_path=str):
    """
    Clips the raster image to the ROI and saves it.
    :param base_path: base path of the images
    :param show_flag: boolean flag to show the images clipped
    :param indice_requested:
    :param request: request number for the downloaded images
    :type request: str
    :rtype: None
    """
    print("=======================")
    print("Clipping indices to ROI")

    indice_list = ["ndmi", "ndvi", "savi", "msavi", "ndwi"]
    choice = []
    for idx, boolean in enumerate(indice_requested):
        if boolean == True:
            choice.append(idx)
    indices = [indice_list[i] for i in indice_requested]

    # indices = ["msavi"]
    for index in indices:
        fp = glob.glob(f"{base_path}.{request}/**/*{index}*",
                       recursive=True)

        # for f_name in fp:
        #     print(f_name)

        length_path_list = len(fp)
        print(f"length of list : {length_path_list}")
        out_tif = [None] * length_path_list

        for i in range(length_path_list):
            split_path = fp[i].split('/')
            out_tif[i] = '/'.join(
                split_path[:-1] + [f"{split_path[-2]}_clipped_{indices[0]}_{split_path[-1].split('_')[-1]}"])

        # for f_path in fp:
        #     print(f_path)

        # for out in out_tif:
        #     print(out)

        data = [None] * length_path_list
        geo = [None] * length_path_list
        coords = [None] * length_path_list
        out_img = [None] * length_path_list
        out_transform = [None] * length_path_list
        out_meta = [None] * length_path_list
        epsg_code = [None] * length_path_list

        for i, f_path in enumerate(fp):
            data[i] = rasterio.open(f_path)

        [minx, miny, maxx, maxy] = csv_crawler(clipper=True)
        print(minx, miny, maxx, maxy)

        bbox = box(minx, miny, maxx, maxy)

        for i in range(length_path_list):
            geo[i] = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(4326))
            # noinspection PyUnresolvedReferences
            geo[i] = geo[i].to_crs(crs=data[i].crs.data)

        for i in range(length_path_list):
            # noinspection PyTypeChecker
            coords[i] = getFeatures(geo[i])
            # print(coords[i])

        for i in range(length_path_list):
            # print(i)
            out_img[i], out_transform[i] = mask(data[i], shapes=coords[i], crop=True)

        for i in range(length_path_list):
            out_meta[i] = data[i].meta.copy()
            # print(out_meta[i])

        for i in range(length_path_list):
            # temp_dict = data[i].crs.data
            # print(temp_dict['init'])
            epsg_code[i] = int(data[i].crs.data['init'].split(':')[-1])
            # print(i, epsg_code[i])

        for i in range(length_path_list):
            out_meta[i].update({"driver": "GTiff",
                                "height": out_img[i].shape[1],
                                "width": out_img[i].shape[2],
                                "transform": out_transform[i],
                                "crs": parse.from_epsg_code(epsg_code[i]).to_proj4()})

        for i in range(length_path_list):
            with rasterio.open(out_tif[i], "w", **out_meta[i]) as destination:
                destination.write(out_img[i])

        if show_flag:
            for i in range(length_path_list):
                clipped = rasterio.open(out_tif[i])
                show(clipped, cmap="terrain")
            # print(clipped.shape)

    print("Indices clipped successfully!!!")
