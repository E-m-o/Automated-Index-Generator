import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os
import matplotlib.pyplot as plt


def mosaic_creator(base_path=None, show_flag=False, requested_indices=None):
    """
    Creates a mosaic of all the images for the current request
    :param base_path: path of current request
    :param show_flag: flag to show mosaics
    :param requested_indices: list of requested indices
    """
    print("================")
    print("Creating Mosaics")
    index_list = ["ndmi", "ndvi", "savi", "msavi", "ndwi"]
    choice = []
    for idx, boolean in enumerate(requested_indices):
        if boolean:
            choice.append(idx)
    indices = [index_list[i] for i in requested_indices]
    date_list = ["Start_date", "End_date"]

    for date in date_list:
        paths = glob.glob(os.path.join(base_path, "**/{}".format(date)), recursive=True)
        path = paths[0]
        print(path)
        # index_dict = {index: [] for index in indices}
        for index in indices:
            print("Creating index {} for {}".format(index, " ".join(date.split('_'))))
            index_image = glob.glob("{}/**/*clipped_{}*".format(path, index), recursive=True)
            # print(index_image)

            src_files_to_mosaic = []
            for file in index_image:
                src = rasterio.open(file)
                src_files_to_mosaic.append(src)
            # print(src_files_to_mosaic)

            mosaic, out_trans = merge(src_files_to_mosaic)
            if show_flag:
                show(mosaic, cmap="terrain")
                plt.waitforbuttonpress()

            out_meta = src_files_to_mosaic[0].meta.copy()
            out_meta.update({"driver": "GTiff",
                             "height": mosaic.shape[1],
                             "width": mosaic.shape[2],
                             "transform": out_trans
                             }
                            )
            try:
                try:
                    os.chdir(os.path.join(path, 'mosaics'))
                except FileNotFoundError:
                    os.mkdir(os.path.join(path, 'mosaics'))
                    os.chdir(os.path.join(path, 'mosaics'))

                with rasterio.open("{}_mosaic_{}.tiff".format(date, index), "w",
                                   **out_meta) as destination:
                    destination.write(mosaic)
                os.chdir(base_path)
            except IndexError:
                pass
    print("Mosaics created successfully!!!")

