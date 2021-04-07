from pandas import DataFrame as df
from pandas import read_csv
import numpy as np

csv = read_csv("/home/emo/Downloads/mandlaBlock.csv")


def csv_crawler(block=None, test=False):
    if test:
        block = "Mandla"
    data = df(csv)

    data_ = data

    columns = ["EXT_MIN_X", "EXT_MIN_Y", "EXT_MAX_X", "EXT_MAX_Y"]

    filter_ = data["BLK_NAME"] == block
    data_.where(filter_, inplace=True)

    arr = data_.dropna()[columns]
    temp = []
    coords = []
    for col in columns:
        temp.append(arr[col].tolist()[0])
    # print(temp)

    temp = np.array(temp)

    longs = list(temp[[0, 2]])
    lats = list(temp[[3, 1]])
    for long_ in longs:
        for lat in lats:
            coords.append([lat, long_])
    # print(coords)

    temp_ = coords[2]
    coords[2] = coords[3]
    coords[3] = temp_
    return coords


# import web_crawler_earthexplorer
#
# coords = csv_crawler("Mandla")
# driver = web_crawler_earthexplorer.make_driver()
# web_crawler_earthexplorer.access_explorer()
# web_crawler_earthexplorer.add_coordinates(coords)
