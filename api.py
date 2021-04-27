import os
import pandas as pd
from datetime import datetime, timedelta
from landsatxplore.api import API
from crawlers.csv_reader import csv_crawler
from crawlers.web_crawler_earthexplorer import get_dates

import warnings
warnings.filterwarnings("ignore")

global data
global data_grouped

username = "vineet"
password = "EROS#3mobiscuit"

sat_choice = input("Choose satellite:\n1. Landsat\n2.Sentinel\n")


def scene_finder(api=None, sat_choice=None, date=None, coordinates=None):
    scenes = None
    landsat_collection = "landsat_8_c1"
    sentinel_collection = "sentinel_2a"

    [xmin, ymin, xmax, ymax] = coordinates
    # print(xmin, ymin, xmax, ymax)
    if sat_choice == "1":
        scenes = api.search(
            dataset=landsat_collection,
            bbox=(xmin,
                  ymin,
                  xmax,
                  ymax),
            start_date=date[0],
            end_date=date[1],
        )
    elif sat_choice == "2":
        scenes = api.search(
            dataset=sentinel_collection,
            bbox=(xmin,
                  ymin,
                  xmax,
                  ymax),
            start_date=date[0],
            end_date=date[1],
        )

    print(f"{len(scenes)} scenes found.")
    return scenes


def scene_downloader(scene_list=None, id=None, request=None):
    for scene in scene_list:
        print(scene[1])
        if id==0:
            os.system(
                f"landsatxplore download {scene[0]} --output /home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.{request}/Start_date --username {username} --password {password}")
        elif id==1:
            os.system(
                f"landsatxplore download {scene[0]} --output /home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.{request}/End_date --username {username} --password {password}")


def download_selector(scenes=None, test=False):
    data = pd.DataFrame()
    columns = ['entity_id', 'wrs_path', 'wrs_row', 'cloud_cover', 'start_time', 'landsat_product_id']
    for scene in scenes:
        temp = {column: scene[column] for column in columns}
        data = data.append(temp, ignore_index=True)
    #         print(temp)
    data_grouped = data.groupby(['wrs_path', 'wrs_row'])
    down_list = []
    for group in data_grouped.groups:
        grp = data_grouped.get_group(group)
        grp.sort_values(['cloud_cover'], inplace=True)
        # print(grp.loc[grp.index[0], ['wrs_path', 'wrs_row']])
        # print(grp)
        # print(f"min = {grp.iloc[0]['cloud_cover']}")
        # print(f"max = {grp.iloc[-1]['cloud_cover']}")
        # print("==========================================================================================")
        down_list.append([grp.iloc[0]['entity_id'], grp.iloc[0]['landsat_product_id']])

    if test:
        return down_list, data
    return down_list


def downloader():
    api = API(username, password)
    choice = "1"

    date_list = get_dates(sat_choice=choice, test=False)
    request = input("Enter request number ")
    co_ord = csv_crawler(block="Mandla", clipper=True)
    # print(co_ord)
    for (id, date) in enumerate(date_list):
        scenes = scene_finder(api, sat_choice, date, coordinates=co_ord)
        scene_list, scene_data = download_selector(scenes, test=True)
        scene_downloader(scene_list, id, request)

    api.logout()

downloader()