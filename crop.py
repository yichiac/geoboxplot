import numpy as np
import os
import csv


# shp = "./data/geological_data/Tainan/tainan.shp"

outputpath = ".//output//" + location + "//" + indicator + "_" + timemode + ".csv"
csvfile = ".//data//climate//" + indicator + "//" + timemode + "//"


def crop(timemode: str, indicator: str, location: str, climate_path: str):
    """
    :param timemode: 時期跟RCP
    :param indicator: 危害指標
    :param location: 地點
    :param climate_path: 氣候資料路徑
    :return: 全部GCM的地區內平均值
    """
    input_climate_path = os.path.join(climate_path, )
    input_geo_path = None
    coord = np.genfromtxt(input_geo_path, delimiter=",")  # read selected coordinate points
    # read all csv files in the directory
    file_list = []
    for file in os.listdir(csvfile):
        if file.endswith(".csv"):
            file_list.append(file)

    # All files with csvfile should be changed
    results = []
    for i in file_list:
        filepath = csvfile + i
        c = np.genfromtxt(filepath, delimiter=",", encoding="utf-8")
        # calculate change rate %
        for j in range(len(c[:, 3])):
            if c[:, 3][j] == -99.9:
                c[:, 5][j] = -99.9
            else:
                c[:, 5][j] = 100 * (c[:, 4][j] / c[:, 2][j])
        print("Done: Calculate changing rate %")
        selected = {tuple(x[:2]): x[2:] for x in c}
        output = []
        for x in coord:
            if tuple(x) in selected:
                jj = np.concatenate((x, selected[tuple(x)]), axis=None)
                output.append(jj)
        average = np.average(np.array(output)[:, 5], axis=0)
        print("The result is: " + str(average))
        results.append(average)
        print("Finish one file: " + filepath)
    with open(outputpath, "w", newline="") as myfile:
        wr = csv.writer(myfile, delimiter=",")
        wr.writerow(results)
    return results


if __name__ == "__main__":
    a = crop("RCP8.5世紀末", "春季(2-4月)累計降雨日數", "台中")
