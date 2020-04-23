import numpy as np
import os
import glob
import matplotlib.pyplot as plt


def crop(timemode: str, indicator: str, location: str, climate_path: str, geo_path: str):
    """
    :param timemode: 時期跟RCP
    :param indicator: 危害指標
    :param location: 地點
    :param climate_path: 氣候資料路徑
    :param geo_path : 地理資料路徑
    :return: 全部GCM的地區內平均值
    """
    input_climate_path = os.path.join(climate_path, indicator, timemode, '*.csv')
    input_geo_path = os.path.join(geo_path, f'{location}.csv')
    coord = np.genfromtxt(input_geo_path, delimiter=",")  # read selected coordinate points
    # read all csv files in the directory

    file_list = glob.glob(input_climate_path)
    # All files with csvfile should be changed
    results = []
    for filepath in file_list:

        c = np.genfromtxt(filepath, delimiter=",", encoding="utf-8")
        # calculate change rate %
        for j in range(len(c[:, 3])):
            if c[:, 3][j] == -99.9:
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


def plot():
    tmode = ["RCP8.5世紀中", "RCP8.5世紀末"]
    ind = ["少雨季(10-1月)平均日降雨量", "冬季(12-1月)平均日最低溫", "多雨季(5-9月)平均日降雨量", "春季(2-4月)平均日降雨量", "春季(2-4月)累計降雨日數"]
    loc = ["台南", "高雄", "屏東", "嘉義", "台中"]

    # read all csv
    mix = []  # 綜合所有模式、時期和地點的大型array
    file_list = []  # 讀取資料夾中所有csv檔的array
    for i in range(len(tmode)):
        for j in range(len(ind)):
            for k in range(len(loc)):
                timemode = tmode[i]
                indicator = ind[j]
                location = loc[k]
                # outputpath = ".//output//mix//" + indicator + "_" + timemode + ".csv"
                # csvfile = f".//output//{location}//{indicator}_{timemode}.csv"
                outputpath = os.path.join('.', 'output', "mix", f"{indicator}_{timemode}.csv")
                csvfile = os.path.join('.', 'output', location, f"{indicator}_{timemode}.csv")
                file_list.append(csvfile)

    # print file_list to ensure there are no duplication files in the list and the index can be used for validation
    for index, p in enumerate(file_list):
        print(index, p)
        c = np.genfromtxt(p, delimiter=",", encoding="utf-8")
        mix.append(c)
    print("==================Finish reading==================")

    for i in range(0, len(mix), len(loc)):
        filename = os.path.basename(file_list[i])
        name, ext = os.path.splitext(filename)
        calc_results = mix[i:i + len(loc)]

        # plotting
        fig1, ax1 = plt.subplots(figsize=(10, 10))
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 導入中文字
        plt.rcParams['axes.unicode_minus'] = False  # 導入中文字
        axes = plt.gca()  # 導入中文字
        axes.set_ylim([-60, 120])  # setting limits for y axis

        # plt.xlabel("地點", fontsize=30)
        plt.ylabel("變化率 %", fontsize=20)
        x = np.array([1, 2, 3, 4, 5])  # 依據不同地點數量修改，此處為5個點
        my_xticks = loc
        y = np.linspace(-60, 120, 10).astype(np.int)  # y軸極值
        ax1.set_title(name.replace("_", "  "), fontsize=30, pad=20)
        ax1.boxplot(calc_results, 1)  # remove 1 for normal boxplot
        ax1.set_xticks([])
        plt.xticks(x, my_xticks, fontsize=20)
        plt.yticks(y, y, fontsize=20)
        plt.savefig(os.path.join('.', 'output', 'mix', f'{name}.png'))
        print("=============Figure saved=============")
        # testing Seaborn package
        """
        print("=========Seaborn testing=========")
        sns.set(style="whitegrid")
        ax = sns.boxplot(data=calc_results)
        print("=========Finish Seaborn testing=========")
        """
    print("==========Plot Done==========")


if __name__ == '__main__':
    a = crop("RCP8.5世紀末", "春季(2-4月)累計降雨日數", "台中", r"C:\Users\user\Desktop\boxplot_NCDR\data\climate",
             r"C:\Users\user\Desktop\boxplot_NCDR\data\geological_data")
