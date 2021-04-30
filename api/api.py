import os
import pandas as pd
from landsatxplore.api import API
from lib.crawlers.csv_reader import csv_crawler
from web.crawlers.web_crawler_earthexplorer import get_dates

import warnings

warnings.filterwarnings("ignore")

global data
global data_grouped

username = "vineet"
password = "EROS#3mobiscuit"

sat_choice = input("Choose satellite:\n1. Landsat\n2.Sentinel\n")


def scene_finder(api=None, sat_choice=None, date=None, coordinates=None):
    """
    Returns the scenes found for each query
    :rtype: list
    :return: Scenes searched
    :param api:
    :param date:
    :param coordinates:
    :param sat_choice: Satellite choice -- 1 -> Landsat, 2 -> Sentinel
    :type sat_choice: str
    """
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


def scene_downloader(scene_list=None, id=None, request=None, sat_choice=None):
    for scene in scene_list:
        if sat_choice == '1':
            print(scene[1])
            if id == 0:
                os.system(
                    f"landsatxplore download {scene[0]} --output /home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.{request}/Start_date --username {username} --password {password}")
            elif id == 1:
                os.system(
                    f"landsatxplore download {scene[0]} --output /home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.{request}/End_date --username {username} --password {password}")
        elif sat_choice == '2':
            print(scene[1])
            if id == 0:
                os.system(
                    f"landsatxplore download {scene[0]} --output /home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.{request}/Start_date --username {username} --password {password}")
            elif id == 1:
                os.system(
                    f"landsatxplore download {scene[0]} --output /home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.{request}/End_date --username {username} --password {password}")


def download_selector(scenes=None, test=False, sat_choice=None):
    global data_grouped
    data = pd.DataFrame()
    columns = []
    if sat_choice == '1':
        columns = ['entity_id', 'wrs_path', 'wrs_row', 'cloud_cover', 'start_time', 'landsat_product_id']
    elif sat_choice == '2':
        columns = ['entity_id', 'tile_number', 'cloud_cover', 'acquisition_start_date', 'sentinel_entity_id']
    for scene in scenes:
        temp = {column: scene[column] for column in columns}
        data = data.append(temp, ignore_index=True)
    #         print(temp)

    down_list = []

    if sat_choice == '1':
        data_grouped = data.groupby(['wrs_path', 'wrs_row'])

        for group in data_grouped.groups:
            grp = data_grouped.get_group(group)
            grp.sort_values(['cloud_cover'], inplace=True)
            # print(grp.loc[grp.index[0], ['wrs_path', 'wrs_row']])
            # print(grp)
            # print(f"min = {grp.iloc[0]['cloud_cover']}")
            # print(f"max = {grp.iloc[-1]['cloud_cover']}")
            # print("==========================================================================================")
            down_list.append([grp.iloc[0]['entity_id'], grp.iloc[0]['landsat_product_id']])
    elif sat_choice == '2':
        data_grouped = data.groupby(['tile_number'])
        for group in data_grouped.groups:
            grp = data_grouped.get_group(group)
            grp.sort_values(['cloud_cover'], inplace=True)
            # print(grp.loc[grp.index[0], ['tile_number']])
            # print(grp)
            # print(f"min = {grp.iloc[0]['cloud_cover']}")
            # print(f"max = {grp.iloc[-1]['cloud_cover']}")
            # print("==========================================================================================")
            down_list.append([grp.iloc[0]['entity_id'], grp.iloc[0]['sentinel_entity_id']])
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
        scene_list, scene_data = download_selector(scenes, test=True, sat_choice=sat_choice)
        scene_downloader(scene_list, request)

    api.logout()


downloader()
