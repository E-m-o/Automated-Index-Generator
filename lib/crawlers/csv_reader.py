from pandas import DataFrame as df
from pandas import read_csv
import numpy as np

# csv = read_csv("/home/chiko/Downloads/mandlaBlock.csv")
def csv_getter(path=None, just_get=False):
    csv = read_csv(path)
    if just_get:
        data = df(csv)
        state = data["STATE"]
        district = data["DISTRICT"]
        subdist = data["SUBDIST"]
        cols = []
        for idx, (s, d, sub) in enumerate(zip(state, district, subdist)):
            # cols.append(", ".join([str(idx), s, d, sub]))
            cols.append(", ".join([s, d, sub]))
        return cols
    return csv


def csv_crawler(block=2027, clipper=False, root=str):
    
    csv = csv_getter(f'{root}/subdist_boundingBox.csv')

    data = df(csv)
    # print(data)

    columns = ["EXT_MIN_X", "EXT_MIN_Y", "EXT_MAX_X", "EXT_MAX_Y"]
    print(data["FID"]==block)
    filt = data["FID"] == block
    print(data[data["FID"]==block])
    data_ = data[filt]
    print(data_)

    arr = data_.dropna()[columns]
    # print(arr)
    temp = []
    coords = []
    for col in columns:
        # print(arr[col])
        temp.append(arr[col].tolist()[0])
    # print(temp)


    if clipper:
        return temp

    temp = np.array(temp)

    longs = list(temp[[0, 2]])
    lats = list(temp[[3, 1]])
    for long_ in longs:
        for lat in lats:
            coords.append([lat, long_])
    print(coords)

    temp_ = coords[2]
    coords[2] = coords[3]
    coords[3] = temp_
    return coords


# import web_crawler_earthexplorer
#
# coords = csv_crawler("Mandla")
# print(coords)
# driver = web_crawler_earthexplorer.make_driver()
# web_crawler_earthexplorer.access_explorer()
# web_crawler_earthexplorer.add_coordinates(coords)
