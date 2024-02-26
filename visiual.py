import numpy as np
import matplotlib.pyplot as plt
import random

# 假设 data_list 是您的18000个数字组成的列表
with open("origindata.txt", "r") as file:
    # 从文件中读取文本并将其转换为列表
    input_list = eval(file.read())

    # 创建一个新列表并将读取的列表赋值给它
    data_list = input_list[:]
with open("origindata2.txt", "r") as file:
    # 从文件中读取文本并将其转换为列表
    input_list = eval(file.read())

    # 创建一个新列表并将读取的列表赋值给它
    data_list2 = input_list[:]
if data_list == data_list2:
    print("yes")
data2 = np.array(data_list)
objects = data2.reshape(-1, 144)
# 计算每个对象中的变量之和
sums = objects.sum(axis=1)
max_sum = sums.max()
# 找出所有等于最小和的对象的索引
# max_indices = np.where(sums >= 9)[0]
# a = random.choice(max_indices)
# print(max_indices)
# print("a:", a)
print("ab:", sums)
# random_one = random.choice(
#     [num for num in range(len(objects[a])) if objects[a][num] == 1]
# )

# print(random_one)
# data = numpy.array(swarm[index].variables)
# objects = data.reshape(-1, 300)
# # 计算每个对象中的变量之和
# sums = objects.sum(axis=1)
# max_sum = sums.max()
# # 找出所有等于最小和的对象的索引
# max_indices = numpy.where(sums >= 9)[0]
# most_g = random.choice(max_indices)
# random_one = random.choice([num for num in range(len(objects[most_g])) if objects[most_g][num] == 1])
# # 将列表转换为60x300的NumPy数组
# matrix = np.array(data_list).reshape(60, 300)

# # 使用Matplotlib绘制热图
# plt.figure(figsize=(20, 10))  # 设置图像大小
# plt.imshow(matrix, cmap="hot", interpolation="nearest", aspect="auto")
# plt.colorbar()  # 显示颜色条
# plt.title("机位与航班分布热图")
# plt.xlabel("航班")
# plt.ylabel("机位")
# plt.show()
# flights_per_slot = np.sum(matrix, axis=1)
# print("每个机位停飞机的数量:", flights_per_slot)

# # 计算每个航班被停的数量
# slots_per_flight = np.sum(matrix, axis=0)
# print("每个航班被停的机位数量:", slots_per_flight)
# 打开文件
