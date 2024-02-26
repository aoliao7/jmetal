from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import PolynomialMutation, SBXCrossover
from jmetal.operator import BitFlipMutation, SPXCrossover
from jmetal.util.solution import get_non_dominated_solutions
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.operator import RandomSolutionSelection


import matplotlib.pyplot as plt
import numpy as np

from jmetal.problem.multiobjective.zdt import ZDT1

problem = ZDT1()

max_evaluations = 25000
algorithm = NSGAII(
    problem=problem,  # 目标函数
    population_size=100,  # 种群规模
    offspring_population_size=100,  # 后代子群规模
    mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables(), distribution_index=20),  # 变异
    crossover=SBXCrossover(probability=1.0, distribution_index=20),  # 交叉
    termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),  # 终止条件
    selection=RandomSolutionSelection(),
)
print("problem.number_of_variables()", problem.number_of_variables())

algorithm.run()
front = get_non_dominated_solutions(algorithm.get_result())

for solution in front:
    print("Objective Values:", solution.objectives)

# 输出非支配解的决策变量值
for solution in front:
    print("Decision Variables:", solution.variables)

objectives = [solution.objectives for solution in front]

x = [_[0] for _ in objectives]
y = [_[1] for _ in objectives]
# print("objectives", objectives)

referenceFront = np.loadtxt("resources/reference_front/ZDT1.pf", delimiter=" ")
referenceFront = referenceFront[referenceFront[:, 0].argsort()]

plt.plot(referenceFront[:, 0], referenceFront[:, 1], color="black")
plt.scatter(x, y, color="black", marker=".")

plt.xlabel("f1")
plt.ylabel("f2")
plt.title(problem.name())
plt.legend(["Reference front", "NSGAII"])
plt.show()
