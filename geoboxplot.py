import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import tqdm


def crop(time_mode: str, indicator: str, location: str, climate_path: str, geo_path: str):
    """
    :param time_mode: 時期跟RCP
    :param indicator: 危害指標
    :param location: 地點
    :param climate_path: 氣候資料路徑
    :param geo_path : 地理資料路徑
    :return: 全部GCM的地區內平均值
    """
    input_climate_path = os.path.join(climate_path, indicator, time_mode, '*.csv')
    input_geo_path = os.path.join(geo_path, f'{location}.csv')
    coord = np.genfromtxt(input_geo_path, delimiter=",")  # read selected coordinate points
    # read all csv files in the directory

    file_list = glob.glob(input_climate_path)
    # All files with csvfile should be changed
    results = []
    for filepath in file_list:
        # print(filepath)
        c = np.genfromtxt(filepath, delimiter=",", encoding="utf-8")
        # calculate change rate %
        for j in range(len(c[:, 3])):
            if c[:, 3][j] == -99.9:
                c[:, 5][j] = -99.9
            elif c[:, 2][j] == 0:
                c[:, 5][j] = -99.9
            else:
                c[:, 5][j] = 100 * (c[:, 4][j] / c[:, 2][j])
        # print("Done: Calculate changing rate %")
        selected = {tuple(x[:2]): x[2:] for x in c}
        output = []
        for x in coord:
            if tuple(x) in selected:
                jj = np.concatenate((x, selected[tuple(x)]), axis=None)
                output.append(jj)
        average = np.average(np.array(output)[:, 5], axis=0)
        # print("The result is: " + str(average))
        results.append(average)
        # print("Finish one file: " + filepath)
    return results


def plot(time_mode_list: list, indicator_list: list, location_list: list, climate_path: str, geo_path: str):
    """

    :param time_mode_list: 時期列表
    :param indicator_list: 危害指標列表
    :param location_list: 地點列表
    :param climate_path: 氣候資料路徑
    :param geo_path: 地理資料路徑
    :return: 沒有
    """

    # read all csv

    file_list = []  # 讀取資料夾中所有csv檔的array
    crop_results = []
    for i in tqdm.tqdm(range(len(time_mode_list))):
        for j in range(len(indicator_list)):
            for k in range(len(location_list)):
                time_mode = time_mode_list[i]
                indicator = indicator_list[j]
                location = location_list[k]

                crop_result = crop(time_mode, indicator, location, climate_path, geo_path)
                crop_results.append(crop_result)
                file_list.append(f"{indicator}_{time_mode}")
    # print file_list to ensure there are no duplication files in the list and the index can be used for validation

    for i in range(0, len(crop_results), len(location_list)):
        filename = os.path.basename(file_list[i])

        calc_results = crop_results[i:i + len(location_list)]

        # plotting
        fig1, ax1 = plt.subplots(figsize=(10, 10))
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 導入中文字
        plt.rcParams['axes.unicode_minus'] = False  # 導入中文字
        axes = plt.gca()  # 導入中文字
        axes.set_ylim([-60, 120])  # setting limits for y axis

        # plt.xlabel("地點", fontsize=30)
        plt.ylabel("變化率 %", fontsize=20)
        x = np.array([1, 2, 3, 4, 5])  # 依據不同地點數量修改，此處為5個點
        y = np.linspace(-60, 120, 10).astype(np.int)  # y軸極值
        ax1.set_title(filename.replace("_", "  "), fontsize=30, pad=20)
        ax1.boxplot(calc_results)  # remove 1 for normal boxplot
        ax1.set_xticks([])
        plt.xticks(x, location_list, fontsize=20)
        plt.yticks(y, y, fontsize=20)
        plt.savefig(os.path.join('.', 'output', 'mix', f'{filename}.png'))


if __name__ == '__main__':
    tmode = ["RCP8.5世紀中", "RCP8.5世紀末"]
    ind = ["少雨季(10-1月)平均日降雨量", "冬季(12-1月)平均日最低溫", "多雨季(5-9月)平均日降雨量", "春季(2-4月)平均日降雨量", "春季(2-4月)累計降雨日數"]
    loc = ["台南", "高雄", "屏東", "嘉義", "台中"]
    a = plot(tmode, ind, loc, r"C:\Users\user\Desktop\boxplot_NCDR\data\climate",
             r"C:\Users\user\Desktop\boxplot_NCDR\data\geological_data")
