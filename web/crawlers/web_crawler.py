# SCRIPT TO DOWNLOAD FILES FROM THE WEB

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    UnexpectedAlertPresentException, WebDriverException
from selenium.webdriver.support.select import Select
import time

# driver = webdriver.Firefox()
path = '/bin/chromedriver'
driver = webdriver.Chrome(path)
driver.implicitly_wait(3)
# driver.set_window_size(1200, 980)
driver.maximize_window()

# ALL CSS, NAME AND ID VALUES
css_dict = {
    'login_page': 'https://ers.cr.usgs.gov/login',
    'user': 'div.inputContainer:nth-child(1) > input:nth-child(1)',
    'password': 'div.inputContainer:nth-child(2) > input:nth-child(1)',
    'login_button': '#loginButton',
    'explorer_page': 'https://earthexplorer.usgs.gov/',
    'shapefile_tab': '#tabUpload',
    'shapefile_selector': '#fileUploadForm > select:nth-child(2)',
    'upload': '#fileUploadFileInput',
    'upload_status': '#uploadProgressTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(4) > button:nth-child(1)',
    'map_use': '#coordUseMap',
    'date_start': '#start_linked',
    'date_end': '#end_linked',
    'datasets_tab': '#tab2',
    'lsat_dropdown': '#cat_210 > div:nth-child(1)',
    'lsat_c1': '#cat_2318 > div:nth-child(1)',
    'lsat_c1_l1': '#cat_1471 > div:nth-child(1)',
    'lsat_c1_l1_8': '#coll_5e83d0b656b77cf3',
    'event': 'div.ui-dialog:nth-child(14) > div:nth-child(3) > div:nth-child(1) > button:nth-child(1)',
    'add_criteria': 'input.unselectable:nth-child(2)',
    'land_cloud': 'input.unselectable:nth-child(2)',
    'results': 'div.tabButtonContainer:nth-child(5) > input:nth-child(2)',
    'searching_status': '#searchDialog > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1)'}

login_count = 0
explorer_count = 0
# LOOP LOGIN
while True:
    flag_login = False
    login_count += 1
    try:
        # OPEN LOGIN
        driver.get(css_dict['login_page'])
        print(driver.title)

        username = driver.find_element_by_css_selector(css_dict['user'])
        username.send_keys('vineet')
        time.sleep(0.25)

        password = driver.find_element_by_css_selector(css_dict['password'])
        password.send_keys('EROS#3mobiscuit')
        time.sleep(0.25)

        submit = driver.find_element_by_css_selector(css_dict['login_button'])
        submit.click()

        # LOOP EXPLORER
        while True:
            flag_explorer = False
            explorer_count += 1
            try:
                # OPEN EARTH EXPLORER
                driver.get(css_dict['explorer_page'])
                print(driver.title)

                # CHANGE TO FILE UPLOAD TAB
                try:
                    upload_tab = driver.find_element_by_css_selector(css_dict['shapefile_tab'])
                    upload_tab.click()
                    time.sleep(1)

                    shapefile_selector = driver.find_element_by_css_selector(css_dict['shapefile_selector'])
                    selector = Select(shapefile_selector)
                    selector.select_by_value(value="shapefile")
                except RuntimeError:
                    pass

                # USE MAP TEST CASE
                # map_use = driver.find_element_by_css_selector(css_dict['map_use'])
                # map_use.click()

                # UPLOAD FILE
                upload = driver.find_element_by_css_selector(css_dict['upload'])
                upload.send_keys('/home/emo/Storage/Projects/Raster Image Calclulator/test_mandala/mandlaBB.zip')

                while True:
                    try:
                        upload_status = driver.find_element_by_css_selector(css_dict['upload_status'])
                        click = upload_status.get_attribute(name='data-action')
                        if click == "close":
                            upload_status.click()
                    except NoSuchElementException:
                        break

                # DATE ENTRY
                try:
                    date_start = driver.find_element_by_css_selector(css_dict['date_start'])
                    date_start.send_keys('01/01/2021')

                    date_end = driver.find_element_by_css_selector(css_dict['date_end'])
                    date_end.send_keys('01/31/2021')
                except UnexpectedAlertPresentException:
                    print('Invalid date input')

                # SWITCH TO DATASETS TAB
                try:
                    datasets_tab = driver.find_element_by_css_selector(css_dict['datasets_tab'])
                    datasets_tab.click()
                except RuntimeError:
                    pass

                # LOOP LANDSAT DROPDOWN
                while True:
                    flag_dropdown = False
                    try:
                        # #cat_210 > div:nth-child(1)
                        lsat_dropdown = driver.find_element_by_css_selector(css_dict['lsat_dropdown'])
                        lsat_dropdown.click()
                        time.sleep(.5)

                        # #cat_2318 > div:nth-child(1)
                        lsat_c1 = driver.find_element_by_css_selector(css_dict['lsat_c1'])
                        lsat_c1.click()
                        time.sleep(.5)

                        # #cat_1471 > div:nth-child(1)
                        lsat_c1_l1 = driver.find_element_by_css_selector(css_dict['lsat_c1_l1'])
                        lsat_c1_l1.click()
                        time.sleep(.5)

                        # #coll_5e83d0b656b77cf3
                        lsat_c1_l1_8 = driver.find_element_by_css_selector(css_dict['lsat_c1_l1_8'])
                        lsat_c1_l1_8.click()
                        time.sleep(.5)

                        try:
                            event = driver.find_element_by_css_selector(css_dict['event'])
                            event.click()
                        except NoSuchElementException:
                            pass

                        flag_dropdown = True
                    except NoSuchElementException:
                        pass
                    if flag_dropdown:
                        break

                add_criteria_tab = driver.find_element_by_css_selector(css_dict['add_criteria'])
                add_criteria_tab.click()

                # LOOP CLOUD COVER ATTRIBUTE
                # div.form_element:nth-child(4) > div:nth-child(1) > div:nth-child(2) > i:nth-child(2)
                # land_cloud = driver.find_element_by_css_selector(css_dict['land_cloud'])
                # land_cloud.click()

                results_tab = driver.find_element_by_css_selector(css_dict['results'])
                results_tab.click()

                while True:
                    try:
                        # #searchDialog > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1)
                        searching_status = driver.find_element_by_css_selector(css_dict['searching_status'])
                    except NoSuchElementException:
                        break
                flag_explorer = True
            except WebDriverException:
                if explorer_count == 5:
                    print('Unable to perform programmed actions on site - EarthExplorer')
                    break
                pass
            if flag_explorer:
                break

        flag_login = True
    except RuntimeError:
        # if login_count == 5:
        #     print('Unable to access site - EROS Registration System')
        break
        # time.sleep(1)
        pass
    if flag_login:
        break

time.sleep(10)
# driver.quit()
