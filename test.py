# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# # object of ChromeOptions class
# path = '/bin/chromedriver'
# op = webdriver.ChromeOptions()
# # browser preferences
# p = {'download.default_directory': '/home/emo/Downloads/Temp'}
# # add options to browser
# op.add_experimental_option('prefs', p)
# # set chromedriver.exe path
# driver = webdriver.Chrome(executable_path=path,
#                           options=op)
# # maximize browser
# driver.maximize_window()
# # launch URL
# driver.get("https://www.seleniumhq.org/download/");
# # click download link
# l = driver.find_element_by_link_text("32 bit Windows IE")
# l.click()

# from mosaic.index_creator import *
# subdir_list = [x[0] for x in os.walk('.')]
# root = os.getcwd()
# crawler(subdir_list, root, test=False)
# # print(os.system('ls'))

import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt

# Open the file:
# raster = rasterio.open('/home/emo/Storage/Projects/Raster_Image_Calculator/Test_files/LC08_L1TP_144045_20210302_20210302_01_RT/LC08_L1TP_144045_20210302_20210302_01_RT_BQA.TIF')


# Normalize bands into 0.0 - 1.0 scale
def normalize(array):
    array_min, array_max = array.min(), array.max()
    return (array - array_min) / (array_max - array_min)


# Convert to numpy arrays
blue = rasterio.open('/home/emo/Storage/Projects/Raster_Image_Calculator/Test_files/LC08_L1TP_144045_20210302_20210302_01_RT/LC08_L1TP_144045_20210302_20210302_01_RT_B3.TIF')
red = rasterio.open('/home/emo/Storage/Projects/Raster_Image_Calculator/Test_files/LC08_L1TP_144045_20210302_20210302_01_RT/LC08_L1TP_144045_20210302_20210302_01_RT_B8.TIF')
green = rasterio.open('/home/emo/Storage/Projects/Raster_Image_Calculator/Test_files/LC08_L1TP_144045_20210302_20210302_01_RT/LC08_L1TP_144045_20210302_20210302_01_RT_B4.TIF')

blue_ = blue.read(1)
red_ = red.read(1)
green_ = green.read(1)
# Normalize band DN
blue_norm = normalize(blue_)
red_norm = normalize(red_)
green_norm = normalize(green_)

# Stack bands
nrg = np.stack((red_norm, green_norm, blue_norm))

# View the color composite
show(nrg)
