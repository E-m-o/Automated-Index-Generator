import glob
import os


def decompress(sat_choice=str, path=str):
    """
    Unzips the *tar.gz files to folders with their respective names
    :return: Download directory list
    :param sat_choice: Satellite choice -> 1. Landsat | 2. Sentinel
    :type sat_choice: str
    :param path: Path of root directory
    :type path: str
    """
    print("===================")
    print("Decompressing files")
    # path = '/home/emo/Storage/Projects/Raster_Image_Calculator/Images/Request.0'
    os.chdir(path=path)
    root = os.getcwd()
    # print(root)
    name_list = []
    down_dir = []
    down_dir_dict = {}
    if sat_choice == '1':
        tar_list = glob.glob(os.path.join(root, '**/*.tar.gz'), recursive=True)
        for (i, tar) in enumerate(tar_list):
            tar_split = tar.split('/')
            split = '/'.join(tar_split[:-1])
            name = tar_split[-1].split('.')[0]
            name_list.append(name)
            down_dir.append(split)
            try:
                os.chdir(down_dir[i])
                os.mkdir(name_list[i])
                os.chdir(root)
            except FileExistsError:
                pass
        for (i, tar) in enumerate(tar_list):
            os.system('tar -xzf {} -C {}'.format(tar, os.path.join(down_dir[i], name_list[i])))

    elif sat_choice == '2':
        zip_list = glob.glob(os.path.join(root, '**/*.zip'), recursive=True)
        for (i, zip_) in enumerate(zip_list):
            zip_split = zip_.split('/')
            name = zip_split[-1].split('.')[0]
            name_list.append(name)
            split = '/'.join(zip_split[:-1])
            down_dir.append(split)
            try:
                os.chdir(down_dir[i])
                os.mkdir(name_list[i])
                os.chdir(root)
            except FileExistsError:
                pass
        for (i, zip_) in enumerate(zip_list):
            os.system('unzip -qo {} -d {}'.format(zip_, os.path.join(down_dir[i], name_list[i])))

    for d_dir, name in zip(down_dir, name_list):
        down_dir_dict[name] = d_dir

    print("Finished decompression")
    # print(down_dir_dict)
    os.chdir(root)
    return down_dir_dict


# d, n = un_zipper(sat_choice='1', path='/home/emo/Storage/Projects/Raster_Image_Calculator/Images')
# print(d)
