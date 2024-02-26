import random
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from jmetal.core.observer import Observer
from jmetal.core.solution import (
    BinarySolution,
    FloatSolution,
    IntegerSolution,
    PermutationSolution,
)
from jmetal.logger import get_logger
from jmetal.problem.multiobjective.pso import PSO
import ast

import jmetal.problem.multiobjective.globalmanger as gm

logger = get_logger(__name__)

S = TypeVar("S")


class Problem(Generic[S], ABC):
    """Class representing problems."""

    MINIMIZE = -1
    MAXIMIZE = 1

    def __init__(self):
        # self.reference_front: List[S] = []

        self.directions: List[int] = []
        self.labels: List[str] = []

    @abstractmethod
    def number_of_variables(self) -> int:
        pass

    @abstractmethod
    def number_of_objectives(self) -> int:
        pass

    @abstractmethod
    def number_of_constraints(self) -> int:
        pass

    @abstractmethod
    def create_solution(self) -> S:
        """Creates a random_search solution to the problem.

        :return: Solution."""
        pass

    @abstractmethod
    def evaluate(self, solution: S) -> S:
        """Evaluate a solution. For any new problem inheriting from :class:`Problem`, this method should be replaced.
        Note that this framework ASSUMES minimization, thus solutions must be evaluated in consequence.

        :return: Evaluated solution."""
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class DynamicProblem(Problem[S], Observer, ABC):
    @abstractmethod
    def the_problem_has_changed(self) -> bool:
        pass

    @abstractmethod
    def clear_changed(self) -> None:
        pass


class BinaryProblem(Problem[BinarySolution], ABC):
    """Class representing binary problems."""

    def __init__(self):
        super(BinaryProblem, self).__init__()


class FloatProblem(Problem[FloatSolution], ABC):
    """Class representing float problems."""

    def __init__(self):
        super(FloatProblem, self).__init__()
        self.lower_bound = []
        self.upper_bound = []

    def number_of_variables(self) -> int:
        return len(self.lower_bound)

    def is_valid(self, matrix, slot, flight):
        # 检查当前机位是否可以分配给当前航班
        # 这里检查的是该机位在当前解决方案中是否已经被其他航班占用
        x = [i for i in range(18000)]
        flag = 0
        for s in range(slot):
            for f in range(flight):
                x[flag] = matrix[s][f]
                flag = flag + 1
        # print("flag", flag)
        # print("dasdas", x)
        p = PSO(x)
        # print(matrix)
        with open("matrix.txt", "w") as file:
            file.write(str(matrix))
        constrain_1 = p.constrain_1()
        constrain_4 = p.constrain_4()
        constrain_7 = p.constrain_7()
        constrain_8 = p.constrain_8()
        #     # 检查列表是否满足自定义约束条件
        #     if not constrain_1 and not constrain_4 and not constrain_7 and not constrain_8:
        if constrain_4 + constrain_7 + constrain_8 < 0:  # 如果当前航班已被分配到该机位
            print("sumconstrains", constrain_4 + constrain_7 + constrain_8)
            return False
        else:
            print("sumconstrains", constrain_4 + constrain_7 + constrain_8)
        return True

    def backtrack(self, matrix, slot, S, F):
        # 如果所有机位都尝试过了，返回True
        if slot == S:
            return True

        # 尝试为当前机位分配每个可能的航班
        for flight in range(F):  # 注意这里的范围是F，代表航班的数量
            if self.is_valid(matrix, S, F):
                # 做选择：将当前机位分配给当前航班
                matrix[slot][flight] = 1
                # 继续尝试分配下一个机位
                if self.backtrack(matrix, slot + 1, S, F):
                    return True
                # 撤销选择
                matrix[slot][flight] = 0

        return False

    def is_valid2(self, matrix, slot, flight_index, p):
        # 这里应该包含判断逻辑，例如检查机位是否已经被其他航班占用等
        # 示例判断逻辑：检查该机位是否已经被占用
        current_flight = p.F[flight_index]
        # 检查机位是否已被当前时间段内的其他航班占用
        # for f_index in range(len(p.F)):
        #     # if matrix[slot][f_index] == 1:
        #     if matrix[slot][f_index] == 1:
        #         if p.f[f_index][2] - current_flight[1] < 1:
        #             return False
        #     if matrix[slot][f_index] == 1:
        matrix[slot][current_flight[0]] = 1
        p.alpha[slot][current_flight[0]] = 1
        if (
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
        ) == 0:
            return True
        else:
            p.alpha[slot][current_flight[0]] = 0
            matrix[slot][current_flight[0]] = 0
            return False

        return True  # 当前机位可以分配给当前航班

    def create_solution(self, index) -> FloatSolution:
        new_solution = FloatSolution(
            self.lower_bound, self.upper_bound, self.number_of_objectives(), self.number_of_constraints()
        )
        # new_solution.variables = [
        #     random.uniform(self.lower_bound[i] * 1.0, self.upper_bound[i] * 1.0)
        #     for i in range(self.number_of_variables())
        # ]
        # print("newso", new_solution)

        # new_solution.variables = [random.randint(0, 1) for _ in range(self.number_of_variables())]
        # new_solution.variables = [binary_list[_] for _ in range(self.number_of_variables())]

        slots = 60
        flights = 144
        kt = 0
        swarms = 200
        if index == 0:
            with open("finallist.txt", "r") as file:
                input_list = eval(file.read())
                new_solution.variables = input_list[:]
            gm._init()
            gm.set_value("origindata", new_solution.variables)
        else:
            data = gm.get_value("origindata")
            for s in range(len(data)):
                new_solution.variables[s] = data[s]
        return new_solution


class IntegerProblem(Problem[IntegerSolution], ABC):
    """Class representing integer problems."""

    def __init__(self):
        super(IntegerProblem, self).__init__()
        self.lower_bound = []
        self.upper_bound = []

    def number_of_variables(self) -> int:
        return len(self.lower_bound)

    def create_solution(self) -> IntegerSolution:
        new_solution = IntegerSolution(
            self.lower_bound, self.upper_bound, self.number_of_objectives(), self.number_of_constraints()
        )
        new_solution.variables = [
            round(random.uniform(self.lower_bound[i] * 1.0, self.upper_bound[i] * 1.0))
            for i in range(self.number_of_variables())
        ]

        return new_solution


class PermutationProblem(Problem[PermutationSolution], ABC):
    """Class representing permutation problems."""

    def __init__(self):
        super(PermutationProblem, self).__init__()


class OnTheFlyFloatProblem(FloatProblem):
    """ Class for defining float problems on the fly.

        Example:

        >>> # Defining problem Srinivas on the fly
        >>> def f1(x: [float]):
        >>>     return 2.0 + (x[0] - 2.0) * (x[0] - 2.0) + (x[1] - 1.0) * (x[1] - 1.0)
        >>>
        >>> def f2(x: [float]):
        >>>     return 9.0 * x[0] - (x[1] - 1.0) * (x[1] - 1.0)
        >>>
        >>> def c1(x: [float]):
        >>>     return 1.0 - (x[0] * x[0] + x[1] * x[1]) / 225.0
        >>>
        >>> def c2(x: [float]):
        >>>     return (3.0 * x[1] - x[0]) / 10.0 - 1.0
        >>>
        >>> problem = OnTheFlyFloatProblem()\
            .set_name("Srinivas")\
            .add_variable(-20.0, 20.0)\
            .add_variable(-20.0, 20.0)\
            .add_function(f1)\
            .add_function(f2)\
            .add_constraint(c1)\
            .add_constraint(c2)
    """

    def __init__(self):
        super(OnTheFlyFloatProblem, self).__init__()
        self.functions = []
        self.constraints = []
        self.problem_name = None

    def set_name(self, name) -> "OnTheFlyFloatProblem":
        self.problem_name = name

        return self

    def add_function(self, function) -> "OnTheFlyFloatProblem":
        self.functions.append(function)

        return self

    def add_constraint(self, constraint) -> "OnTheFlyFloatProblem":
        self.constraints.append(constraint)

        return self

    def add_variable(self, lower_bound, upper_bound) -> "OnTheFlyFloatProblem":
        self.lower_bound.append(lower_bound)
        self.upper_bound.append(upper_bound)

        return self

    def number_of_objectives(self) -> int:
        return len(self.functions)

    def number_of_constraints(self) -> int:
        return len(self.constraints)

    def evaluate(self, solution: FloatSolution) -> None:
        for i in range(self.number_of_objectives()):
            solution.objectives[i] = self.functions[i](solution.variables)

        for i in range(self.number_of_constraints()):
            solution.constraints[i] = self.constraints[i](solution.variables)

    def name(self) -> str:
        return self.problem_name
