import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os
import matplotlib.pyplot as plt


def mosaic_creator(base_path=None, test=False):

    print("================")
    print("Creating Mosaics")
    indices = ["ndvi", "ndwi", "ndmi", "savi", "msavi"]
    satellite = None
    # start_files = {}
    # end_files = {}
    files_dict = {}
    date_list = ["Start_date", "End_date"]

    for date in date_list:
        paths = glob.glob(os.path.join(base_path, "**/{}".format(date)), recursive=True)
        path = paths[0]
        print(path)
        index_dict = {index: [] for index in indices}
        for index in indices:
            print("Creating index {} for {}".format(index, " ".join(date.split('_'))))
            index_image = glob.glob("{}/**/*{}*".format(path, index), recursive=True)
            print(index_image)

            src_files_to_mosaic = []
            for file in index_image:
                src = rasterio.open(file)
                src_files_to_mosaic.append(src)
            print(src_files_to_mosaic)

            mosaic, out_trans = merge(src_files_to_mosaic)
            # show(mosaic, cmap="gray")
            # plt.waitforbuttonpress()
            #
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
    # print(len(image_dir_list))
    # for image_dir in image_dir_list:
    #     print(image_dir)

    # for date in date_list:
    #     for image_dir in image_dir_list:
    #         print(date, image_dir)
    #         if date in image_dir:
    #             files = glob.glob(os.path.join(image_dir, "/*.tiff"))
    #             files.sort()
    #             files_dict[image_dir] = files
    #
    # for key, value in files_dict.items():
    #     print(key, value)

    #     index_dict = {index: [] for index in indices}
    #     for index in indices:
    #         for key, value in files_dict.items():
    #             for val in value:
    #                 if "{}*.tiff".format(index) in val:
    #                     index_dict[index].append(val)
    #
    #         try:
    #             src_files_to_mosaic = []
    #             for file in index_dict[index]:
    #                 src = rasterio.open(file)
    #                 src_files_to_mosaic.append(src)
    #
    #             mosaic, out_trans = merge(src_files_to_mosaic)
    #             # show(mosaic, cmap="gray")
    #
    #             out_meta = src_files_to_mosaic[0].meta.copy()
    #             out_meta.update({"driver": "GTiff",
    #                              "height": mosaic.shape[1],
    #                              "width": mosaic.shape[2],
    #                              "transform": out_trans
    #                              }
    #                             )
    #
    #             # noinspection PyUnboundLocalVariable
    #             split = "/".join(key.split("/")[:-1])
    #             try:
    #                 os.chdir(os.path.join(split, 'mosaics'))
    #             except FileNotFoundError:
    #                 os.mkdir(os.path.join(split, 'mosaics'))
    #                 os.chdir(os.path.join(split, 'mosaics'))
    #             # print(os.getcwd())
    #
    #             pos = date.split('_')[0]
    #             with rasterio.open("{}_{}_mosaic{}.tiff".format(satellite, pos, index), "w",
    #                                **out_meta) as destination:
    #                 destination.write(mosaic)
    #             os.chdir(base)
    #         except IndexError:
    #             pass
    #     # print(index_dict)
    # print("Mosaics created")


# d = unzipper.decompress(sat_choice="2", path="/home/emo/Storage/Projects/Raster_Image_Calculator/Images")
