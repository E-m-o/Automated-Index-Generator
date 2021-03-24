import glob
import os

os.chdir('/home/emo/Storage/Projects/Raster_Image_Calculator/Test_files/Temp/Start_date')
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