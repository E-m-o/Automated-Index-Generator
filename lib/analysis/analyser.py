import numpy as np
from rasterio import open as r_open
from rasterio.plot import show
import os
import glob
import matplotlib.pyplot as plt


def analyser(path=None, requested_indices=[False, False, False, True, False]):
    """
    Performs time-series analysis on the images
    :param path: image directory path
    :param requested_indices: list of indices on which analysis is to be carried out
    :return: None
    """
    print("================")
    print("Analysing images")
    mosaic_paths = [os.path.join(path, "End_date/mosaics"), os.path.join(path, "Start_date/mosaics")]
    comparison_dict = {}
    indice_list = ["ndmi", "ndvi", "savi", "msavi", "ndwi"]
    choice = []
    for idx, boolean in enumerate(requested_indices):
        if boolean == True:
            choice.append(idx)
    indices = [indice_list[i] for i in requested_indices]

    # indices = ["msavi"]
    for index in indices:
        for mosaic_path in mosaic_paths:
            os.chdir(mosaic_path)
            # print(f"{mosaic_path} \t {index}")
            f_list = glob.glob(f"*_{index}.tiff")
            # print(f_list)

            if index not in comparison_dict.keys():
                comparison_dict[index] = []
                comparison_dict[index].append([os.path.join(os.getcwd(), f_list[0]), r_open(f_list[0])])
            else:
                comparison_dict[index].append([os.path.join(os.getcwd(), f_list[0]), r_open(f_list[0])])

    print(comparison_dict)

    try:
        print("creating analysis folder")
        os.chdir(os.path.join(path, 'analysis'))
    except FileNotFoundError:
        os.mkdir(os.path.join(path, 'analysis'))
        os.chdir(os.path.join(path, 'analysis'))

    os.chdir(os.path.join(path, "analysis"))
    for key, value in comparison_dict.items():
        print(f"Analysing {key} image")
        end = value[0]
        start = value[1]
        start_tiff = start[-1].read(1).astype("float64")
        end_tiff = end[-1].read(1).astype("float64")
        print(start_tiff.shape, end_tiff.shape, start_tiff.shape == end_tiff.shape)
        analysis = end_tiff - start_tiff
        max = analysis[0, 0]
        min = analysis[0, 0]
        for i in range(analysis.shape[0]):
            for j in range(analysis.shape[1]):
                if analysis[i, j] == np.nan:
                    print("nan")
                if analysis[i, j] > max:
                    max = analysis[i, j]
                if analysis[i, j] < min:
                    min = analysis[i, j]
                if analysis[i, j] == 0:
                    analysis[i, j] = 0
                elif analysis[i, j] < 0:
                    analysis[i, j] = -1
                    # less_than[i, j] = -1
                else:
                    analysis[i, j] = 1
                    # greater_than[i, j] = 1

        # for i in range(analysis.shape[0]):
        #     for j in range(analysis.shape[1]):
        #         analysis[i, j] = (analysis[i, j] - min)/(max - min)
        # max = analysis[0, 0]
        # min = analysis[0, 0]
        # for i in range(analysis.shape[0]):
        #     for j in range(analysis.shape[1]):
        #         if analysis[i, j] > max:
        #             max = analysis[i, j]
        #         if analysis[i, j] < min:
        #             min = analysis[i, j]

        print(max, min)
        figure_size = (20, 20)
        plt.figure(figsize=figure_size)
        plt.imshow(analysis)

        destination = r_open(f'./analysis_{key}.tiff', 'w', driver='GTiff',
                             width=start[-1].width, height=start[-1].height,
                             count=1,
                             crs=start[-1].crs,
                             transform=start[-1].transform,
                             dtype='float64')
        destination.write(analysis, 1)
        destination.close()
    print(os.getcwd())
    os.chdir(path)
    print(os.getcwd())
    print("Analysis successfully completed!!!")
    return

