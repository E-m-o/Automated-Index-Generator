import os
import pandas as pd
from landsatxplore.api import API
from lib.crawlers.csv_reader import *
from web.crawlers.web_crawler_earthexplorer import get_dates
import random
import warnings

warnings.filterwarnings("ignore")

global data
global data_grouped

username = "vineet"
password = "EROS#3mobiscuit"


def satellite_selector():
    return input("Choose satellite:\n1. Landsat 8\n2. Landsat 7\n3. Landsat 5\n4. Sentinel\n")


def indices_requested():

    def mapper(choice):
        return True if choice=='y' else False

    indice_list = ["ndmi", "ndvi", "savi", "msavi", "ndwi"]
    print("Type yes(y) or no(n) when prompted against the index name.")

    t = [input(f"{i}: ") for i in indice_list]
    temp = list(map(mapper, t))

    return temp

def scene_finder(api=None, sat_choice=None, date=None, coordinates=None):
    """
    Returns the scenes found for each query
    :rtype: list
    :return: Scenes searched
    :param api:
    :param date:
    :param coordinates:
    :param sat_choice: Satellite choice -- 1 -> Landsat, 2 -> Landsat, 3 -> Landsat, 4 -> Sentinel
    :type sat_choice: str
    """
    scenes = None
    landsat_8_collection = "landsat_8_c1"
    sentinel_collection = "sentinel_2a"
    landsat_5_collection = "landsat_8_c1"
    landsat_7_collection = "landsat_etm_c1"

    [xmin, ymin, xmax, ymax] = coordinates
    # print(xmin, ymin, xmax, ymax)
    if sat_choice == "1":
        scenes = api.search(
            dataset=landsat_8_collection,
            bbox=(xmin,
                  ymin,
                  xmax,
                  ymax),
            start_date=date[0],
            end_date=date[1],
        )
        # print(scenes)
    elif sat_choice == "2":
        scenes = api.search(
            dataset=landsat_7_collection,
            bbox=(xmin,
                  ymin,
                  xmax,
                  ymax),
            start_date=date[0],
            end_date=date[1],
        )
    elif sat_choice == "3":
        scenes = api.search(
            dataset=landsat_5_collection,
            bbox=(xmin,
                  ymin,
                  xmax,
                  ymax),
            start_date=date[0],
            end_date=date[1],
        )
    elif sat_choice == "4":
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

    if sat_choice == "1" or sat_choice == "2" or sat_choice == "3":
        # try:
        #     os.chdir()
        for scene in scene_list:
            print(scene[1])
            if id == 0:
                os.system(
                    f"landsatxplore download {scene[0]} --output /home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.{request}/Start_date --username {username} --password {password}")
            elif id == 1:
                os.system(
                    f"landsatxplore download {scene[0]} --output /home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.{request}/End_date --username {username} --password {password}")
    # elif sat_choice == '2':
    #     for scene in scene_list:
    #         print(scene[1])
    #         if id == 0:
    #             os.system(
    #                 f"landsatxplore download {scene[0]} --output /home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.{request}/Start_date --username {username} --password {password}")
    #         elif id == 1:
    #             os.system(
    #                 f"landsatxplore download {scene[0]} --output /home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.{request}/End_date --username {username} --password {password}")
    # elif sat_choice == '3':
    #     for scene in scene_list:
    #         print(scene[1])
    #         if id == 0:
    #             os.system(
    #                 f"landsatxplore download {scene[0]} --output /home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.{request}/Start_date --username {username} --password {password}")
    #         elif id == 1:
    #             os.system(
    #                 f"landsatxplore download {scene[0]} --output /home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Request.{request}/End_date --username {username} --password {password}")
    elif sat_choice == '4':
        for scene in scene_list:
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
    if sat_choice == "1" or sat_choice == "2" or sat_choice == "3":
        columns = ['entity_id', 'wrs_path', 'wrs_row', 'cloud_cover', 'start_time', 'landsat_product_id']
    # elif sat_choice == '2':
    #     columns = ['entity_id', 'wrs_path', 'wrs_row', 'cloud_cover', 'start_time', 'landsat_product_id']
    # elif sat_choice == '3':
    #     columns = ['entity_id', 'wrs_path', 'wrs_row', 'cloud_cover', 'start_time', 'landsat_product_id']
    elif sat_choice == '4':
        columns = ['entity_id', 'tile_number', 'cloud_cover', 'acquisition_start_date', 'sentinel_entity_id']
    for scene in scenes:
        temp = {column: scene[column] for column in columns}
        data = data.append(temp, ignore_index=True)
    #         print(temp)

    down_list = []

    if sat_choice == "1" or sat_choice == "2" or sat_choice == "3":
        data_grouped = data.groupby(['wrs_path', 'wrs_row'])

        for group in data_grouped.groups:
            grp = data_grouped.get_group(group)
            grp.sort_values(['cloud_cover'], inplace=True)
            down_list.append([grp.iloc[0]['entity_id'], grp.iloc[0]['landsat_product_id']])
    # elif sat_choice == '2':
    #     data_grouped = data.groupby(['wrs_path', 'wrs_row'])
    #
    #     for group in data_grouped.groups:
    #         grp = data_grouped.get_group(group)
    #         grp.sort_values(['cloud_cover'], inplace=True)
    #         down_list.append([grp.iloc[0]['entity_id'], grp.iloc[0]['landsat_product_id']])
    # elif sat_choice == '3':
    #     data_grouped = data.groupby(['wrs_path', 'wrs_row'])
    #
    #     for group in data_grouped.groups:
    #         grp = data_grouped.get_group(group)
    #         grp.sort_values(['cloud_cover'], inplace=True)
    #         down_list.append([grp.iloc[0]['entity_id'], grp.iloc[0]['landsat_product_id']])
    elif sat_choice == '4':
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
    return down_list, None


def downloader(sat_choice=None, block=2027, dates=None, indice_requested=[False, False, False, True, False], test=False, root=str):
    api = API(username, password)
    if test==True:
        sat_choice = satellite_selector()
        dates = get_dates(sat_choice=sat_choice, test=False)
        indice_requested = indices_requested()
    request = str(random.randint(5,101))
    try:
        try:
            os.rmdir(f'./Images/Request.{request}')
        except:
            os.mkdir(f'./Images/Request.{request}')
            os.mkdir(f"./Images/Request.{request}/Start_date")
            os.mkdir(f"./Images/Request.{request}/End_date")
    except:
        pass
    co_ord = csv_crawler(block=block, clipper=True, root=root)
    # print(co_ord)
    for (id, date) in enumerate(dates):
        scenes = scene_finder(api, sat_choice, date, coordinates=co_ord)
        print(scenes)
        # scene_list, scene_data = download_selector(scenes, test=True, sat_choice=sat_choice)
        scene_list, scene_data = download_selector(scenes, sat_choice=sat_choice)
        scene_downloader(scene_list, id=id, request=request, sat_choice=sat_choice)

    api.logout()

    return sat_choice, indice_requested

# downloader()
