import numpy as np

np.random.seed(1234124)
# 每5分钟为一个时间单位，共1440个时间单位
total_time = 1440
time_width = 50
f_num = 300
g_num = 60

# 生成航班数据

f_id = np.array([i for i in range(f_num)])
left = np.random.uniform(0, total_time - time_width, f_num).astype(int)
delta = np.fabs(np.random.normal(time_width, 1, f_num)).astype(int)
right = left + delta
flight = list(zip(f_id, left, right))
sorted_flight = sorted(flight, key=lambda x: x[1])
# print(sorted_flight)
function_called = True
# print("fid", f_id)
# print("left", left)
# print("delta", delta)
# print("right", right)
print("flight", flight)

# 生成停机位数据
stand = np.array([i for i in range(g_num)])
print("stand", stand)
GB = np.array([i for i in range(int(np.ceil(g_num / 2)))])
print("GB", GB)


def sort_by_left(e):
    return e[1]


def sort_by_right(e):
    return e[2]


tu = 1
tp = 1
ts = 1
flight.sort(key=sort_by_left)
print("dasda", flight)
FUS = []
tag = [0 for _ in range(len(flight))]
for i in range(len(flight)):
    FT = set()
    for j in range(i):
        if flight[i][1] - flight[i - j - 1][2] < tu:
            FT.add(flight[i - j - 1])
    FT.add(flight[i])
    FUS.append(FT)
for i in range(len(flight)):
    for j in range(len(flight)):
        if i == j:
            continue
        if FUS[i].issubset(FUS[j]):
            tag[i] = 1
            break

FUS = [FUS[i] for i in range(len(flight)) if tag[i] == 0]


# print("FUS", FUS)


flight.sort(key=sort_by_right)
FPS = []
tag = [0 for _ in range(len(flight))]
for i in range(len(flight)):
    FT = set()
    for j in range(i):
        if flight[i][2] - flight[i - j - 1][2] < tp:
            FT.add(flight[i - j - 1])
        else:
            break
    FT.add(flight[i])
    FPS.append(FT)
for i in range(len(flight)):
    for j in range(len(flight)):
        if i == j:
            continue
        if FPS[i].issubset(FPS[j]):
            tag[i] = 1
            break
FPS = [FPS[i] for i in range(len(flight)) if tag[i] == 0]

flight.sort(key=sort_by_right)
FSS = []
tag = [0 for _ in range(len(flight))]
for i in range(len(flight)):
    FT = set()
    for j in range(i):
        if flight[i][2] - flight[i - j - 1][2] < ts:
            FT.add(flight[i - j - 1])
    FT.add(flight[i])
    FSS.append(FT)
for i in range(len(flight)):
    for j in range(len(flight)):
        if i == j:
            continue
        if FSS[i].issubset(FSS[j]):
            tag[i] = 1
            break
FSS = [FSS[i] for i in range(len(flight)) if tag[i] == 0]
# FUS, FPS, FSS
# with open("constrain_4.txt", "a") as file:
#     file.write(str(FUS) + "\n")
#     file.write(str(FPS) + "\n")
#     file.write(str(FSS) + "\n")


# # 定义一个函数来计算在任何时刻最多同时存在的元组数量
# def max_simultaneous_presence(times):
#     # 创建一个列表来存储所有的到来和离开事件
#     events = []
#     for _, arrival, departure in times:
#         events.append((arrival, "arrival"))
#         events.append((departure, "departure"))

#     # 按时间顺序对事件进行排序
#     events.sort()

#     # 遍历事件，计算最大同时存在的元组数量
#     max_count = 0
#     current_count = 0
#     for _, event in events:
#         if event == "arrival":
#             current_count += 1
#             max_count = max(max_count, current_count)
#         else:
#             current_count -= 1

#     return max_count


# # 完整的数据列表，合并第一部分和第二部分

# k_full = [
#     (119, 3, 52),
#     (64, 4, 53),
#     (42, 8, 58),
#     (46, 13, 61),
#     (103, 22, 70),
#     (191, 28, 79),
#     (6, 42, 93),
#     (7, 50, 99),
#     (195, 50, 100),
#     (84, 53, 101),
#     (194, 73, 122),
#     (23, 76, 125),
#     (121, 92, 141),
#     (102, 94, 142),
#     (188, 96, 146),
#     (82, 103, 154),
#     (176, 112, 160),
#     (93, 132, 180),
#     (187, 135, 184),
#     (22, 139, 189),
#     (32, 142, 191),
#     (48, 146, 197),
#     (21, 155, 205),
#     (157, 168, 216),
#     (57, 169, 218),
#     (99, 173, 224),
#     (131, 182, 231),
#     (147, 185, 233),
#     (145, 196, 244),
#     (137, 234, 284),
#     (117, 250, 300),
#     (1, 257, 307),
#     (150, 265, 314),
#     (146, 275, 323),
#     (36, 278, 327),
#     (132, 281, 331),
#     (11, 289, 339),
#     (183, 290, 339),
#     (111, 293, 342),
#     (68, 295, 345),
#     (168, 317, 367),
#     (9, 326, 376),
#     (138, 330, 380),
#     (13, 334, 383),
#     (39, 334, 382),
#     (169, 334, 384),
#     (69, 350, 400),
#     (185, 354, 403),
#     (20, 355, 403),
#     (182, 358, 407),
#     (58, 365, 416),
#     (90, 367, 415),
#     (88, 371, 420),
#     (180, 381, 430),
#     (63, 388, 438),
#     (28, 399, 449),
#     (151, 409, 458),
#     (181, 427, 475),
#     (25, 438, 488),
#     (65, 438, 487),
#     (125, 441, 490),
#     (184, 443, 492),
#     (179, 445, 493),
#     (113, 454, 504),
#     (118, 454, 503),
#     (76, 456, 506),
#     (199, 458, 507),
#     (24, 462, 512),
#     (19, 467, 518),
#     (92, 467, 517),
#     (186, 471, 521),
#     (85, 476, 526),
#     (98, 486, 536),
#     (26, 490, 540),
#     (175, 491, 540),
#     (44, 493, 543),
#     (112, 500, 550),
#     (77, 504, 553),
#     (70, 519, 568),
#     (41, 524, 571),
#     (177, 528, 576),
#     (66, 537, 587),
#     (134, 555, 604),
#     (130, 558, 608),
#     (159, 558, 607),
#     (80, 592, 640),
#     (105, 602, 649),
#     (30, 605, 655),
#     (106, 616, 666),
#     (33, 619, 669),
#     (133, 633, 683),
#     (196, 633, 682),
#     (160, 647, 697),
#     (16, 662, 713),
#     (50, 664, 713),
#     (52, 667, 717),
#     (141, 680, 729),
#     (95, 682, 731),
#     (51, 699, 749),
#     (172, 711, 761),
#     (73, 716, 766),
#     (161, 729, 780),
#     (148, 731, 782),
#     (197, 732, 781),
#     (153, 735, 785),
#     (34, 737, 787),
#     (165, 737, 787),
#     (116, 738, 786),
#     (140, 742, 792),
#     (97, 774, 823),
#     (59, 775, 825),
#     (87, 787, 838),
#     (100, 788, 838),
#     (122, 790, 839),
#     (166, 797, 846),
#     (2, 809, 859),
#     (47, 819, 870),
#     (155, 820, 869),
#     (120, 823, 872),
#     (124, 827, 876),
#     (89, 839, 888),
#     (149, 839, 889),
#     (104, 844, 893),
#     (101, 848, 898),
#     (142, 854, 903),
#     (164, 867, 918),
#     (190, 869, 920),
#     (81, 871, 921),
#     (5, 878, 927),
#     (178, 906, 954),
#     (158, 910, 959),
#     (152, 934, 984),
#     (114, 938, 990),
#     (62, 940, 988),
#     (108, 949, 998),
#     (71, 954, 1005),
#     (54, 955, 1004),
#     (27, 959, 1009),
#     (139, 960, 1010),
#     (167, 963, 1011),
#     (129, 974, 1023),
#     (174, 977, 1026),
#     (83, 980, 1029),
#     (15, 992, 1041),
#     (109, 1000, 1049),
#     (60, 1005, 1055),
#     (163, 1014, 1062),
#     (10, 1025, 1076),
#     (78, 1026, 1076),
#     (107, 1030, 1079),
#     (189, 1042, 1091),
#     (154, 1069, 1118),
#     (173, 1080, 1130),
#     (75, 1094, 1145),
#     (193, 1096, 1145),
#     (17, 1109, 1159),
#     (61, 1112, 1162),
#     (127, 1114, 1163),
#     (144, 1114, 1164),
#     (192, 1116, 1166),
#     (171, 1118, 1167),
#     (143, 1125, 1175),
#     (79, 1130, 1181),
#     (37, 1132, 1182),
#     (53, 1136, 1183),
#     (49, 1142, 1192),
#     (45, 1145, 1194),
#     (198, 1147, 1196),
#     (128, 1153, 1202),
#     (0, 1162, 1211),
#     (29, 1164, 1214),
#     (135, 1170, 1220),
#     (94, 1172, 1219),
#     (67, 1174, 1225),
#     (8, 1184, 1233),
#     (86, 1198, 1246),
#     (91, 1205, 1255),
#     (38, 1215, 1264),
#     (110, 1215, 1264),
#     (126, 1220, 1269),
#     (56, 1242, 1291),
#     (170, 1244, 1294),
#     (115, 1252, 1301),
#     (12, 1262, 1313),
#     (35, 1274, 1325),
#     (18, 1281, 1330),
#     (156, 1285, 1333),
#     (96, 1308, 1356),
#     (40, 1312, 1364),
#     (31, 1319, 1367),
#     (162, 1320, 1369),
#     (74, 1323, 1373),
#     (14, 1334, 1383),
#     (72, 1339, 1388),
#     (43, 1359, 1408),
#     (136, 1371, 1420),
#     (4, 1377, 1425),
#     (3, 1381, 1429),
#     (55, 1385, 1435),
#     (123, 1388, 1439),
# ]

# print(max_simultaneous_presence(k_full))
