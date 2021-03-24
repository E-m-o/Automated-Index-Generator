from rasterio import open
from rasterio.plot import show
import numpy as np
import glob

np.seterr(divide='ignore', invalid='ignore')


def band_returner_landsat(show_list=False):
    """
    Returns the list of relevant bands as per the truth value of input parameters

    :param show_list: flag
    :type show_list: bool
    """
    _list = []
    _list = glob.glob('*')
    _list.sort()
    ret_dict = {}

    for band in _list:
        if '6.TIF' in band[-7:]:
            ret_dict['6'] = band  # swir
        if '5.TIF' in band[-7:]:
            ret_dict['5'] = band  # nir
        if '4.TIF' in band[-7:]:
            ret_dict['4'] = band  # red

    for band in _list:
        if '6.tif' in band[-7:]:
            ret_dict['6'] = band  # swir
        if '5.tif' in band[-7:]:
            ret_dict['5'] = band  # nir
        if '4.tif' in band[-7:]:
            ret_dict['4'] = band  # red

    if show_list:
        # print(_list)
        print(ret_dict)
    if len(ret_dict) >= 3:
        return ret_dict
    else:
        return False


def ndmi_calc_landsat(show_flag=False):
    """
    Calculates and saves the Normalised Difference Moisture Index (NDMI) raster image

    :param show_flag: flag
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_landsat()

    if band_dict:
        # read bands
        band5 = open(band_dict['5'])  # nir
        band6 = open(band_dict['6'])  # swir
        nir = band5.read(1).astype('float64')
        swir = band6.read(1).astype('float64')

        # calculate ndmi raster image
        ndmi = np.where(
            (swir + nir) == 0.,
            0,
            (nir - swir) / (nir + swir)
        )

        # save ndmi raster image
        ndmi_image = open('./ndmi_landsat.tiff', 'w', driver='GTiff',
                          width=band5.width, height=band5.height,
                          count=1,
                          crs=band5.crs,
                          transform=band5.transform,
                          dtype='float64')
        ndmi_image.write(ndmi, 1)
        ndmi_image.close()

        if show_flag:
            ndmi = open('ndmi_landsat.tiff')
            show(ndmi, cmap='Blues')


def ndvi_calc_landsat(show_flag=False):
    """
    Calculates and saves the Normalised Difference Vegetation Index (NDVI) raster image

    :param show_flag: flag
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_landsat()

    if band_dict:
        # read bands
        band4 = open(band_dict['4'])  # red
        band5 = open(band_dict['5'])  # nir
        red = band4.read(1).astype('float64')
        nir = band5.read(1).astype('float64')

        # calculate ndvi raster image
        ndvi = np.where(
            (nir + red) == 0.,
            0,
            (nir - red) / (nir + red)
        )

        # save ndvi raster image
        ndvi_image = open('./ndvi_landsat.tiff', 'w', driver='GTiff',
                          width=band5.width, height=band5.height,
                          count=1,
                          crs=band5.crs,
                          transform=band5.transform,
                          dtype='float64')
        ndvi_image.write(ndvi, 1)
        ndvi_image.close()

        if show_flag:
            ndvi = open('ndvi_landsat.tiff')
            show(ndvi, cmap='Greens')


def savi_calc_landsat(show_flag=False):
    """
    Calculates and saves the Soil Adjusted Vegetation Index (SAVI) raster image

    :param show_flag: flag
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_landsat()

    if band_dict:
        # read bands
        band4 = open(band_dict['4'])  # red
        band5 = open(band_dict['5'])  # nir
        red = band4.read(1).astype('float64')
        nir = band5.read(1).astype('float64')

        # calculate savi raster image
        savi = np.where(
            (nir + red) == 0.,
            0,
            ((nir - red) / (nir + red + 0.5)) * 1.5
        )

        # INSERT CHECKING CONDITION
        savi[savi > 1] = 1
        savi[savi < -1] = -1

        # save savi raster image
        savi_image = open('./savi_landsat.tiff', 'w', driver='GTiff',
                          width=band5.width, height=band5.height,
                          count=1,
                          crs=band5.crs,
                          transform=band5.transform,
                          dtype='float64')
        savi_image.write(savi, 1)
        savi_image.close()

        if show_flag:
            savi = open('savi_landsat.tiff')
            show(savi, cmap='Greens')


def msavi_calc_landsat(show_flag=False):
    """
    Calculates and saves the Modified Soil Adjusted Vegetation Index (MSAVI) raster image

    :param show_flag: flag
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_landsat()

    if band_dict:
        # read bands
        band4 = open(band_dict['4'])  # red
        band5 = open(band_dict['5'])  # nir
        red = band4.read(1).astype('float64')
        nir = band5.read(1).astype('float64')

        # calculate msavi raster image
        msavi = np.where(
            (nir + red) == 0.,
            0,
            (2 * nir + 1 - np.sqrt((2 * nir + 1)**2 - 8 * (nir - red)))/2
        )

        # INSERT CHECKING CONDITION
        msavi[msavi > 1] = 1
        msavi[msavi < -1] = -1

        # save msavi raster image
        msavi_image = open('./msavi_landsat.tiff', 'w', driver='GTiff',
                           width=band5.width, height=band5.height,
                           count=1,
                           crs=band5.crs,
                           transform=band5.transform,
                           dtype='float64')
        msavi_image.write(msavi, 1)
        msavi_image.close()

        if show_flag:
            msavi = open('savi_landsat.tiff')
            show(msavi, cmap='Greens')


def image_display_landsat():
    """
    Displays the images of landsat indices in a folder one at a time
    """
    ndmi = open('ndmi_landsat.tiff')
    ndvi = open('ndvi_landsat.tiff')
    savi = open('savi_landsat.tiff')
    msavi = open('msavi_landsat.tiff')
    show(ndmi, cmap='Blues')
    show(ndvi, cmap='Greens')
    show(savi, cmap='Greens')
    show(msavi, cmap='Greens')


def execute_landsat(show_individual=False, show_all=False, show_only=False):
    """
    Executes the process of calculation of indices for landsat images

    :param show_individual: setting for showing individual images while calculating indices
    :type show_individual: bool
    :param show_all: setting to show all the indices one by one after calculation
    :type show_all: bool
    :param show_only: setting for only showing images of existing indices, if any
    :type show_only: bool
    """
    try:
        if show_only:
            image_display_landsat()
            exit()
        ndmi_calc_landsat(show_flag=show_individual)
        ndvi_calc_landsat(show_flag=show_individual)
        savi_calc_landsat(show_flag=show_individual)
        msavi_calc_landsat(show_flag=show_individual)
        if show_all:
            image_display_landsat()
    except RuntimeError:
        print('Unable to show images')


def landsat_test():
    """
    Test case for the index_calculator_landsat.py file
    """
    execute_landsat(show_individual=True)
    band_returner_landsat(show_list=True)
