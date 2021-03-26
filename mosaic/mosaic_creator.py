import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os
import unzipper


def mosaic_creator(down_dir_dict=dict, test=False):

    bands = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '8A']

    start_files = {}
    end_files = {}
    base = os.getcwd()
    # noinspection PyArgumentList
    for (name, d_dir) in down_dir_dict.items():
        path = os.path.join(d_dir, name)
        if 'Start_date' in d_dir:
            start_file = glob.glob(os.path.join(path, '**/*.TIF'), recursive=True)
            start_file.sort()
            if len(start_file) < 10:
                start_file = glob.glob(os.path.join(path, '**/*.jp2'), recursive=True)
            start_files[path] = start_file
        if 'End_date' in d_dir:
            end_file = glob.glob(os.path.join(path, '**/*.TIF'), recursive=True)
            end_file.sort()
            if len(end_file) < 10:
                end_file = glob.glob(os.path.join(path, '**/*.jp2'), recursive=True)
            end_files[path] = end_file

    # print(start_files)
    # print(end_files)
    files_list = {'start': start_files,
                  'end': end_files}

    for pos, files in files_list.items():
        band_dict = {band: [] for band in bands}
        for band in bands:
            for key, value in files.items():
                for val in value:
                    if 'B{}.TIF'.format(band) in val:
                        band_dict[band].append(val)
                    if 'B{}.jp2'.format(band) in val:
                        band_dict[band].append(val)
                    elif 'B0{}.jp2'.format(band) in val:
                        band_dict[band].append(val)

            try:
                src_files_to_mosaic = []
                for file in band_dict[band]:
                    src = rasterio.open(file)
                    src_files_to_mosaic.append(src)

                mosaic, out_trans = merge(src_files_to_mosaic)
                # show(mosaic, cmap='gray')

                out_meta = src_files_to_mosaic[0].meta.copy()
                out_meta.update({"driver": "GTiff",
                                 "height": mosaic.shape[1],
                                 "width": mosaic.shape[2],
                                 "transform": out_trans
                                 }
                                )
                # noinspection PyUnboundLocalVariable
                os.chdir('/'.join(key.split('/')[:-1]))
                # print(os.getcwd())
                with rasterio.open('{}_mosaic{}.tiff'.format(pos, band), "w", **out_meta) as destination:
                    destination.write(mosaic)
                os.chdir(base)
            except IndexError:
                pass
        # print(band_dict)


# d = unzipper.decompress(sat_choice='1', path='/home/emo/Storage/Projects/Raster_Image_Calculator/Images')
# # print(os.getcwd())
# mosaic_creator(d)
