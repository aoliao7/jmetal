from math import cos, pi, pow, sin, sqrt, exp
from copy import copy
from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
from jmetal.problem.multiobjective.pso import PSO
import os
import numpy as np

"""
.. module:: ZDT
   :platform: Unix, Windows
   :synopsis: ZDT problem family of multi-objective problems.

.. moduleauthor:: Antonio J. Nebro <antonio@lcc.uma.es>
"""


class ZDT1(FloatProblem):
    """Problem ZDT1.

    .. note:: Bi-objective unconstrained problem. The default number of variables is 30.
    .. note:: Continuous problem having a convex Pareto front
    """

    def __init__(self, number_of_variables: int = 8640):
        """:param number_of_variables: Number of decision variables of the problem."""
        super(ZDT1, self).__init__()

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ["x"]
        self.lower_bound = number_of_variables * [0]
        self.upper_bound = number_of_variables * [1]

    def number_of_objectives(self) -> int:
        return 1

    def number_of_variables(self) -> int:
        return len(self.lower_bound)

    def number_of_constraints(self) -> int:
        return 10

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        x = solution.variables
        with open("dict.txt", "r") as file:
            content = file.read()
            my_dict = eval(content)
        items_list = list(my_dict.items())
        p = PSO()
        p.load_state(r"D:\JeMetalpy\pso.tkl")
        ct = 0
        p.weight[0] = 100
        for d in p.alpha:
            for j in range(144):
                if x[ct] == 1:
                    key = items_list[j][0]
                    value = items_list[j][1]
                    d[key] = 1

                ct += 1
        with open("a.txt", "w") as file:
            file.write(str(p.alpha))
        solution.constraints[0] = p.constrain_1()
        solution.constraints[1] = p.constrain_2()
        solution.constraints[2] = p.constrain_3()
        solution.constraints[3] = p.constrain_4()
        solution.constraints[4] = p.constrain_6()
        solution.constraints[5] = p.constrain_7()
        solution.constraints[6] = p.constrain_8()
        solution.constraints[7] = p.constrain_10()
        solution.constraints[8] = p.constrain_13()
        solution.constraints[9] = p.constrain_14()
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
        ) * (1000000)
        print(
            f"ppp,,,{p.constrain_1()},{p.constrain_2()},{p.constrain_3()},{p.constrain_4()},{p.constrain_6()},{p.constrain_7()},{p.constrain_8()},{p.constrain_10()}{p.constrain_13()}{p.constrain_14()}"
        )
        solution.objectives[0] = p.evaluate_1(punish)
        if punish != 0:
            solution = copy(solution.attributes["local_best"])
            solution.attributes["local_best"] = copy(solution)
        return solution

    def name(self):
        return "ZDT1"


class ZDT1Modified(ZDT1):
    """Problem ZDT1Modified.

    .. note:: Version including a loop for increasing the computing time of the evaluation functions.
    """

    def __init__(self, number_of_variables=30):
        super(ZDT1Modified, self).__init__(number_of_variables)

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        s: float = 0.0
        for i in range(1000):
            for j in range(10000):
                s += i * 0.235 / 1.234 + 1.23525 * j
        return super().evaluate(solution)


class ZDT2(ZDT1):
    """Problem ZDT2.

    .. note:: Bi-objective unconstrained problem. The default number of variables is 30.
    .. note:: Continuous problem having a non-convex Pareto front
    """

    def eval_h(self, f: float, g: float) -> float:
        return 1.0 - pow(f / g, 2.0)

    def name(self):
        return "ZDT2"


class ZDT3(ZDT1):
    """Problem ZDT3.

    .. note:: Bi-objective unconstrained problem. The default number of variables is 30.
    .. note:: Continuous problem having a partitioned Pareto front
    """

    def eval_h(self, f: float, g: float) -> float:
        return 1.0 - sqrt(f / g) - (f / g) * sin(10.0 * f * pi)

    def name(self):
        return "ZDT3"


class ZDT4(ZDT1):
    """Problem ZDT4.

    .. note:: Bi-objective unconstrained problem. The default number of variables is 10.
    .. note:: Continuous multi-modal problem having a convex Pareto front
    """

    def __init__(self, number_of_variables: int = 10):
        """:param number_of_variables: Number of decision variables of the problem."""
        super(ZDT4, self).__init__()
        self.lower_bound = number_of_variables * [-5.0]
        self.upper_bound = number_of_variables * [5.0]
        self.lower_bound[0] = 0.0
        self.upper_bound[0] = 1.0

    def eval_g(self, solution: FloatSolution):
        g = 0.0

        for i in range(1, solution.number_of_variables):
            g += pow(solution.variables[i], 2.0) - 10.0 * cos(4.0 * pi * solution.variables[i])

        g += 1.0 + 10.0 * (solution.number_of_variables - 1)

        return g

    def eval_h(self, f: float, g: float) -> float:
        return 1.0 - sqrt(f / g)

    def name(self):
        return "ZDT4"


class ZDT5(ZDT1):
    """Problem ZDT5.

    .. note:: Bi-objective unconstrained problem. The default number of variables is 30.
    .. note:: Continuous problem having a non-convex Pareto front
    """

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        g = self.eval_g(solution)
        h = self.eval_h(solution.variables[0], g)

        solution.objectives[0] = 1.0 + g
        solution.objectives[1] = h * (1.0 - (solution.objectives[0] / h) ** 0.25)

        return solution

    def eval_g(self, solution: FloatSolution):
        g = sum(solution.variables[1:]) / (solution.number_of_variables - 1)

        g = 1.0 + 9.0 * g

        return g

    def eval_h(self, f: float, g: float) -> float:
        h = 1.0 - (f / g) ** 0.5 - (f / g) * sin(10.0 * pi * f)

        return h

    def name(self):
        return "ZDT5"


class ZDT6(ZDT1):
    """Problem ZDT6.

    .. note:: Bi-objective unconstrained problem. The default number of variables is 10.
    .. note:: Continuous problem having a non-convex Pareto front
    """

    def __init__(self, number_of_variables: int = 10):
        """:param number_of_variables: Number of decision variables of the problem."""
        super(ZDT6, self).__init__(number_of_variables=number_of_variables)

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        solution.objectives[0] = (
            1.0 - exp(-4.0 * solution.variables[0]) * (sin(6.0 * pi * solution.variables[0])) ** 6.0
        )

        g = self.eval_g(solution)
        h = self.eval_h(solution.objectives[0], g)
        solution.objectives[1] = h * g

        return solution

    def eval_g(self, solution: FloatSolution):
        g = sum(solution.variables) - solution.variables[0]
        g = g / (solution.number_of_variables - 1)
        g = pow(g, 0.25)
        g = 9.0 * g
        g = 1.0 + g

        return g

    def eval_h(self, f: float, g: float) -> float:
        return 1.0 - pow(f / g, 2.0)

    def name(self):
        return "ZDT6"
