import numpy as np

with open("list1.txt", "r") as file:
    input_list = eval(file.read())
    origindata = input_list[:]
with open("list2.txt", "r") as file:
    input_list = eval(file.read())
    res = input_list[:]
ct = 0

change_flight = []
for i in range(int(len(res) / 60)):
    for j in range(60):
        if (
            res[j * (int(len(res) / 60)) + i]
            != origindata[j * (int(len(res) / 60)) + i]
        ):
            ct += 1
            change_flight.append(i)
            break
print("改变飞机个数:", ct)
print("改变飞机个的编号:", change_flight)
