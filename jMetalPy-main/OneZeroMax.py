# The OneZeroMax problem consists of maximizing the number of zeros and the number of ones in a binary string
from jmetal.problem.multiobjective.unconstrained import OneZeroMax
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import PolynomialMutation, SBXCrossover
from jmetal.operator import BitFlipMutation, SPXCrossover
from jmetal.util.solution import get_non_dominated_solutions
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.algorithm.multiobjective.omopso import OMOPSO
import matplotlib.pyplot as plt
import numpy as np

bit_string_length = 1  # 0和1两种取值
problem = OneZeroMax(bit_string_length)
max_evaluations = 25000
algorithm = NSGAII(
    problem=problem,
    population_size=100,
    offspring_population_size=100,
    mutation=BitFlipMutation(probability=1.0 / bit_string_length),
    crossover=SPXCrossover(probability=1.0),
    termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),
)


algorithm.run()
front = get_non_dominated_solutions(algorithm.get_result())


objectives = [solution.objectives for solution in front]

x = [_[0] for _ in objectives]
y = [_[1] for _ in objectives]
plt.plot(x, y, color="black")

plt.xlabel("f1")
plt.ylabel("f2")
plt.title(problem.name())
plt.legend(["NSGAII"])
plt.show()
