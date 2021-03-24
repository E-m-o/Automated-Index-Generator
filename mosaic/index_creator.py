import os
import glob
from index_calculator import index_calculator_landsat, index_calculator_sentinel

# TODO: add path parameter to help save with better filenames


def crawler(subdir_list=None, root=str, landsat_list_len=3, sentinel_list_len=3, test=False):
    """
    Creates all the indices for a sub-folder in subdir_list in which relevant bands are found

    :param subdir_list: list of strings with paths
    :param root: root directory
    :type root: string
    :type landsat_list_len: integer
    :type sentinel_list_len: integer
    :param test: bool for test case
    """
    if subdir_list is None:
        print('Invalid paths')
        print('Terminating')
        exit()

    for sub in subdir_list:
        caps_tif_list = glob.glob(sub+'/*.TIF')
        if len(caps_tif_list) >= landsat_list_len:
            os.chdir(root+sub[1:])
            current_dir = os.getcwd()
            print('Landsat images found in .{}'.format(current_dir))
            if not test:
                print('Calculating Indices.....')
                index_calculator_landsat.execute_landsat()
        os.chdir(root)

    for sub in subdir_list:
        tif_list = glob.glob(sub + '/*.tif')
        if len(tif_list) >= landsat_list_len:
            os.chdir(root + sub[1:])
            print('Landsat images found in .{}'.format(os.getcwd()))
            if not test:
                print('Calculating Indices.....')
                index_calculator_landsat.execute_landsat()
        os.chdir(root)

    for sub in subdir_list:
        caps_jp2_list = glob.glob(sub + '/*.JP2')
        if len(caps_jp2_list) >= sentinel_list_len:
            os.chdir(root + sub[1:])
            print('Sentinel images found in .{}'.format(os.getcwd()))
            if not test:
                print('Calculating Indices.....')
                index_calculator_sentinel.execute_sentinel()
        os.chdir(root)

    for sub in subdir_list:
        jp2_list = glob.glob(sub + '/*.jp2')
        if len(jp2_list) >= sentinel_list_len:
            os.chdir(root + sub[1:])
            print('Sentinel images found in .{}'.format(os.getcwd()))
            if not test:
                print('Calculating Indices.....')
                index_calculator_sentinel.execute_sentinel()
        os.chdir(root)
