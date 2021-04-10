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
            f_list = glob.glob(f"*{index}.tiff")
            # print(f_list)
            if index not in comparison_dict.keys():
                comparison_dict[index] = []
                comparison_dict[index].append(r_open(f_list[0]))
            else:
                comparison_dict[index].append(r_open(f_list[0]))
    # print(comparison_dict)

    try:
        os.chdir(os.path.join(path, 'analysis'))
    except FileNotFoundError:
        os.mkdir(os.path.join(path, 'analysis'))
        os.chdir(os.path.join(path, 'analysis'))

    os.chdir(os.path.join(path, "analysis"))
    print("entering loop")
    for key, value in comparison_dict.items():
        print(f"loop for key {key}")
        end = value[0]
        start = value[1]
        start_tiff = start.read(1).astype("float64")
        end_tiff = end.read(1).astype("float64")
        print(start_tiff.shape, end_tiff.shape, start_tiff.shape < end_tiff.shape)
        # analysis = end_tiff - start_tiff
        # anlaysis_meta = start_tiff.meta.copy()
        # with r_open("analysis_{}.tiff".format(key), "w", **anlaysis_meta) as destination:
        #     destination.write(analysis)
    print(os.getcwd())
    os.chdir(path)
    print(os.getcwd())
    return


# analyser("/home/emo/Storage/Projects/Raster_Image_Calculator/Images/Request.2")
