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

from mosaic.index_creator import *
subdir_list = [x[0] for x in os.walk('.')]
root = os.getcwd()
crawler(subdir_list, root, test=False)
# print(os.system('ls'))
