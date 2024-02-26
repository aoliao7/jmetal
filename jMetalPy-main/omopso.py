from jmetal.algorithm.multiobjective.omopso import OMOPSO
from jmetal.operator import UniformMutation
from jmetal.operator.mutation import NonUniformMutation
from jmetal.problem import ZDT1
from jmetal.util.archive import CrowdingDistanceArchive
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.problem.multiobjective.unconstrained import OneZeroMax
import matplotlib.pyplot as plt
import numpy as np
import time
import ast
from jmetal.problem.multiobjective.pso import PSO


def testbridge(res):
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


k = 0
while k < 1:
    problem = ZDT1()
    mutation_probability = 1.0 / problem.number_of_variables()  # 变异概率，跳出局部最优解，增加多样性
    max_evaluations = 900  # 最大迭代次数
    swarm_size = 300  # 粒子群大小

    algorithm = OMOPSO(
        problem=problem,
        swarm_size=swarm_size,
        epsilon=0.0075,  # 这个解在每个目标上至少需要与归档中现有的解有0.0075的差异才能被认为是独特的
        # uniform_mutation=UniformMutation(probability=mutation_probability, perturbation=0.5),
        # # 每个粒子的每个决策变量有 mutation_probability 的概率发生变异，变异的幅度由 perturbation 参数控制，这里设置为0.5。
        # non_uniform_mutation=NonUniformMutation(
        #     mutation_probability, perturbation=0.5, max_iterations=int(max_evaluations / swarm_size)
        # ),
        leaders=CrowdingDistanceArchive(400),
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),  # 算法停止条件
    )

    start_time = time.time()
    algorithm.run()
    end_time = time.time()
    front = algorithm.get_result()
    leader = algorithm.get_leaders()
    one = algorithm.get_ones()
    zero = algorithm.get_zeros()
    evaluation = algorithm.get_evalutions()
    change = algorithm.get_changes()
    change_list = algorithm.get_change_list()
    ct = 0
    for index, solution in enumerate(front):
        print("constraints:", solution.constraints)
        print("Objective Values:", solution.objectives)
        filename = f"11list{ct+1}.txt"
        with open(filename, "w") as file:
            file.write(str(solution.variables) + "\n")
        if index == len(front) - 1:
            with open("finallist.txt", "w") as file:
                file.write(str(solution.variables) + "\n")
        testbridge(solution.variables)
        ct += 1
    # print("solution", solution)
    # for solution in leader:
    #     if solution.objectives[0] not in unique_solutions:
    #         unique_solutions.add(solution.objectives[0])
    #         print("constraints_leader222:", solution.constraints)
    #         print("Objective Values_leader222:", solution.objectives)
    #         # matrix = np.array(solution.variables).reshape(60, 144)
    #         # flights_per_slot = np.sum(matrix, axis=1)
    #         # print("每个机位停飞机的数量:", flights_per_slot)
    #         testbridge(solution.variables)
    #         with open("leaderlist.txt", "w") as file:
    #             file.write(str(solution.variables) + "\n")
    #     else:
    #         continue
    k += 1
print("time", end_time - start_time)
