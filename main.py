from analysis.analyser import analyser
from crawlers import web_crawler_earthexplorer as earth
from crawlers.csv_reader import csv_crawler
from crawlers.web_crawler_earthexplorer import *
from index_calculator.index_creator import generate_indices
from mosaic.mosaic_creator import mosaic_creator
from mosaic.unzipper import *
from atmos_correction.atmos_correction_landsat import apply_atmos_correction_landsat
# path_list = ['/home/emo/Storage/Projects/Raster_Image_Calculator/Images/Test_files/test_mandala/mandlaBB.zip']
# , '/home/emo/Storage/Projects/Raster_Image_Calculator/Test_files/test_mandala/mandlaBB-2.zip'

root = "/home/chiko/Storage/Projects/Raster_Image_Calculator"
choice = None

request = input("Enter Request Number -> ")
# request = 2
print(root)
base_path = os.path.join(root, 'Images/Request.{}'.format(request))

create_dir(base_path)


def downloader():
    # SELECT DATASET
    # choice = satellite_choice()
    # noinspection PyShadowingNames
    choice = "1"

    # GET DATES
    date_list = get_dates(sat_choice=choice, test=True)

    for (id, date) in enumerate(date_list):
        earth.driver = make_driver(id=id, base_path=base_path, chrome=True, firefox=False)

        # if counter['login'] == 0:  # Login only once per session
        #     counter['login'] = 1
            # LOGIN PAGE ACCESSED
        access_login()

            # ENTERING LOGIN DETAILS
        login()

        # if counter['explorer'] == 0:  # Access explorer only once per session
            # driver.refresh()

            # ACCESS EXPLORER
        access_explorer()

        # FILE UPLOAD
        # if id == 0:
        # coordinates = csv_crawler(test=True)
        # add_coordinates(coordinates)
        upload_file(path_="/home/chiko/Storage/Projects/Raster_Image_Calculator/Images/Test_files/test_mandala/mandlaBB.zip")

        # TODO: Add download paths -> START and END date

        # ADD DATES
        add_date(date_list=date)

        # SET DATASET
        set_dataset(sat_choice=choice)

        # RESULTS
        get_results()

        # GET METADATA
        meta = get_metadata(sat_choice=choice)

        # SELECT IMAGES TO DOWNLOAD
        download_list = download_selector(meta, sat_choice=choice)
        # print(download_list)
        # DOWNLOAD SELECTED IMAGES
        download(download_list, sat_choice=choice, test=False)

    counter['explorer'] += 1
    if compare_flags():
        print('Waiting for downloads to complete...')
        # print(meta_dict)
        # driver.quit()
    else:
        print(flags)


def processor():
    decompress_time = time.time()
    # DECOMPRESS IMAGES
    down_dir_dict = decompress(base_path)
    decompress_time = int(time.time() - decompress_time)

    atmos_time = time.time()
    # ATMOSPHERIC CORRECTION
    apply_atmos_correction_landsat(base_path)
    atmos_time = int(time.time() - atmos_time)

    index_time = time.time()
    # GENERATE INDICES
    generate_indices(down_dir_dict, test=False)
    index_time = int(time.time() - index_time)

    mosaic_time = time.time()
    # CREATE MOSAICS OF THE INDICES GENERATED
    mosaic_creator(base_path)
    mosaic_time = int(time.time() - mosaic_time)

    analysis_time = time.time()
    # # CREATE MOSAICS OF THE INDICES GENERATED
    analyser(base_path)
    analysis_time = int(time.time() - analysis_time)

    print("{}{:<}\n{}{:<}\n{}{:<}\n{}{:<}\n{}{:<}".format("Decompress", "{:10.2f}".format(decompress_time/60),
                                                          "Atmos     ", "{:10.2f}".format(atmos_time/60),
                                                          "Index     ", "{:10.2f}".format(index_time/60),
                                                          "Mosaic    ", "{:10.2f}".format(mosaic_time/60),
                                                          "Analysis  ", "{:10.2f}".format(analysis_time/60)))
    # print("{:<}{:<}{:<}{:<}".format(, ,
    #                                     , ,
    #                                     ))


downloader()
process_time = time.time()
processor()
process_time = time.time() - process_time
print("{:<12}".format("Total time"))
print("{:<12}".format(process_time/60))
