import os
import numpy as np
from scipy.io import savemat


def process(dir_path, save_dir):
    dirs = os.listdir(dir_path)
    for dir in dirs:
        if dir != "readMe.txt":
            sub_num = subject_dict[dir]
            files_path = os.path.join(dir_path, dir)
            files = os.listdir(files_path)
            for file in files:
                # print(file)
                # 活动标签
                if file.__contains__("电梯上"):
                    act_num = 3
                elif file.__contains__("电梯下"):
                    act_num = 4
                elif file.__contains__("楼梯上") or file.__contains__("上楼梯"):
                    act_num = 5
                elif file.__contains__("楼梯下") or file.__contains__("下楼梯"):
                    act_num = 6
                elif file.__contains__("骑"):
                    act_num = 7
                file_path = os.path.join(files_path, file)
                data = []
                for index, line in enumerate(open(file_path, mode='r')):
                    if index % 12 in [4, 5, 6]:
                        data.append(int(line))

                # 处理文件最后三轴加速度未写全的情况
                real_num = len(data) // 3
                data = data[:real_num * 3]

                # 整理数据格式，sample_num * 250 * 3
                signal = np.array(data, dtype=int).reshape(-1, 3)
                sample_num = signal.shape[0] // 250  # 采样率125Hz，两秒一分片，一共可得到的分片数
                signal = signal[:sample_num * 250, :].reshape(sample_num, 250, 3)
                save_name = "sub" + str(sub_num) + "Act" + str(act_num) + ".mat"
                save_path = os.path.join(save_dir, save_name)
                savemat(save_path, {"data": signal})
                print(save_name + " saved!")


if __name__ == "__main__":
    # 用户编号字典
    subject_dict = {"hyk": 1, "lt": 2, "xdj": 3, "xgc": 4, "zq": 5}

    dir_path = "./11.6"
    save_dir = "./11.6-result"
    process(dir_path, save_dir)
