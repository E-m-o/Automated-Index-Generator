from rasterio import open as raster_open
# from rasterio.plot import show
import glob
import os


def apply_atmos_correction_landsat(request=None):
    """Applies atmospheric correction to the read images
    
    Keyword Arguments:
        request {str} -- request number (default: {None})
    """
    path = os.path.join(os.getcwd(), 'Images/Request.{}'.format(request))
    os.chdir(path)
    tif_list = glob.glob("./**/*.TIF", recursive=True)
    tif_dict = {}
    for tif in tif_list:
        tif_split = "/".join(tif.split("/")[:3])
        if tif_split not in tif_dict:
            tif_dict[tif_split] = [tif]
        else:
            tif_dict[tif_split].append(tif)

    for tif_dir in tif_dict:
        print(tif_dir)
        os.chdir(tif_dir)
        tif_dict[tif_dir].sort()

        meta_file = glob.glob("*.txt")[0]

        reflectance_mult_band = []
        reflectance_add_band = []
        sun_elevation = None

        with open(meta_file, "r") as file:
            for txt in file:
                # print(txt, end="")
                if "REFLECTANCE_ADD_BAND" in txt:
                    reflectance_add_band.append(txt)
                if "REFLECTANCE_MULT_BAND" in txt:
                    reflectance_mult_band.append(txt)
                if "SUN_ELEVATION" in txt:
                    sun_elevation = txt

        # for (mult, add) in zip(radiance_mult_band, radiance_add_band):
        #     print(mult.split('='), add, end="")
        #
        # for (mult, add) in zip(reflectance_mult_band, reflectance_add_band):
        #     print(mult, add, end="")
        #
        # print(sun_elevation)

        band_dict = {
            "1": None,
            "2": None,
            "3": None,
            "4": None,
            "5": None,
            "6": None,
            "7": None,
            "8": None,
            "9": None
        }
        for tif in tif_dict[tif_dir]:
            tif_band = tif.split('.')[1][-3:]
            for band in band_dict:
                if "_B{}".format(band) in tif_band:
                    # print(tif.split('.')[1][-3:])
                    band_dict[band] = tif.split("/")[-1]

        for (band, mult, add) in zip(band_dict, reflectance_mult_band, reflectance_add_band):
            fn = band_dict[band]
            mult = float(mult.split("=")[-1].strip())
            add = float(add.split("=")[-1].strip())
            print(band, mult, add)

            with raster_open(fn) as file:
                temp = file.read(1).astype("float64")
                meta = {
                    'width': file.width,
                    'height': file.height,
                    'crs': file.crs,
                    'transform': file.transform
                }
                # show(temp)
                # print(file.transform)
            temp = mult * temp + add
            # show(temp)

            temp_image = raster_open(fn, 'w', driver='GTiff',
                                     width=meta['width'], height=meta['height'],
                                     count=1,
                                     crs=meta['crs'],
                                     transform=meta['transform'],
                                     dtype='float64')
            temp_image.write(temp, 1)
            temp_image.close()
        os.chdir(path)


# apply_atmos_correction_landsat("0")
