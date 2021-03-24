import glob
import os


def un_zipper(path=str):
    """
    Unzips the *tar.gz files to folders with their respective names
    :param path: Path of root directory
    :type path: str
    """
    os.chdir(path=path)
    root = os.getcwd()
    print(root)

    list_ = glob.glob('*.tar.gz')
    # print(list_)
    name = []
    for (i, tar) in enumerate(list_):
        name.append(tar.split('.')[0])
        try:
            os.mkdir(os.path.join(os.getcwd(), name[i]))
        except FileExistsError:
            pass

    for (i, tar) in enumerate(list_):
        print(name[i])
        os.system('tar -xzvf {} -C {}'.format(tar, os.path.join(os.getcwd(), name[i])))