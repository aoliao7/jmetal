import numpy as np
import pickle

from jmetal.problem.multiobjective.dataset import get_mapping, get_dataset
from jmetal.problem.multiobjective.model import get_model2

# from dataset import get_mapping, get_dataset
# from model import get_model2


class PSO:

    # def __init__(self):
    def origin(self):
        self.G_num = 60
        self.weight = np.ones(14)
        # alpha[g][f]
        self.alpha = [dict() for _ in range(self.G_num)]
        # number为机位号，id为映射的编号
        self.G_number, self.G_id = get_mapping()
        self.model, self.total_model = get_model2()

        (
            self.F,
            self.G,
            self.FIN,
            self.FOUT,
            self.FUS,
            self.FPS,
            self.FSS,
            self.FIN_P,
            self.FSP,
            self.FS,
            self.FI,
            self.FD,
            self.FSF,
            self.FC,
            self.FU,
            self.FV,
            self.FYJS,
            self.FYSS,
            self.FARJ,
            self.FCQ,
            self.FDH,
            self.FGH,
            self.FCI,
            self.GI,
            self.GD,
            self.GS,
            self.GC,
            self.GU,
            self.GB,
            self.GF,
            self.GT,
        ) = get_dataset(self.G_num)

    # 尝试按规则分配，不成功的航班先不分配
    def allocate(self, ids, G):
        length = len(ids)
        is_allocate = [0 for _ in range(length)]
        k = 0
        while k < length:
            flag = False
            for g in G:
                self.alpha[g][ids[k]] = 1
                k = k + 1
                # 除了唯一性约束
                if self.all_constrain() == 1:
                    k = k - 1
                    self.alpha[g][ids[k]] = 0
                else:
                    flag = True
                    is_allocate[k - 1] = 1
                    break
            if not flag:
                print(ids[k] + " 未分配" + " k =", k)
                k = k + 1

    def all_constrain(self):
        add = 0
        # add = add + self.constrain_1()
        add = add + self.constrain_2()
        add = add + self.constrain_3()
        add = add + self.constrain_4()
        # self.constrain_5()
        add = add + self.constrain_6()
        add = add + self.constrain_7()
        add = add + self.constrain_8()
        # self.constrain_9()
        add = add + self.constrain_10()
        # self.constrain_12()
        add = add + self.constrain_13()
        add = add + self.constrain_14()
        return 1 if add != 0 else 0

    def greedy_solution(self):

        total_ids = set()

        # 1.ARJ给自滑机位
        ids = []
        FIN = self.FIN.sort_values(by=["sta"], ascending=True)
        for index, f in FIN.iterrows():
            if f.loc["aircraft_type_code_icao"] == "ARJ21":
                ids.append(index)
        GS = list(self.GS)
        self.allocate(ids, GS)
        total_ids.update(ids)

        # todo 2.顺丰给16、18机位(目前数据没货运)
        # todo 3.货机(目前数据没货运)
        # 4.国外客机
        ids = []
        FIN = self.FIN.sort_values(by=["sta"], ascending=True)
        for index, f in FIN.iterrows():
            if f.loc["is_freight"] == "0" and f.loc["home_or_abroad"] == "2":
                ids.append(index)
        GI = list(self.GI)
        self.allocate(ids, GI)
        total_ids.update(ids)

        # 5.国内过站客机
        ids = []
        FIN_P = self.FIN_P.sort_values(by=["sta"], ascending=True)
        for index, f in FIN_P.iterrows():
            if f.loc["is_freight"] == "0" and f.loc["home_or_abroad"] == "1":
                ids.append(index)
        GDB = list(self.GB - self.GI)
        self.allocate(ids, GDB)
        total_ids.update(ids)

        # 6.国内停场客机
        ids = []
        FS = self.FS.sort_values(by=["sta"], ascending=True)
        for index, f in FS.iterrows():
            if f.loc["is_freight"] == "0" and f.loc["home_or_abroad"] == "1":
                ids.append(index)
        # 国内客机位
        GDU = list(self.GU - self.GI)
        self.allocate(ids, GDU)
        total_ids.update(ids)

        for index, f in FIN.iterrows():
            if index not in total_ids:
                print("未包含在内的航班：", index)

    def constrain_1(self):
        for index, f in self.FIN.iterrows():
            add = 0
            for g in self.G:
                add = add + (self.alpha[g][f.name] if f.name in self.alpha[g] else 0)
            if add != 1:
                return 1
        return 0

    def constrain_2(self):
        for index, f in self.FI.iterrows():
            for g in self.GD:
                if (self.alpha[g][f.name] if f.name in self.alpha[g] else 0) == 1:
                    return 1
        for index, f in self.FD.iterrows():
            for g in self.GI:
                if (self.alpha[g][f.name] if f.name in self.alpha[g] else 0) == 1:
                    return 1
        return 0

    def constrain_3(self):
        for index, f in self.FD.iterrows():
            for g in self.G:
                if (self.alpha[g][f.name] if f.name in self.alpha[g] else 0) == 1:
                    flag = False
                    # todo 目前是所有鼻轮都行
                    for i in range(len(self.model[g])):
                        if f["aircraft_type_code_icao"] in self.model[g][i]:
                            flag = True
                            break
                    if not flag:
                        return 1
        return 0

    def constrain_4(self):
        for g in self.G:
            for FT in self.FUS:
                add = 0
                for f in FT:
                    add = add + (self.alpha[g][f] if f in self.alpha[g] else 0)
                if add > 1:
                    return 1
        return 0

    # def constrain_5(self):
    #     for f in self.FT1:
    #         for g in self.G:
    #             if g < 311 or 321 < g:
    #                 continue
    #             if self.alpha[f[0]][g] == 1:
    #                 return 1
    #     for f in self.FT2:
    #         for g in self.G:
    #             if g < 1 or 7 < g:
    #                 continue
    #             if self.alpha[f[0]][g] == 1:
    #                 return 1
    #     return 0

    def constrain_6(self):
        for index, f in self.FIN_P.iterrows():
            for g in self.G:
                if g in self.GB:
                    continue
                if (self.alpha[g][f.name] if f.name in self.alpha[g] else 0) == 1:
                    return 1
        return 0

    def constrain_7(self):
        for g in self.G:
            # todo 相邻机位暂定
            g2 = (g + 1) % self.G_num
            for FT in self.FPS:
                add1 = 0
                add2 = 0
                for f in FT:
                    add1 = add1 + (self.alpha[g][f] if f in self.alpha[g] else 0)
                    add2 = add2 + (self.alpha[g2][f] if f in self.alpha[g2] else 0)
                if add1 * add2 != 0:
                    return 1
        return 0

    def constrain_8(self):
        for g in self.G:
            # todo 相隔机位暂定
            g2 = (g + 2) % self.G_num
            for FT in self.FSS:
                add1 = 0
                add2 = 0
                for f in FT:
                    add1 = add1 + (self.alpha[g][f] if f in self.alpha[g] else 0)
                    add2 = add2 + (self.alpha[g2][f] if f in self.alpha[g2] else 0)
                if add1 * add2 != 0:
                    return 1
        return 0

    def constrain_10(self):
        # todo 公务机数据没有
        # for f in self.FO:
        #     for g in self.G:
        #         if g in self.GC:
        #             continue
        #         if g in self.GS:
        #             continue
        #         # if g[] == 15:
        #         #     continue
        #         if self.alpha[g[0]][f[0]] == 1:
        #             return 1
        for index, f in self.FSF.iterrows():
            for g in self.G:
                if g == 16 or g == 18:
                    continue
                if (self.alpha[g][f.name] if f.name in self.alpha[g] else 0) == 1:
                    return 1
        for index, f in self.FIN.iterrows():
            g = self.G_number[332]
            if (self.alpha[g][f.name] if f.name in self.alpha[g] else 0) == 1:
                return 1
        return 0

    # def constrain_12(self):
    #     for f in self.FGS:
    #
    #     for g in self.G:
    #         g2 = self.G[(g[0]+1) % self.G_num]
    #         for FT in self.FPS:
    #             add1 = 0
    #             add2 = 0
    #             for f in FT:
    #                 add1 = add1 + self.alpha[g[0]][f[0]]
    #                 add2 = add2 + self.alpha[g2[0]][f[0]]
    #             if add1*add2 != 0:
    #                 return 1
    #     return 0

    def constrain_13(self):
        for index, f in self.FARJ.iterrows():
            for g in self.G:
                if g in self.GS:
                    continue
                if (self.alpha[g][f.name] if f.name in self.alpha[g] else 0) == 1:
                    return 1
        return 0

    def constrain_14(self):
        for index, f in self.FC.iterrows():
            for g in self.G:
                if g in self.GC:
                    continue
                if (self.alpha[g][f.name] if f.name in self.alpha[g] else 0) == 1:
                    return 1
        return 0

    def evaluate_1(self, punish):
        add = 0
        for index, f in self.F.iterrows():
            for g in self.GB:
                add = add + (self.alpha[g][f.name] if f.name in self.alpha[g] else 0)
        return add * -1 + punish

    def evaluate_2(self):
        add = 0
        for index, f in self.FU.iterrows():
            for g in self.GU:
                add = add + (self.alpha[g][f.name] if f.name in self.alpha[g] else 0)
        return add

    def evaluate_3(self):
        add = 0
        for index, f in self.FU.iterrows():
            for g in self.GB:
                add = add + (self.alpha[g][f.name] if f.name in self.alpha[g] else 0)
        return add

    def evaluate_4(self):
        add = 0
        for index, f in self.FCQ.iterrows():
            for g in self.GS:
                add = add + (self.alpha[g][f.name] if f.name in self.alpha[g] else 0)
        return add

    def evaluate_5(self):
        add = 0
        for index, f in self.FDH.iterrows():
            j = 17
            while j <= 20:
                g = self.G_number[j]
                add = add + (self.alpha[g][f.name] if f.name in self.alpha[g] else 0)
                j = j + 1
        for index, f in self.FGH.iterrows():
            j = 17
            while j <= 20:
                g = self.G_number[j]
                add = add + (self.alpha[g][f.name] if f.name in self.alpha[g] else 0)
                j = j + 1
        return add

    # def evaluate_6(self):
    #     add = 0
    #     for f in self.FT1:
    #         j = 8
    #         while j <= 14:
    #             add = add + self.alpha[self.G_number[j]][f[0]]
    #             j = j + 1
    #     return add

    def evaluate_7(self):
        add = 0
        for index, f in self.FS.iterrows():
            for g in self.GB:
                add = add + (self.alpha[g][f.name] if f.name in self.alpha[g] else 0)
        return add

    def evaluate_9(self):
        add = 0
        for index, f in self.FIN.iterrows():
            j = 8
            while j <= 26:
                g = self.G_number[j]
                add = add + (self.alpha[g][f.name] if f.name in self.alpha[g] else 0) / j
                j = j + 1
        return add

    def evaluate_10(self):
        add = 0
        for index, f in self.FV.iterrows():
            j = 316
            while j <= 320:
                g = self.G_number[j]
                add = add + (self.alpha[g][f.name] if f.name in self.alpha[g] else 0)
                j = j + 1
        return add

    def evaluate_11(self):
        add = 0
        for index, f in self.FSP.iterrows():
            for g in self.GB:
                add = add + (self.alpha[g][f.name] if f.name in self.alpha[g] else 0)
        return add

    # def evaluate_12(self):
    #     add = 0
    #     for f in self.FO:
    #         j = 15
    #         while j <= 15:
    #             add = add + 3 * self.alpha[self.G_number[j]][f[0]]
    #             j = j + 1
    #         j = 516
    #         while j <= 518:
    #             add = add + 2 * self.alpha[self.G_number[j]][f[0]]
    #             j = j + 1
    #         for g in self.GS:
    #             add = add + self.alpha[g[0]][f[0]]
    #     return add

    def evaluate_13(self):
        add = 0
        for index, f in self.FCI.iterrows():
            j = 510
            while j <= 514:
                g = self.G_number[j]
                add = add + (self.alpha[g][f.name] if f.name in self.alpha[g] else 0)
                j = j + 1
        return add

    def evaluate_14(self):
        add = 0
        for index, f in self.FYJS.iterrows():
            for g in self.GB:
                add = add + 2 * (self.alpha[g][f.name] if f.name in self.alpha[g] else 0)
        for index, f in self.FYSS.iterrows():
            for g in self.GB:
                add = add + (self.alpha[g][f.name] if f.name in self.alpha[g] else 0)
        return add

    def evaluate_total(self):
        value = [
            self.evaluate_1(),
            self.evaluate_2(),
            self.evaluate_3(),
            self.evaluate_4(),
            self.evaluate_5(),
            self.evaluate_7(),
            0,
            self.evaluate_9(),
            self.evaluate_10(),
            self.evaluate_11(),
            self.evaluate_13(),
            self.evaluate_14(),
        ]
        # value.append(self.evaluate_8()) self.evaluate_6(),  self.evaluate_12(),

        mean = np.mean(value)
        var = np.var(value)
        for i in range(len(value)):
            value[i] = (value[i] - mean) / var

        result = 0
        for i in range(len(value)):
            result = result + self.weight[i] * value[i]
        result = result + len(value) * mean
        result = result / var
        return result * 100

    def save_state(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.__dict__, f)

    def load_state(self, filename):
        with open(filename, "rb") as f:
            state = pickle.load(f)
            self.__dict__.update(state)

    def generate_dict(self):
        mydict = {}
        gd = 0
        res = [[0 for f in range(self.FIN.shape[0])] for g in range(60)]
        tmp = 0
        flag = 0
        for ii in self.alpha:
            for key in ii:
                if ii[key] == 1:
                    # print("第", gd, "组第", flag, "个")
                    res[gd][flag] = 1
                    mydict[key] = flag
                    flag = flag + 1
            gd = gd + 1
        with open("dict.txt", "w") as file:
            file.write(str(mydict))
        res2 = []
        for g in range(60):
            for f in range(self.FIN.shape[0]):
                res2.append(res[g][f])
        with open("origindata.txt", "w") as file:
            file.write(str(res2))


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
    ax.set_yticks([i * width for i in range(60)], labels=pso.G_id)

    # 设置条形数据
    for i in range(60):
        ax.broken_barh(info[i], (i * width, width - 10), facecolors=color)

    plt.show()


if __name__ == "__main__":
    pso = PSO()
    pso.origin()
    pso.save_state("pso.tkl")
    pso.greedy_solution()
    pso.generate_dict()
    res = [[0 for f in range(pso.FIN.shape[0])] for g in range(60)]
    # flag = 0
    mydict = {}
    gd = 0
    for ii in pso.alpha:
        for key in ii:
            tmp = tmp + ii[key]
            if ii[key] == 1:
                print("第", gd, "组第", flag, "个")
                res[gd][flag] = 1
                mydict[key] = flag
                flag = flag + 1
        gd = gd + 1
    print("需分配航班数：", pso.FIN.shape[0])
    print("已分配航班数：", tmp)
    print("len(dict)", len(mydict))
    # with open("dict.txt", "w") as file:
    #     file.write(str(mydict))
