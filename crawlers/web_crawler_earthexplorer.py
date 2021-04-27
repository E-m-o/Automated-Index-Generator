import os

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from datetime import datetime, timedelta
from pandas import DataFrame

path_dict = {
    # login
    'login_page': 'https://ers.cr.usgs.gov/login',
    'user': 'div.inputContainer:nth-child(1) > input:nth-child(1)',
    'password': 'div.inputContainer:nth-child(2) > input:nth-child(1)',
    'login_button': '#loginButton',
    'login_check': '#profileNameContainer',
    # earth explorer
    'explorer_page': 'https://earthexplorer.usgs.gov/',
    # search criteria tab
    'search_criteria_tab': '#tab1',
    'shapefile_tab': '#tabUpload',
    # shapefile selector
    'shapefile_selector': '#fileUploadForm > select:nth-child(2)',
    'upload': '#fileUploadFileInput',
    'upload_status': '#uploadProgressTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > button:nth-child(1)',
    'map_use': '#coordUseMap',
    # add coords
    'decimal': '#lat_lon_section > label:nth-child(3)',
    'add_coord': '#coordEntryAdd',
    'add_lat': '#coordEntryDialogArea > div:nth-child(2) > input:nth-child(1)',
    'add_long': '#coordEntryDialogArea > div:nth-child(5) > input:nth-child(1)',
    'add_button_xpath': '/html/body/div[5]/div[3]/div/button[1]',
    'cancel_add_coords':
        'body > div:nth-child(14) > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(2)',
    'clear_coords': '#coordEntryClear',
    # date setter
    'date_start': '#start_linked',
    'date_end': '#end_linked',
    # datasets tab
    'datasets_tab': '#tab2',
    'lsat_dropdown': '#cat_210 > div:nth-child(1)',
    'lsat_c1': '#cat_2318 > div:nth-child(1)',
    'lsat_c1_l1': '#cat_1471 > div:nth-child(1)',
    'lsat_c1_l1_8': '#coll_5e83d0b656b77cf3',
    'sentinel_dropdown': '#cat_1253 > div:nth-child(1)',
    'sentinel_2': '#coll_5e83a42ca9977c30',
    'event': 'div.ui-dialog:nth-child(14) > div:nth-child(3) > div:nth-child(1) > button:nth-child(1)',
    'add_criteria': 'input.unselectable:nth-child(2)',
    # results tab
    'results_add_criteria_tab': 'div.tabButtonContainer:nth-child(5) > input:nth-child(2)',
    'results_datasets_tab': 'input.unselectable:nth-child(3)',
    'searching_status': '#searchDialog > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1)',
    'result_rows': '/html/body/div[1]/div/div/div[2]/div[2]/div[4]/form/div[2]/div[2]/div/table/tbody/tr/td/a',
    'row_links': '/html/body/div[1]/div/div/div[2]/div[2]/div[4]/form/div[2]/div[2]/div/table/tbody/tr',
    'meta_close': 'div.ui-dialog:nth-child(11) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2)',
    # metadata extractors landsat
    'name_landsat': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]',
    'wrs_path_landsat': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[6]/td[2]',
    'wrs_row_landsat': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[7]/td[2]',
    'cloud_cover_landsat': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[17]/td[2]',
    'UL_lat_landsat': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[50]/td[2]',
    'UL_long_landsat': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[51]/td[2]',
    'UR_lat_landsat': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[52]/td[2]',
    'UR_long_landsat': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[53]/td[2]',
    'LL_lat_landsat': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[54]/td[2]',
    'LL_long_landsat': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[55]/td[2]',
    'LR_lat_landsat': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[56]/td[2]',
    'LR_long_landsat': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[57]/td[2]',
    'center_lat': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[48]/td[2]',
    'center_long': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[49]/td[2]',
    # metadata extractors sentinel
    'name_sentinel': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[14]/td[2]',
    'tile_number': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[4]/td[2]',
    'cloud_cover_sentinel': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[5]/td[2]',
    'UL_lat_sentinel': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[34]/td[2]',
    'UL_long_sentinel': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[35]/td[2]',
    'UR_lat_sentinel': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[36]/td[2]',
    'UR_long_sentinel': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[37]/td[2]',
    'LR_lat_sentinel': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[38]/td[2]',
    'LR_long_sentinel': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[39]/td[2]',
    'LL_lat_sentinel': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[40]/td[2]',
    'LL_long_sentinel': '/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[41]/td[2]',
    # download
    'download_options': '/html/body/div[1]/div/div/div[2]/div[2]/div[4]/form/div[2]/div[2]/div/table/tbody/tr/td/ul/li/div/a[5]',
    'download_button_landsat': '/html/body/div[6]/div[2]/div/div[2]/div[5]/div[1]/button',
    'download_button_sentinel': '/html/body/div[6]/div[2]/div/div[2]/div[1]/div[1]/button',
    'download_close': '/html/body/div[6]/div[1]/button'
    # 'download_button_sentinel': 'div.row:nth-child(1) > div:nth-child(1) > button:nth-child(1)'
}

counter = {
    'login': 0,
    'explorer': 0
}

flags = {
    'login': False,
    'explorer': {
        'access': False,
        'upload': False,
        'date': False,
        'tab': False,
        'landsat_selector': False,
        'results': False,
        'metadata': False
    }
}

clean_flags = {
    'login': True,
    'explorer': {
        'access': True,
        'upload': True,
        'date': True,
        'tab': True,
        'landsat_selector': True,
        'results': True,
        'metadata': True
    }
}


# noinspection PyShadowingNames
def make_driver(id=None, base_path=None, firefox=True, chrome=False):
    """
    Makes the driver object and returns it
    :return: Driver for the program
    :rtype: selenium.webdriver.Firefox
    """
    if firefox:
        # binary = FirefoxBinary("/usr/bin/firefox")
        # profile = FirefoxProfile("/home/emo/.mozilla/firefox/by25928h.selenium")
        # profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        driver = webdriver.Firefox()
        driver.maximize_window()
        return driver
    if chrome:
        print(id)
        options = webdriver.ChromeOptions()
        down_dir_opt = None
        if id == 0:
            down_dir_opt = {'download.default_directory': f"{os.path.join(base_path, 'Start_date')}"}
        if id == 1:
            down_dir_opt = {'download.default_directory': f"{os.path.join(base_path, 'End_date')}"}
        options.add_experimental_option('prefs', down_dir_opt)
        driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)
        return driver


def create_dir(base_path=None):
    try:
        os.mkdir(base_path)
        os.mkdir(os.path.join(base_path, "Start_date"))
        os.mkdir(os.path.join(base_path, "End_date"))
    except FileExistsError:
        pass
    return


def switch_tabs(key):
    """
    Switches the tab on the EarthExplorer site

    :param key: Key for changing tabs
    :type key: str
    """
    print('Switching tabs...')
    while True:
        try:
            tab = driver.find_element_by_css_selector(path_dict[key])
            tab.click()
            flags['explorer']['tab'] = True
            print('Tab switch successful !!!')
            break
        except NoSuchElementException:
            print('Tab switch failed -> No such element')
            flags['explorer']['tab'] = False
        except TimeoutException:
            print('Tab switch failed -> Timeout')
            flags['explorer']['tab'] = False


def access_login():
    """
    Accesses the login page of EROS Registration System
    """
    print('==========================================')
    print('Accessing site -> EROS Registration System')
    while True:
        try:
            driver.get(path_dict['login_page'])
            print('Accessed site  ->', driver.title)
            flags['login'] = True
            time.sleep(2)
            break
        except TimeoutException:
            flags['login'] = False
        except WebDriverException:
            flags['login'] = False
            access_login()


def login():
    """
    Logs in to the EROS Registration System
    """
    print('====================')
    print('Attempting to log in')
    while True:
        try:

            # if not driver.find_element_by_css_selector(path_dict['login_check']):

            username = driver.find_element_by_css_selector(path_dict['user'])
            username.send_keys('vineet')

            password = driver.find_element_by_css_selector(path_dict['password'])
            password.send_keys('EROS#3mobiscuit')

            submit = driver.find_element_by_css_selector(path_dict['login_button'])
            submit.click()

            time.sleep(10)

            login_waiter = WebDriverWait(driver, 5)
            login_waiter.until(lambda ele: ele.find_element_by_css_selector(path_dict['login_check']))

            print('Log in successful !!!')
            flags['login'] = True
            break
        except TimeoutException:
            print('Failed to log in -> Timeout')
            flags['login'] = False
        except NoSuchElementException:
            print('Failed to log in -> No such element')
            time.sleep(2)
            flags['login'] = False
            # login()


def satellite_choice(test=False):
    """
    Gets the input of the satellite choice of the user
    :param test: Test case identifier
    :type test: bool
    :return: Satellite choice -> 1. Landsat | 2. Sentinel
    :rtype: str
    """
    if test:
        return "2"
    while True:
        choice = input("Choose satellite: \n1. Landsat \n2.Sentinel \nYour choice: ")
        if choice == "1":
            return choice
        if choice == "2":
            return choice
        else:
            print('Invalid input \nRetry')


def get_dates(sat_choice='1', test=False):
    """
    Gets the time_period of interest from the user
    :param sat_choice: Satellite choice -> 1. Landsat | 2. Sentinel
    :type sat_choice: str
    :param test: test case dates
    :type test: bool
    :return: Start and ends dates
    :rtype: list
    """
    if test:
        start_date_entry = '01/01/2021'
        end_date_entry = '03/17/2021'
        return [[start_date_entry, end_date_entry]]
    else:
        start_date_entry = input('Enter a start date (format - mm/dd/yyyy) -> ')
        end_date_entry = input('Enter a end date (format - mm/dd/yyyy) -> ')

        dates = []
        today = datetime.today()
        for date_entry in [start_date_entry, end_date_entry]:
            try:
                month, day, year = map(int, date_entry.split('/'))
                date_entry = datetime(year, month, day)
                if date_entry >= today:
                    date_entry = today
                dates.append(date_entry)
            except ValueError as err:
                print(err)

        try:
            date_start = dates[0]
            date_end = dates[1]
            if date_start > date_end:
                print("End date cannot be older than start date")
                return

            date_list = []
            td = low_date = high_date = None
            for date in dates:
                if date.date() != today.date():
                    if sat_choice == '1':
                        td = timedelta(8)
                    elif sat_choice == '2':
                        td = timedelta(5)
                    low_date = date - td
                    high_date = date + td
                elif date.date() == today.date():
                    if sat_choice == '1':
                        td = timedelta(16)
                    elif sat_choice == '2':
                        td = timedelta(10)
                    low_date = date - td
                    high_date = date

                thresh_dates = [low_date, high_date]

                low_year, low_month, low_day = thresh_dates[0].year, thresh_dates[0].month, thresh_dates[0].day
                high_year, high_month, high_day = thresh_dates[1].year, thresh_dates[1].month, thresh_dates[1].day

                low_date_str = "/".join([str(low_month), str(low_day), str(low_year)])
                high_date_str = "/".join([str(high_month), str(high_day), str(high_year)])

                date_list.append([low_date_str, high_date_str])
            print(date_list)
            return date_list
        except IndexError:
            print("Invalid date entry... Try again")
            dates = get_dates()
            return dates

def access_explorer():
    """
    Accesses the page of EarthExplorer
    """
    print('===============================')
    print('Accessing site -> EarthExplorer')
    while True:
        try:
            driver.get(path_dict['explorer_page'])
            print('Accessed site  ->', driver.title)
            flags['explorer']['access'] = True
            break
        except TimeoutException:
            flags['explorer']['access'] = False
        except WebDriverException:
            flags['explorer']['access'] = False


def upload_file(path_):
    """
    Uploads the shapefile at the given path

    :param path_: path of the shapefile
    :type path_: str
    """
    print('=========================')
    print('Attempting file upload...')
    while True:
        try:
            switch_tabs('search_criteria_tab')

            upload_tab = driver.find_element_by_css_selector(path_dict['shapefile_tab'])
            upload_tab.click()
            time.sleep(1)

            shapefile_selector = driver.find_element_by_css_selector(path_dict['shapefile_selector'])
            selector = Select(shapefile_selector)
            selector.select_by_value(value="shapefile")

            upload = driver.find_element_by_css_selector(path_dict['upload'])
            upload.send_keys(path_)

            try:
                upload_waiter = WebDriverWait(driver, 3)
                upload_waiter.until(
                    lambda ele: ele.find_element_by_css_selector(path_dict['upload_status']).get_attribute(
                        name="data-action") == "close")
            except TimeoutException:
                pass

            upload_status = driver.find_element_by_css_selector(path_dict['upload_status'])
            upload_status.click()
            flags['explorer']['upload'] = True
            print('File upload successful !!!')
            break
        except NoSuchElementException:
            print('Failed to upload file -> No such element error')
            flags['explorer']['upload'] = False
        except ElementNotInteractableException:
            flags['explorer']['upload'] = False
        except TimeoutException:
            print('Failed to upload file -> Timeout error')
            flags['explorer']['upload'] = False


def add_date(date_list=(str, str), test=False):
    """
    Adds the date criteria for search of the relevant images
    :param test: Test case
    :type test: bool
    :type date_list: (str, str)
    :param date_list: Start and end dates
    """
    print('==========================')
    print('Attempting to set dates...')
    if test:
        for date in date_list:
            print(date[0])
            print(date[1])
        return
    switch_tabs('search_criteria_tab')
    while True:
        try:
            date_start = driver.find_element_by_css_selector(path_dict['date_start'])
            date_start.clear()
            date_start.send_keys(date_list[0])

            date_end = driver.find_element_by_css_selector(path_dict['date_end'])
            date_end.clear()
            date_end.send_keys(date_list[1])
            flags['explorer']['date'] = True
            print('Dates set successfully !!!')
            break
        except UnexpectedAlertPresentException:
            flags['explorer']['date'] = False
            print('Failed to set dates -> Unexpected alert present')


def set_dataset(sat_choice='1'):
    """
    Selects the Landsat Collection 1 Level-1 dataset or the Sentinel-2 dataset
    :param sat_choice: Satellite choice -> 1. Landsat | 2. Sentinel
    :type sat_choice: str
    """
    print('===============================')
    print('Attempting to select dataset...')
    switch_tabs('datasets_tab')
    while True:
        try:
            # landsat_waiter = WebDriverWait(driver, 10)
            # landsat_waiter.until(lambda ele: ele.find_element_by_css_selector(css_dict['lsat_dropdown']))

            if sat_choice == "1":
                if not driver.find_element_by_css_selector(path_dict['lsat_c1_l1_8']).is_displayed():
                    lsat_dropdown = driver.find_element_by_css_selector(path_dict['lsat_dropdown'])
                    lsat_dropdown.click()

                    lsat_c1 = driver.find_element_by_css_selector(path_dict['lsat_c1'])
                    lsat_c1.click()

                    lsat_c1_l1 = driver.find_element_by_css_selector(path_dict['lsat_c1_l1'])
                    lsat_c1_l1.click()

                    lsat_c1_l1_8 = driver.find_element_by_css_selector(path_dict['lsat_c1_l1_8'])
                    lsat_c1_l1_8.click()

                try:
                    WebDriverWait(driver, 10).until(lambda ele: ele.find_element_by_css_selector(path_dict['event']))
                    event = driver.find_element_by_css_selector(path_dict['event'])
                    event.click()
                except NoSuchElementException:
                    pass
                except TimeoutException:
                    pass
            elif sat_choice == "2":
                if not driver.find_element_by_css_selector(path_dict['sentinel_2']).is_displayed():
                    sentinel_dropdown = driver.find_element_by_css_selector(path_dict['sentinel_dropdown'])
                    sentinel_dropdown.click()

                    sentinel_2 = driver.find_element_by_css_selector(path_dict['sentinel_2'])
                    sentinel_2.click()

                try:
                    WebDriverWait(driver, 10).until(lambda ele: ele.find_element_by_css_selector(path_dict['event']))
                    event = driver.find_element_by_css_selector(path_dict['event'])
                    event.click()
                except NoSuchElementException:
                    pass
                except TimeoutException:
                    pass

            flags['explorer']['landsat_selector'] = True
            print('Dataset set successfully !!!')
            break
        except NoSuchElementException:
            flags['explorer']['landsat_selector'] = False
            print('Waiting for dataset list to load')
            time.sleep(2)


def get_results():
    """
    Fetches the results of the performed search
    """
    # try:
    #     results_tab = driver.find_element_by_css_selector(css_dict['results_add_criteria_tab'])
    #     results_tab.click()
    # except NoSuchElementException:
    print('==============================')
    print('Attempting to fetch results...')
    while True:
        try:
            results_tab = driver.find_element_by_css_selector(path_dict['results_datasets_tab'])
            results_tab.click()
            time.sleep(2)
            WebDriverWait(driver, 10).until(lambda ele: ele.find_elements_by_xpath(path_dict['result_rows']))
            flags['explorer']['results'] = True
            print('Results fetched successfully !!!')
            break
        except NoSuchElementException:
            flags['explorer']['results'] = False
            print('Failed to fetch results -> No such element')
            time.sleep(1)
        except ElementNotInteractableException:
            flags['explorer']['results'] = False
            print('Failed to fetch results -> Element not interactable')
            time.sleep(1)
        except ElementClickInterceptedException:
            flags['explorer']['results'] = False
            print('Failed to fetch results -> Element click intercepted')
            time.sleep(1)


def get_metadata(sat_choice=str):
    """
    Looks for the metadata of each result image and returns it as a dictionary
    :param sat_choice: Satellite choice -> 1. Landsat | 2. Sentinel
    :type sat_choice: str
    :return:  Dictionary of relevant metadata
    :rtype: dict
    """
    print('======================')
    print('Extracting metadata...')
    meta_ret = {
        'result_index': [],
        'name': [],
        'wrs_path': [],
        'wrs_row': [],
        'tile_number': [],
        'cloud_cover': [],
        'ul_lat': [],
        'ul_long': [],
        'ur_lat': [],
        'ur_long': [],
        'll_lat': [],
        'll_long': [],
        'lr_lat': [],
        'lr_long': [],
        'center_lat': [],
        'center_long': []
    }
    while True:
        try:
            rows = driver.find_elements_by_xpath(path_dict['result_rows'])
            # row_images = driver.find_elements_by_xpath(path_dict['row_links'])
            print('Found {} results'.format(len(rows)))
            for (index, row) in enumerate(rows, 1):
                print("Extracting metadata for row {0:02d} images".format(index))
                row.click()
                time.sleep(5)
                if sat_choice == '1':
                    name = driver.find_element_by_xpath(path_dict['name_landsat']).get_attribute("innerHTML")
                    wrs_path = driver.find_element_by_xpath(path_dict['wrs_path_landsat']).get_attribute("innerHTML")
                    wrs_row = driver.find_element_by_xpath(path_dict['wrs_row_landsat']).get_attribute("innerHTML")
                    cloud_cover_land = driver.find_element_by_xpath(path_dict['cloud_cover_landsat']).get_attribute(
                        "innerHTML")
                    ul_lat = driver.find_element_by_xpath(path_dict['UL_lat_landsat']).get_attribute("innerHTML")
                    ul_long = driver.find_element_by_xpath(path_dict['UL_long_landsat']).get_attribute("innerHTML")
                    ur_lat = driver.find_element_by_xpath(path_dict['UR_lat_landsat']).get_attribute("innerHTML")
                    ur_long = driver.find_element_by_xpath(path_dict['UR_long_landsat']).get_attribute("innerHTML")
                    ll_lat = driver.find_element_by_xpath(path_dict['LL_lat_landsat']).get_attribute("innerHTML")
                    ll_long = driver.find_element_by_xpath(path_dict['LL_long_landsat']).get_attribute("innerHTML")
                    lr_lat = driver.find_element_by_xpath(path_dict['LR_lat_landsat']).get_attribute("innerHTML")
                    lr_long = driver.find_element_by_xpath(path_dict['LR_long_landsat']).get_attribute("innerHTML")
                    center_lat = driver.find_element_by_xpath(path_dict['center_lat']).get_attribute("innerHTML")
                    center_long = driver.find_element_by_xpath(path_dict['center_long']).get_attribute("innerHTML")

                    meta_ret['result_index'].append(index)
                    meta_ret['name'].append(name)
                    meta_ret['wrs_path'].append(wrs_path)
                    meta_ret['wrs_row'].append(wrs_row)
                    meta_ret['tile_number'].append(None)
                    meta_ret['cloud_cover'].append(cloud_cover_land)
                    meta_ret['ul_lat'].append(ul_lat)
                    meta_ret['ul_long'].append(ul_long)
                    meta_ret['ur_lat'].append(ur_lat)
                    meta_ret['ur_long'].append(ur_long)
                    meta_ret['ll_lat'].append(ll_lat)
                    meta_ret['ll_long'].append(ll_long)
                    meta_ret['lr_lat'].append(lr_lat)
                    meta_ret['lr_long'].append(lr_long)
                    meta_ret['center_lat'].append(center_lat)
                    meta_ret['center_long'].append(center_long)

                elif sat_choice == '2':
                    name = driver.find_element_by_xpath(path_dict['name_sentinel']).get_attribute("innerHTML")
                    tile_number = driver.find_element_by_xpath(path_dict['tile_number']).get_attribute("innerHTML")
                    cloud_cover_land = driver.find_element_by_xpath(path_dict['cloud_cover_sentinel']).get_attribute(
                        "innerHTML")
                    ul_lat = driver.find_element_by_xpath(path_dict['UL_lat_sentinel']).get_attribute("innerHTML")
                    ul_long = driver.find_element_by_xpath(path_dict['UL_long_sentinel']).get_attribute("innerHTML")
                    ur_lat = driver.find_element_by_xpath(path_dict['UR_lat_sentinel']).get_attribute("innerHTML")
                    ur_long = driver.find_element_by_xpath(path_dict['UR_long_sentinel']).get_attribute("innerHTML")
                    ll_lat = driver.find_element_by_xpath(path_dict['LL_lat_sentinel']).get_attribute("innerHTML")
                    ll_long = driver.find_element_by_xpath(path_dict['LL_long_sentinel']).get_attribute("innerHTML")
                    lr_lat = driver.find_element_by_xpath(path_dict['LR_lat_sentinel']).get_attribute("innerHTML")
                    lr_long = driver.find_element_by_xpath(path_dict['LR_long_sentinel']).get_attribute("innerHTML")
                    center_lat = driver.find_element_by_xpath(path_dict['center_lat']).get_attribute("innerHTML")
                    center_long = driver.find_element_by_xpath(path_dict['center_long']).get_attribute("innerHTML")

                    meta_ret['result_index'].append(index)
                    meta_ret['name'].append(name)
                    meta_ret['wrs_path'].append(None)
                    meta_ret['wrs_row'].append(None)
                    meta_ret['tile_number'].append(tile_number)
                    meta_ret['cloud_cover'].append(cloud_cover_land)
                    meta_ret['ul_lat'].append(ul_lat)
                    meta_ret['ul_long'].append(ul_long)
                    meta_ret['ur_lat'].append(ur_lat)
                    meta_ret['ur_long'].append(ur_long)
                    meta_ret['ll_lat'].append(ll_lat)
                    meta_ret['ll_long'].append(ll_long)
                    meta_ret['lr_lat'].append(lr_lat)
                    meta_ret['lr_long'].append(lr_long)
                    meta_ret['center_lat'].append(center_lat)
                    meta_ret['center_long'].append(center_long)

                while True:
                    try:
                        close = driver.find_element_by_css_selector(path_dict['meta_close'])
                        close.click()
                        break
                    except ElementClickInterceptedException:
                        print('Element click intercepted')
                        time.sleep(2)
                    except ElementNotInteractableException:
                        time.sleep(2)
                        print('Element not interactable')

            print('Metadata extraction successful !!!')
            flags['explorer']['metadata'] = True
            return meta_ret
        except NoSuchElementException:
            print('Failed to extract metadata -> No such element')
            time.sleep(2)
            flags['explorer']['metadata'] = False
        except TimeoutException:
            print('Failed to extract metadata -> Timeout')
            flags['explorer']['metadata'] = False


def download_selector(meta=dict, sat_choice="1", test=False):
    """
    Returns the download index of the results
    :param meta: Dictionary of metadata
    :type meta: dict
    :param sat_choice: Satellite choice -> 1. Landsat | 2. Sentinel
    :type sat_choice: str
    :return: List of selected results
    :rtype: list
    """
    data = DataFrame(meta)
    download_index = []
    if sat_choice == "1":
        data_grouped = data.groupby(['wrs_row', 'wrs_path'])
        download_index = []
        for group in data_grouped.groups:
            grp = data_grouped.get_group(group)
            print(grp)
            grp.sort_values(['cloud_cover'])
            mini = grp.iloc[-1]
            # print(mini['result_index'], mini['cloud_cover'])
            download_index.append([mini['result_index'], mini['name']])
            if test:
                return data, data_grouped, download_index
    elif sat_choice == "2":
        data_grouped = data.groupby(['tile_number'])
        download_index = []
        for group in data_grouped.groups:
            grp = data_grouped.get_group(group)
            # print(grp)
            grp.sort_values(['cloud_cover'])
            mini = grp.iloc[-1]
            # print(mini['result_index'], mini['cloud_cover'])
            download_index.append([mini['result_index'], mini['name']])


def waitUntilDownloadCompleted(maxTime=600):
    driver.execute_script("window.open()")
    # switch to new tab
    driver.switch_to.window(driver.window_handles[-1])
    # navigate to chrome downloads
    driver.get('chrome://downloads')
    # define the endTime
    # endTime = time.time() + maxTime
    while True:
        try:
            # get the download percentage
            downloadPercentage = driver.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            if downloadPercentage == 100:
                # exit the method once it's completed
                return downloadPercentage
        except:
            pass
        # wait for 1 second before checking the percentage next time
        time.sleep(1)
        # exit method if the download not completed with in MaxTime.
        # if time.time() > endTime:
        #     break


def download(download_index=None, sat_choice='1', test=False):
    """
    Downloads the relevant results
    :param test: Test case
    :type test: bool
    :param download_index: List of results to be downloaded
    :type download_index: list
    :param sat_choice: Satellite choice -> 1. Landsat | 2. Sentinel
    :type sat_choice: str
    """
    print('==============')
    while True:
        try:
            download_buttons = driver.find_elements_by_xpath(path_dict['download_options'])
            for data in download_index:
                print(data[0])
                download_buttons[data[0]-1].click()
                time.sleep(2)
                if not test:
                    if sat_choice == '1':
                        download_waiter = WebDriverWait(driver, 3)
                        download_waiter.until(
                            ec.element_to_be_clickable((By.XPATH, path_dict['download_button_landsat']))).click()
                        waitUntilDownloadCompleted()
                    elif sat_choice == '2':
                        download_waiter = WebDriverWait(driver, 3)
                        download_waiter.until(
                            ec.element_to_be_clickable((By.XPATH, path_dict['download_button_sentinel']))).click()
                        waitUntilDownloadCompleted()
                    print('Downloading {}'.format(data[1]))
                close = driver.find_element_by_xpath(path_dict['download_close'])
                close.click()
                print('Closing Download dialog for {}'.format(data[1]))
            break
        except ElementClickInterceptedException:
            print('Element click intercepted')
            time.sleep(2)
        except TimeoutException:
            print('Timeout')
            time.sleep(1)


def compare_flags():
    """
    Returns the truth value for flag comparison

    :return: Truth value for comparison
    :rtype: bool
    """
    if flags == clean_flags:
        return True
    else:
        return False


def add_coordinates(coords=None, test=False):
    """
    Adds the coordinates to the website search criteria
    :param coords: contains the coordinates to be added to the site, in order
    :type coords: list[float]
    :param test: test case flag, for independently using the driver
    :type test: bool
    """
    if test:
        global driver
        driver = make_driver()
    switch_tabs("search_criteria_tab")
    # noinspection PyUnboundLocalVariable
    driver.find_element_by_css_selector(path_dict['decimal']).click()
    count = 0
    while True:
        try:
            for coord in coords:
                # driver.switch_to.active_element()
                add_button_waiter = WebDriverWait(driver, 10)
                add_button_waiter.until(ec.element_to_be_clickable((By.CSS_SELECTOR, path_dict['add_coord'])))
                driver.find_element_by_css_selector(path_dict['add_coord']).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(path_dict['add_lat']).send_keys(str(coord[0]))
                driver.find_element_by_css_selector(path_dict['add_long']).send_keys(str(coord[1]))
                time.sleep(0.5)

                while count <= 4:
                    try:
                        count += 1
                        # add_button_waiter = WebDriverWait(driver, 10)
                        # add_button_waiter.until(ec.element_to_be_clickable((By.XPATH, path_dict['add_button_xpath'])))
                        add_button = driver.find_element_by_xpath(path_dict['add_button_xpath'])
                        driver.execute_script("arguments[0].click();", add_button)
                        break
                    except ElementClickInterceptedException:
                        time.sleep(5)
                        print("error - 1")
                    except NoSuchElementException:
                        time.sleep(5)
                        print("error - 2")
                    except TimeoutException:
                        print("error - 3")
            break
        finally:
            pass


# root = "/home/chiko/Storage/Projects/Raster_Image_Calculator"
# choice = "1"
#
# request = input("Enter Request Number -> ")
# # request = 2
# print(root)
# base_path = os.path.join(root, 'Images/Request.{}'.format(request))
#
# create_dir(base_path)
#
# driver = make_driver(id=0, base_path=base_path, chrome=True, firefox=False)
# access_login()
# login()
# access_explorer()
# upload_file(path_="/home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Test_files/test_mandala/mandlaBB.zip")
# date = get_dates(sat_choice=choice, test=True)[0]
# add_date(date_list=date)
# # SET DATASET
# set_dataset(sat_choice=choice)
#
# # RESULTS
# get_results()
#
# # GET METADATA
# meta = get_metadata(sat_choice=choice)
#
# # SELECT IMAGES TO DOWNLOAD
# data, data_grped, download_list = download_selector(meta, sat_choice=choice, test=True)
# # print(download_list)