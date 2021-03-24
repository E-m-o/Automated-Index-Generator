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

import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os

os.chdir('/home/emo/Storage/Projects/Raster_Image_Calculator/Test_files/Temp/Start_date')
print(os.getcwd())

list_ = glob.glob('*.tar.gz')
# print(list_)

for gzip in list_:
    print('GUNZIPing {}'.format(gzip))
    os.system('gunzip -f -k {}'.format(gzip))

list_ = glob.glob('*.tar')

for tar in list_:
    name = tar.split('.')[0]
    try:
        os.mkdir(os.path.join(os.getcwd(), name))
    except FileExistsError:
        pass

lis_ = os.walk('.')
for lis in lis_:
    print(lis)
