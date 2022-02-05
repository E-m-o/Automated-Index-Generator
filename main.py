from lib.analysis.analyser import analyser
from lib.analysis.clipper import clipper
from web.crawlers import web_crawler_earthexplorer as earth
from lib.crawlers.csv_reader import csv_crawler
from web.crawlers.web_crawler_earthexplorer import *
from lib.index_calculator.index_creator import generate_indices
from lib.mosaic.mosaic_creator import mosaic_creator
from lib.mosaic.unzipper import *
from lib.atmos_correction.atmos_correction_landsat import apply_atmos_correction_landsat
from api.api import *

root = os.getcwd()
choice = None

# request = input("Enter Request Number -> ")
request = "3"
# request = 2
print(f"root = {root}")

base_path = os.path.join(root, 'Images/Request.{}'.format(request))

create_dir(base_path)


def downloader_web():
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
        upload_file(
            path_=f"{root}/Images/Test_files/test_mandala/mandlaBB.zip")

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


def processor(sat_choice=None, requested_indices=[False, False, False, True, False]):
    """
    Processes the downloaded images
    :param sat_choice: Satellite choice -- 1 -> Landsat 8, 2 -> Landsat 7, 3 -> Landsat 5, 4 -> Sentinel
    :param requested_indices: Indices requested to be processed
    """
    # DECOMPRESS IMAGES
    decompress_time = time.time()
    down_dir_dict = decompress(base_path)
    decompress_time = int(time.time() - decompress_time)

    # ATMOSPHERIC CORRECTION
    atmos_time = time.time()
    apply_atmos_correction_landsat(base_path)
    atmos_time = int(time.time() - atmos_time)

    # GENERATE INDICES
    index_time = time.time()
    generate_indices(down_dir_dict, test=False, sat_choice=sat_choice)
    index_time = int(time.time() - index_time)

    # CLIP INDICES
    clip_time = time.time()
    clipper(request=request, indice_requested=requested_indices, base_path=base_path)
    clip_time = int(time.time() - clip_time)

    # CREATE MOSAICS OF THE INDICES GENERATED
    mosaic_time = time.time()
    mosaic_creator(base_path=base_path, requested_indices=requested_indices)
    mosaic_time = int(time.time() - mosaic_time)

    # CREATE MOSAICS OF THE INDICES GENERATED
    analysis_time = time.time()
    analyser(base_path, requested_indices=requested_indices)
    analysis_time = int(time.time() - analysis_time)
    print("================================")
    print("{}{:<}\n{}{:<}\n{}{:<}\n{}{:<}\n{}{:<}".format("Decompress", "{:10.2f}".format(decompress_time / 60),
                                                          "Atmos     ", "{:10.2f}".format(atmos_time / 60),
                                                          "Index     ", "{:10.2f}".format(index_time / 60),
                                                          "Clipper   ", "{:10.2f}".format(clip_time / 60),
                                                          "Mosaic    ", "{:10.2f}".format(mosaic_time / 60),
                                                          "Analysis  ", "{:10.2f}".format(analysis_time / 60)))


def main_test():
    download_time = time.time()
    sat_choice, requested_indices = downloader(test=False, block=2027, root=root)  # for downloading from the api
    download_time = time.time() - download_time
    print("{:<15}".format("Download time"))
    print("{:<15}".format(download_time / 60))

    requested_indices = [False, False, False, True, False]
    process_time = time.time()
    processor(sat_choice=sat_choice, requested_indices=requested_indices)
    process_time = time.time() - process_time
    print("{:<15}".format("Processing time"))
    print("{:<15}".format(process_time / 60))


main_test()
