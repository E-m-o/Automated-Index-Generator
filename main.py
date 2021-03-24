from crawlers.index_creator import *
from crawlers.web_crawler_earthexplorer import *
from crawlers import web_crawler_earthexplorer as earth
import json

path_list = ['/home/emo/Storage/Projects/Raster_Image_Calculator/Test_files/test_mandala/mandlaBB.zip']
# , '/home/emo/Storage/Projects/Raster_Image_Calculator/Test_files/test_mandala/mandlaBB-2.zip'

earth.driver = make_driver()

for path in path_list:
    if counter['login'] == 0:
        # LOGIN PAGE ACCESSED
        access_login()

        # ENTERING LOGIN DETAILS
        login()
        counter['login'] = 1

    if counter['explorer'] == 0:
        # driver.refresh()

        # ACCESS EXPLORER
        access_explorer()

    # SELECT DATASET
    choice = satellite_choice()

    # GET DATES
    date_list = get_dates(sat_choice=choice)

    for date in date_list:
        # FILE UPLOAD
        upload_file(path)

        # ADD DATES
        add_date(date_list=date)

        # SET DATASET
        set_dataset(sat_choice=choice)

        # RESULTS
        get_results()

        # GET METADATA
        meta = get_metadata(sat_choice=choice)

        download_list = download_selector(meta, sat_choice=choice)
        download(download_list, sat_choice=choice, test=False)

    counter['explorer'] += 1
    if counter['explorer'] == len(path_list):
        if compare_flags():
            print('Closing browser...')
            # print(meta_dict)
            time.sleep(10)
            # driver.quit()
            break
    else:
        print(flags)

# meta_json = json.dumps(meta_dict, indent=2)
# print(meta_json)
# subdir_list = [x[0] for x in os.walk('.')]
# root = os.getcwd()
#
# crawler(subdir_list, root, test=True)
