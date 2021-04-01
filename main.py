from crawlers.web_crawler_earthexplorer import *
from index_calculator.index_creator import *
from mosaic.mosaic_creator import mosaic_creator
from mosaic.unzipper import *
from crawlers import web_crawler_earthexplorer as earth

path_list = ['/home/emo/Storage/Projects/Raster_Image_Calculator/Test_files/test_mandala/mandlaBB.zip']
# , '/home/emo/Storage/Projects/Raster_Image_Calculator/Test_files/test_mandala/mandlaBB-2.zip'


root = os.getcwd()
choice = None

request = input("Enter Request Number ->")
base_path = '/home/emo/Storage/Projects/Raster_Image_Calculator/Images/Request.{}'.format(request)


def downloader():
    earth.driver = make_driver()

    for path in path_list:
        path_flag = False
        while not path_flag:
            if counter['login'] == 0:  # Login only once per session
                # LOGIN PAGE ACCESSED
                access_login()

                # ENTERING LOGIN DETAILS
                login()
                counter['login'] = 1

            if counter['explorer'] == 0:  # Access explorer only once per session
                # driver.refresh()

                # ACCESS EXPLORER
                access_explorer()

            # SELECT DATASET
            choice = satellite_choice()

            # GET DATES
            date_list = get_dates(sat_choice=choice, test=False)

            for date in date_list:
                # FILE UPLOAD
                upload_file(path)

                # ADD DATES
                add_date(date_list=date, test=False)

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
                    print('Waiting for downloads to complete...')
                    # print(meta_dict)
                    time.sleep(10)
                    # driver.quit()
                    path_flag = True
                    break
            else:
                print(flags)


def processor():
    down_dir_dict = decompress(base_path)
    generate_indices(down_dir_dict, test=False)
    mosaic_creator(base_path)


# downloader()
processor()
