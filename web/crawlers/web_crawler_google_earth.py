from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import time

css_dict = {
    'google_earth': 'https://www.google.com/earth/',
    'launch_earth': 'div.ge-desktop-only:nth-child(3) > div:nth-child(1) > a:nth-child(1)',
    'draw_roi': '#content'
}

flags = {
    'earth': False,
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
    'earth': True,
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


def access_earth():
    """
    Accesses the page Google Earth
    """
    print('------------------------------------------')
    print('Accessing site -> Google Earth')
    while True:
        try:
            driver.get(css_dict['google_earth'])
            print('Accessed site  ->', driver.title)
            flags['earth'] = True
            time.sleep(2)
            break
        except TimeoutException:
            flags['earth'] = False
        except WebDriverException:
            flags['earth'] = False
            access_earth()


def earth_launcher():
    """
    Launches Earth
    """
    print('------------------------------------------')
    print('Launching -> Google Earth')
    while True:
        try:
            launch_earth = driver.find_element_by_css_selector(css_dict['launch_earth'])
            launch_earth.click()
            print('Launched  ->', driver.title)
            break
        except WebDriverException:
            pass


driver = webdriver.Firefox()
driver.implicitly_wait(3)

access_earth()
earth_launcher()
