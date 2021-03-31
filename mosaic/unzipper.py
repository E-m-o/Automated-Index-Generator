import glob
import os


def decompress(path=str):
    """
    Unzips the *tar.gz files to folders with their respective names
    :return: Download directory list
    # :param sat_choice: Satellite choice -> 1. Landsat | 2. Sentinel
    # :type sat_choice: str
    :param path: Path of root directory
    :type path: str
    """
    print("===================")
    print("Decompressing files")

    os.chdir(path=path)
    root = os.getcwd()

    name_list_tar = []
    down_dir_tar = []
    name_list_zip = []
    down_dir_zip = []
    down_dir_dict = {}
    tar_list = glob.glob(os.path.join(root, '**/*.tar.gz'), recursive=True)
    paths = []
    if tar_list:
        for (i, tar) in enumerate(tar_list):
            tar_split = tar.split('/')
            split = '/'.join(tar_split[:-1])
            name = tar_split[-1].split('.')[0]
            name_list_tar.append(name)
            down_dir_tar.append(split)
            try:
                paths.append(os.path.join(split, name))
                os.mkdir(paths[i])
            except FileExistsError:
                pass
        for (i, tar) in enumerate(tar_list):
            os.system('tar -xzf {} -C {}'.format(tar, paths[i]))

    zip_list = glob.glob(os.path.join(root, '**/*.zip'), recursive=True)
    if zip_list:
        for (i, zip_) in enumerate(zip_list, len(tar_list)):
            zip_split = zip_.split('/')
            split = '/'.join(zip_split[:-1])
            name = zip_split[-1].split('.')[0]
            name_list_zip.append(name)
            down_dir_zip.append(split)
            try:
                paths.append(os.path.join(split, name))
                os.mkdir(paths[i])
            except FileExistsError:
                pass
        for (i, zip_) in enumerate(zip_list, len(tar_list)):
            os.system('unzip -qo {} -d {}'.format(zip_, paths[i]))

    for d_dir, name in zip(down_dir_tar, name_list_tar):
        down_dir_dict[name] = d_dir

    for d_dir, name in zip(down_dir_zip, name_list_zip):
        down_dir_dict[name] = d_dir

    print("Finished decompression")

    for key, value in down_dir_dict.items():
        print(key, value)
    os.chdir(root)
    return down_dir_dict
