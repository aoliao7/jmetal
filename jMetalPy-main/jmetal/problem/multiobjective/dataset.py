from jmetal.problem.multiobjective.mapping import mapping
from jmetal.problem.multiobjective.model import get_model2

# from mapping import mapping
# from model import get_model2


from datetime import datetime

import numpy as np
import pandas as pd


# 作出冲突子集，顺便得到出港时间写进F
def make_subset(FIN, FOUT, tu, tp, ts):
    total_time = 1440

    FUS = []
    tag = [0 for _ in range(FIN.shape[0])]
    for i in range(FIN.shape[0]):
        FT = set()
        for j in range(FIN.shape[0]):
            if i == j:
                continue

            if get_minute(FIN.iloc[j]["sta"]) > get_minute(FIN.iloc[i]["sta"]):
                continue

            # todo 没有next航班代表停站
            nxt = FIN.iloc[j]["next_flight_id"]
            if nxt == "zyy14241":
                right = total_time
            else:
                right = get_minute(FOUT.loc[nxt, "std"])

            if get_minute(FIN.iloc[i]["sta"]) - right < tu:
                FT.add(FIN.iloc[j].name)
        FT.add(FIN.iloc[i].name)
        FUS.append(FT)
    for i in range(FIN.shape[0]):
        for j in range(FIN.shape[0]):
            if i == j:
                continue
            if FUS[i].issubset(FUS[j]):
                tag[i] = 1
                break
    FUS = [FUS[i] for i in range(FIN.shape[0]) if tag[i] == 0]

    FPS = []
    tag = [0 for _ in range(FIN.shape[0])]
    for i in range(FIN.shape[0]):
        FT = set()
        for j in range(FIN.shape[0]):
            if i == j:
                continue

            nxt = FIN.iloc[j]["next_flight_id"]
            if nxt == "zyy14241":
                right = total_time
            else:
                right = get_minute(FOUT.loc[nxt, "std"])

            nxt_i = FIN.iloc[i]["next_flight_id"]
            if nxt_i == "zyy14241":
                right_i = total_time
            else:
                right_i = get_minute(FOUT.loc[nxt_i, "std"])

            if right > right_i:
                continue
            if right_i - right < tp:
                FT.add(FIN.iloc[j].name)
            else:
                break
        FT.add(FIN.iloc[i].name)
        FPS.append(FT)
    for i in range(FIN.shape[0]):
        for j in range(FIN.shape[0]):
            if i == j:
                continue
            if FPS[i].issubset(FPS[j]):
                tag[i] = 1
                break
    FPS = [FPS[i] for i in range(FIN.shape[0]) if tag[i] == 0]

    FSS = []
    tag = [0 for _ in range(FIN.shape[0])]
    for i in range(FIN.shape[0]):
        FT = set()
        for j in range(FIN.shape[0]):
            if i == j:
                continue

            nxt = FIN.iloc[j]["next_flight_id"]
            if nxt == "zyy14241":
                right = total_time
            else:
                right = get_minute(FOUT.loc[nxt, "std"])

            nxt_i = FIN.iloc[i]["next_flight_id"]
            if nxt_i == "zyy14241":
                right_i = total_time
            else:
                right_i = get_minute(FOUT.loc[nxt_i, "std"])

            if right > right_i:
                continue
            if right_i - right < ts:
                FT.add(FIN.iloc[j].name)
        FT.add(FIN.iloc[i].name)
        FSS.append(FT)
    for i in range(FIN.shape[0]):
        for j in range(FIN.shape[0]):
            if i == j:
                continue
            if FSS[i].issubset(FSS[j]):
                tag[i] = 1
                break
    FSS = [FSS[i] for i in range(FIN.shape[0]) if tag[i] == 0]

    return FUS, FPS, FSS


def get_minute(str_time):
    form = "%Y%m%d%H%M%S"
    time = datetime.strptime(str_time, form)
    minute = time.hour * 60 + time.minute
    return minute


def get_FSP(FIN_P, FOUT_P):
    a = FIN_P["std"] == 1

    for index, row in FIN_P.iterrows():
        nxt = row["next_flight_id"]
        if nxt == "zyy14241":
            right = 1440
        else:
            right = get_minute(FOUT_P.loc[nxt, "std"])
        if get_minute(row["sta"]) - right < 90:
            a.loc[index] = True
        else:
            a.loc[index] = False

    return FIN_P[a]


def get_FS(FIN, FOUT):
    a = FIN["std"] == 1

    for index, row in FIN.iterrows():
        a.loc[index] = False

        if row["is_overnight"] == "0":
            continue

        nxt = row["next_flight_id"]
        if nxt == "zyy14241":
            a.loc[index] = True
            continue

        if int(FOUT.loc[nxt, "std"][8:10]) >= 6:
            a.loc[index] = True

    return FIN[a]


def make_F_subset(F):
    tu = 15
    tp = 10
    ts = 10
    # todo tk,tg

    # 进港航班 1代表进
    FIN = F[F["in_out_type"] == "1"]
    FOUT = F[F["in_out_type"] == "2"]

    # 冲突子集
    FUS, FPS, FSS = make_subset(FIN, FOUT, tu, tp, ts)

    # 过站航班
    # FP = F[((F["in_out_type"] == "2") & (F["pre_flight_id"].notna()))
    #        | ((F["in_out_type"] == "1") & (F["next_flight_id"].notna()))]

    # 进港过站航班
    FIN_P = F[(F["in_out_type"] == "1") & (F["is_overnight"] == "0")]

    # 出港过站航班
    FOUT_P = F[(F["in_out_type"] == "2") & (F["is_overnight"] == "0")]

    # 过站时间小于90min的过站航班
    FSP = get_FSP(FIN_P, FOUT_P)

    # todo 这里FS只有停场
    # 始发/停站航班,1过夜航班0不过夜航班
    FS = get_FS(FIN, FOUT)

    # 表示国际航班,国内：1国际：2
    FI = FIN[FIN["home_or_abroad"] == "2"]

    # 表示国内航班
    FD = FIN[FIN["home_or_abroad"] == "1"]

    # 表示公务航班
    # FO =

    # 表示顺丰国内航班
    FSF = FIN[FIN["airline_code_iata"] == "O3"]

    # 货机航班,is_freight是否为货运0：客运
    FC = FIN[FIN["is_freight"] == "1"]

    # 客机航班
    FU = FIN[FIN["is_freight"] == "0"]

    # VIP航班
    FV = FIN[FIN["is_vip"] == "1"]

    # 停场时间未超90min且无长时间延误的甬京快线航班
    FYJS = FSP[(FSP["dep_airport_name"] == "北京大兴") | (FSP["dep_airport_name"] == "北京首都")]

    # 停场时间未超90min且无长时间延误的甬穗快线航班
    FYSS = FSP[FSP["dep_airport_name"] == "广州"]

    # 航司T1的航班
    # FT1 = 1

    # 航司T2的航班
    # FT2 = 1

    # 机型为ARJ的航班
    FARJ = FIN[FIN["aircraft_type_code_icao"] == "ARJ"]

    # 春秋航空的航班
    FCQ = FIN[FIN["airline_code_iata"] == "9C"]

    # 东航的航班
    FDH = FIN[FIN["airline_code_iata"] == "MU"]

    # 国航的航班
    FGH = FIN[FIN["airline_code_iata"] == "CA"]

    # 货机国际航班
    FCI = FIN[(FIN["home_or_abroad"] == "2") & (FIN["is_freight"] == "1")]

    return FIN, FOUT, FUS, FPS, FSS, FIN_P, FSP, FS, FI, FD, FSF, FC, FU, FV, FYJS, FYSS, FARJ, FCQ, FDH, FGH, FCI


def make_G_subset(G):
    # 表示国际机位
    GI = {mapping(i + 305) for i in range(6)}

    # 表示国内机位
    GD = G - GI

    # 自滑机位，也就是G_(326 - 331)
    # todo 自滑机位不确定
    GS = {mapping(i + 326) for i in range(6)}

    # 货机位
    GC = {mapping(i + 510) for i in range(10)}

    # 客机位
    GU = G - GC

    # 廊桥机位
    GB = {mapping(i + 305) for i in range(17)} | {mapping(i + 1) for i in range(7)}

    # 远机位
    GF = G - GB

    # 320、321、1号特殊机位
    GT = {mapping(320), mapping(321), mapping(1)}

    return GI, GD, GS, GC, GU, GB, GF, GT


def get_dataset(g_num):
    # 读取航班数据 预处理
    path = r"C:\Users\lenovo\Documents\WeChat Files\wxid_5r8bt6p5rod122\FileStorage\File\2024-02\宁波机场20240121-20240128 第三次.xlsx"
    F = pd.read_excel(io=path, sheet_name="Sheet1", dtype=str)
    F = F.set_index("id")
    F = F[(F["is_cancelled"] == "0") & (F["is_working"] == "1")]
    # 替换空值
    F = F.fillna(value="zyy14241")

    # 删除机型不存在的航班
    model, total_model = get_model2()
    a = F["pre_flight_id"] == 1
    for i in range(F.shape[0]):
        a.iloc[i] = True
        if F.iloc[i]["aircraft_type_code_icao"] not in total_model:
            a.iloc[i] = False
    F = F[a]

    # 取0121一天的数据
    date = "20240121"
    next_day = "20240122"
    a = F["sta"] == "xxxx"
    for i in range(F.shape[0]):
        a.iloc[i] = False
        if F.iloc[i]["in_out_type"] == "1" and F.iloc[i]["sta"][0:8] == date:
            a.iloc[i] = True
        if F.iloc[i]["in_out_type"] == "2" and F.iloc[i]["std"][0:8] == date:
            a.iloc[i] = True
        # 次日出港
        if F.iloc[i]["in_out_type"] == "2" and F.iloc[i]["std"][0:8] == next_day:
            a.iloc[i] = True
    F = F[a]

    # 检查是否有next_id但是没next的航班
    a = F["pre_flight_id"] == 1
    for i in range(F.shape[0]):
        a.iloc[i] = True
        if F.iloc[i]["next_flight_id"] != "zyy14241" and F.iloc[i]["next_flight_id"] not in F.index:
            a.iloc[i] = False
    F = F[a]

    # 有两个pre_flight相同（目前只保留相互对应的数据）
    # a = F["pre_flight_id"] == 1
    # for i in range(F.shape[0]):
    #     a.iloc[i] = True
    #     if F.iloc[i]["pre_flight_id"] != "zyy14241" and F.iloc[i]["pre_flight_id"] not in F.index:
    #         a.iloc[i] = False
    #         continue
    #     if F.iloc[i]["next_flight_id"] != "zyy14241" and F.iloc[i]["next_flight_id"] not in F.index:
    #         a.iloc[i] = False
    #         continue
    # F = F[a]

    # 加上进出港时间
    F.insert(F.shape[1], "in_time", -1)
    F.insert(F.shape[1], "out_time", -1)

    FIN = F[F["in_out_type"] == "1"]
    FOUT = F[F["in_out_type"] == "2"]
    total_time = 1440
    # 得到出港时间，加到F里
    for i in range(FIN.shape[0]):
        nxt = FIN.iloc[i]["next_flight_id"]
        if nxt == "zyy14241":
            right = total_time
        else:
            right = get_minute(FOUT.loc[nxt, "std"])
        F.loc[FIN.iloc[i].name, "in_time"] = get_minute(FIN.iloc[i]["sta"])
        F.loc[FIN.iloc[i].name, "out_time"] = right

    # 停机位数据
    G = {i for i in range(g_num)}

    return F, G, *make_F_subset(F), *make_G_subset(G)


def get_mapping():
    G_number = [0 for _ in range(520)]
    G_id = [0 for _ in range(60)]

    i = 1
    while i <= 26:
        G_number[i] = mapping(i)
        G_id[mapping(i)] = i
        i = i + 1

    i = 305
    while i <= 321:
        G_number[i] = mapping(i)
        G_id[mapping(i)] = i
        i = i + 1

    i = 326
    while i <= 332:
        G_number[i] = mapping(i)
        G_id[mapping(i)] = i
        i = i + 1

    i = 510
    while i <= 519:
        G_number[i] = mapping(i)
        G_id[mapping(i)] = i
        i = i + 1

    return G_number, G_id


def main():
    # F, G, GB = generate_data(300, 60, 1440, 180)
    # make_subset(F)
    get_dataset(60)


if __name__ == "__main__":
    main()
