from rasterio import open as r_open
from rasterio.plot import show
import os
import glob


def analyser(path=None):
    mosaic_paths = [os.path.join(path, "End_date/mosaics"), os.path.join(path, "Start_date/mosaics")]
    comparison_dict = {}
    indices = ["ndvi", "ndwi", "ndmi", "savi", "msavi"]
    for index in indices:
        for mosaic_path in mosaic_paths:
            os.chdir(mosaic_path)
            print(f"{mosaic_path} \t {index}")
            f_list = glob.glob(f"*_{index}.tiff")
            # print(f_list)
            if index not in comparison_dict.keys():
                comparison_dict[index] = []
                comparison_dict[index].append([os.path.join(os.getcwd(), f_list[0]), r_open(f_list[0])])
            else:
                comparison_dict[index].append([os.path.join(os.getcwd(), f_list[0]), r_open(f_list[0])])
    # print(comparison_dict)

    try:
        os.chdir(os.path.join(path, 'analysis'))
    except FileNotFoundError:
        os.mkdir(os.path.join(path, 'analysis'))
        os.chdir(os.path.join(path, 'analysis'))

    os.chdir(os.path.join(path, "analysis"))
    print("=================")
    print("Analysing indices")
    for key, value in comparison_dict.items():
        print(f"loop for key {key}")
        end = value[0]
        start = value[1]
        start_tiff = start[-1].read(1).astype("float64")
        end_tiff = end[-1].read(1).astype("float64")
        print(start_tiff.shape, end_tiff.shape, start_tiff.shape < end_tiff.shape)
        diff = [int, int]
        if start_tiff.shape > end_tiff.shape:
            f_name = ".".join(start[0].split('.')[:-1])
            print(f_name)
            with r_open(f"{f_name}_mod.tiff", 'w', driver='GTiff',
                        width=start[-1].width, height=start[-1].height,
                        count=1,
                        crs=start[-1].crs,
                        transform=start[-1].transform,
                        dtype='float64') as start_image:
                diff[0] = start_tiff.shape[0] - end_tiff.shape[0]
                diff[1] = start_tiff.shape[1] - end_tiff.shape[1]
                start_tiff = start_tiff[diff[0]:, diff[1]:]
                start_image.write(start_tiff, 1)
                print(start_tiff.shape, end_tiff.shape)
        elif start_tiff.shape > end_tiff.shape:
            f_name = ".".join(end[0].split('.')[:-1])
            print(f_name)
            with r_open(f"{f_name}_mod.tiff", 'w', driver='GTiff',
                        width=end[-1].width, height=end[-1].height,
                        count=1,
                        crs=end[-1].crs,
                        transform=end[-1].transform,
                        dtype='float64') as end_image:
                diff[0] = end_tiff.shape[0] - start_tiff.shape[0]
                diff[1] = end_tiff.shape[1] - start_tiff.shape[1]
                end_tiff = end_tiff[diff[0]:, diff[1]:]
                end_image.write(end_tiff, 1)
            print(start_tiff.shape, end_tiff.shape)
        # analysis = end_tiff - start_tiff
        # anlaysis_meta = start_tiff.meta.copy()
        # with r_open("analysis_{}.tiff".format(key), "w", **anlaysis_meta) as destination:
        #     destination.write(analysis)
    print(os.getcwd())
    os.chdir(path)
    print(os.getcwd())
    return


# analyser("/home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.3")
