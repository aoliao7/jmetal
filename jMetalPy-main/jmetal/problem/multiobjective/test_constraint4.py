from pso import PSO
import numpy as np


import globalmanger as gm

from test2 import test


def show_stand(info, color, title):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(18, 18))
    plt.rcParams["font.sans-serif"] = ["kaiti"]

    width = 30
    # 设置xy轴的范围
    ax.set_ylim(0, 60 * width)
    ax.set_xlim(0, 1440)

    plt.title(title)  # 图的标题
    plt.xlabel("时间（分钟）")  # 横轴标签
    plt.ylabel("机位号")  # 纵轴标签

    # 更改y轴记号标签
    ax.set_yticks([i * width for i in range(60)], labels=p.G_id)

    # 设置条形数据
    for i in range(60):
        ax.broken_barh(info[i], (i * width, width - 10), facecolors=color)

    plt.show()


res = []
with open("origindata.txt", "r") as file:
    # 从文件中读取文本并将其转换为列表
    input_list = eval(file.read())

    # 创建一个新列表并将读取的列表赋值给它
    res = input_list[:]
matrix = np.array(res).reshape(60, 144)
flights_per_slot = np.sum(matrix, axis=1)
print("每个机位停飞机的数量:", flights_per_slot)
# for i, flights in enumerate(matrix):
#     print(f"机位{i}停的飞机编号:", [j for j, val in enumerate(flights) if val == 1])
with open("dict.txt", "r") as file:
    content = file.read()
    my_dict = eval(content)
items_list = list(my_dict.items())
p = PSO()
p.load_state(r"D:\JeMetalpy\pso.tkl")
p.weight[0] = 100
# print(os.getcwd())

ct = 0
for d in p.alpha:
    for j in range(144):
        if res[ct] == 1:
            key = items_list[j][0]
            value = items_list[j][1]
            d[key] = 1
        ct += 1
punish = (
    p.constrain_1()
    + p.constrain_2()
    + p.constrain_3()
    + p.constrain_4()
    + p.constrain_6()
    + p.constrain_7()
    + p.constrain_8()
    + p.constrain_10()
    + p.constrain_13()
    + p.constrain_14()
)
print(punish)
print(p.evaluate_1(punish))


near_num = 0
far_num = 0
data = [[] for i in range(60)]
for ii in range(60):
    for key in p.alpha[ii]:
        if p.alpha[ii][key] == 1:
            data[ii].append(
                (
                    p.F.loc[key, "in_time"],
                    p.F.loc[key, "out_time"] - p.F.loc[key, "in_time"],
                )
            )
            if ii in p.GB:
                near_num = near_num + 1
            else:
                far_num = far_num + 1
    data[ii].sort(key=lambda x: x[0])
print(
    "靠桥率：",
    near_num / (near_num + far_num),
    "近机位数：",
    near_num,
    "远机位数：",
    far_num,
)

near_num = 0
far_num = 0
data2: list = [[] for i in range(60)]
for indexx, ff in p.FIN.iterrows():
    if ff.loc["arr_stand"] == "zyy14241":
        continue
    idd = p.G_number[int(ff.loc["arr_stand"])]
    data2[idd].append((ff.loc["in_time"], ff.loc["out_time"] - ff.loc["in_time"]))
    if idd in p.GB:
        near_num = near_num + 1
    else:
        far_num = far_num + 1
print(
    "原靠桥率：",
    near_num / (near_num + far_num),
    "近机位数：",
    near_num,
    "远机位数：",
    far_num,
)

# show_stand(data, "tab:blue", "算法分配结果")
# show_stand(data2, "tab:red", "原始分配结果")
