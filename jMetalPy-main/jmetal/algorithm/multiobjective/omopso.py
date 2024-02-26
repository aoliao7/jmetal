import random
from copy import copy
from typing import List, Optional, TypeVar
import math
import numpy
from jmetal.problem.multiobjective.pso import PSO
from jmetal.config import store
from jmetal.core.algorithm import ParticleSwarmOptimization
from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution, IntegerSolution
from jmetal.operator import UniformMutation
from jmetal.operator.mutation import NonUniformMutation
from jmetal.util.archive import BoundedArchive, NonDominatedSolutionsArchive
from jmetal.util.comparator import DominanceComparator, EpsilonDominanceComparator
from jmetal.util.evaluator import Evaluator
from jmetal.util.generator import Generator
from jmetal.util.termination_criterion import TerminationCriterion
from jmetal.problem.multiobjective.pso import PSO

R = TypeVar("R")

"""
.. module:: OMOPSO
   :platform: Unix, Windows
   :synopsis: Implementation of SMPSO.

.. moduleauthor:: Antonio J. Nebro <antonio@lcc.uma.es>
"""


class OMOPSO(ParticleSwarmOptimization):
    def __init__(
        self,
        problem: FloatProblem,
        swarm_size: int,
        # uniform_mutation: UniformMutation,
        # non_uniform_mutation: NonUniformMutation,
        leaders: Optional[BoundedArchive],
        epsilon: float,
        termination_criterion: TerminationCriterion,
        swarm_generator: Generator = store.default_generator,
        swarm_evaluator: Evaluator = store.default_evaluator,
    ):
        """This class implements the OMOPSO algorithm as described in

        todo Update this reference
        * SMPSO: A new PSO-based metaheuristic for multi-objective optimization

        The implementation of OMOPSO provided in jMetalPy follows the algorithm template described in the algorithm
        templates section of the documentation.

        :param problem: The problem to solve.
        :param swarm_size: Size of the swarm.
        :param leaders: Archive for leaders.
        """
        super(OMOPSO, self).__init__(problem=problem, swarm_size=swarm_size)
        self.swarm_generator = swarm_generator
        self.swarm_evaluator = swarm_evaluator

        self.termination_criterion = termination_criterion
        self.observable.register(termination_criterion)

        self.max_evaluations = 3000
        self.origin_evaluation = 300
        # self.uniform_mutation = uniform_mutation
        # self.non_uniform_mutation = non_uniform_mutation

        self.leaders = leaders
        self.one = 0
        self.zero = 0
        self.change = 0
        self.change_list = []
        self.epsilon = epsilon
        self.epsilon_archive = NonDominatedSolutionsArchive(EpsilonDominanceComparator(epsilon))

        self.c1_min = 1.5
        self.c1_max = 2.0
        self.c2_min = 1.5
        self.c2_max = 2.0
        self.r1_min = 0.0
        self.r1_max = 1.0
        self.r2_min = 0.0
        self.r2_max = 1.0
        self.weight_min = 0.1
        self.weight_max = 0.5
        self.change_velocity1 = -1
        self.change_velocity2 = (
            -1
        )  # 粒子在碰到边界时速度方向会反转。这种处理可以防止粒子超出定义的搜索空间，同时允许它们在边界附近探索。

        self.dominance_comparator = DominanceComparator()

        self.speed = numpy.zeros((self.swarm_size, self.problem.number_of_variables()), dtype=float)
        # print("speed", self.speed)

    def create_initial_solutions(self) -> List[FloatSolution]:
        return [self.swarm_generator.new(self.problem, _) for _ in range(self.swarm_size)]

    def evaluate(self, solution_list: List[FloatSolution]):
        return self.swarm_evaluator.evaluate(solution_list, self.problem)

    def stopping_condition_is_met(self) -> bool:
        return self.termination_criterion.is_met

    def initialize_global_best(self, swarm: List[FloatSolution]) -> None:
        for particle in swarm:
            if self.leaders.add(particle):
                self.epsilon_archive.add(copy(particle))

    def initialize_particle_best(self, swarm: List[FloatSolution]) -> None:
        for particle in swarm:
            particle.attributes["local_best"] = copy(particle)  ##粒子当前自身的拷贝

    def initialize_velocity(self, swarm: List[FloatSolution]) -> None:
        for i in range(self.swarm_size):
            for j in range(self.problem.number_of_variables()):
                self.speed[i][j] = 0.0

    def find_least(self, swarm: List[FloatSolution], index: int) -> int:
        # 将列表分成每300个一组，形成60个对象
        data = numpy.array(swarm[index].variables)
        objects = data.reshape(-1, 144)

        # 计算每个对象中的变量之和
        sums = objects.sum(axis=1)

        # 找到和的最小值
        min_sum = sums.min()

        # 找出所有等于最小和的对象的索引
        rand = random.randint(0, 3)
        # if rand == 0:
        #     min_indices = numpy.where(sums >= 0)[0]

        #     least_g = random.sample(list(min_indices), 1)
        # else:
        a = [0, 1, 2, 3, 4, 5, 6, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
        least_g = random.sample(a, 1)
        return least_g

    def find_most(self, swarm: List[FloatSolution], index: int) -> int:
        # 将列表分成每300个一组，形成60个对象
        data = numpy.array(swarm[index].variables)

        objects = data.reshape(-1, 144)

        # 计算每个对象中的变量之和
        sums = objects.sum(axis=1)
        # print("sums", sums)
        max_sum = sums.max()
        # 找出所有等于最小和的对象的索引
        # print("sums", sums)
        max = numpy.where(sums >= 1)
        a = random.sample([i for i in range(len(max))], 1)
        max_indices = max[a[0]]
        # print("max_indices", max_indices)
        if len(max_indices) == 0:
            max_indices = numpy.where(sums == max_sum)[0]
        most_g = random.sample(list(max_indices), 1)
        random_one = random.sample([num for num in range(len(objects[most_g[0]])) if objects[most_g[0]][num] == 1], 1)
        return most_g, random_one

    def find_random(self, swarm: List[FloatSolution], index: int) -> int:
        data = numpy.array(swarm[index].variables)
        objects = data.reshape(-1, 144)
        sums = objects.sum(axis=1)
        max_sum = sums.max()
        max = numpy.where(sums >= 2)
        a = random.sample([i for i in range(len(max))], 1)
        max_indices = max[a[0]]
        if len(max_indices) == 0:
            max_indices = numpy.where(sums == max_sum)[0]
        most_g = random.sample(list(max_indices), 1)
        random_one = random.sample([num for num in range(len(objects[most_g[0]])) if objects[most_g[0]][num] == 1], 2)
        return most_g, random_one

    def test_cons(self, swarm: List[FloatSolution], index: int) -> bool:
        with open("dict.txt", "r") as file:
            content = file.read()
            my_dict = eval(content)
        items_list = list(my_dict.items())
        p = PSO()
        # print(os.getcwd())
        p.load_state(r"D:\JeMetalpy\pso.tkl")
        ct = 0
        for d in p.alpha:
            for j in range(144):
                if swarm[index].variables[ct] == 1:
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
        if punish != 0:
            return False
        return True

    def update_velocity(self, swarm: List[FloatSolution]) -> None:
        for i in range(self.swarm_size):
            best_particle = copy(swarm[i].attributes["local_best"])
            best_global = (
                self.select_global_best()
            )  # 全局解大于2就随机选两个，再从两个中跳一个  小于等于2个,就随便取一个

            r1 = round(random.uniform(self.r1_min, self.r1_max), 1)
            r2 = round(random.uniform(self.r2_min, self.r2_max), 1)
            c1 = round(random.uniform(self.c1_min, self.c1_max), 1)
            c2 = round(random.uniform(self.c2_min, self.c2_max), 1)
            w = round(random.uniform(self.weight_min, self.weight_max), 1)

            change_flight = 1

            for c in range(int(change_flight)):
                most_g, gu = self.find_most(swarm, i)
                u = gu[0]
                ff = self.find_least(swarm, i)
                fg = ff[0]
                origin_data = swarm[i].variables[u + fg * 144]
                true_speed = (
                    w * self.speed[i][u + fg * 144]
                    + (c1 * r1 * (best_particle.variables[u + fg * 144] - swarm[i].variables[u + fg * 144]))
                    + (c2 * r2 * (best_global.variables[u + fg * 144] - swarm[i].variables[u + fg * 144]))
                )
                s_speed = 1 / (1 + numpy.exp(-1 * true_speed))
                r = random.uniform(0, 1)
                if r < s_speed:
                    self.speed[i][u + fg * 144] = 1
                else:
                    self.speed[i][u + fg * 144] = 0
                if origin_data != self.speed[i][u + fg * 144]:
                    if self.speed[i][u + fg * 144] == 1:
                        for a in range(60):
                            if a != fg:
                                swarm[i].variables[u + a * 144] = 0
                        swarm[i].variables[u + fg * 144] = 1
                        print("0->1", most_g[0], fg)
                    elif self.speed[i][u + fg * 144] == 0:
                        swarm[i].variables[u + fg * 144] = 0
                        least_g = self.find_least(swarm, i)
                        while least_g[0] == fg:
                            least_g = self.find_least(swarm, i)
                        swarm[i].variables[u + least_g[0] * 144] = 1
                        print("1->0", least_g[0])
                        # p = random.sample(range(60), 1)

                        # swarm[i].variables[u + p[0] * 144] = 1
            # if self.evaluations / self.origin_evaluation == 3:
            #     count = 1
            #     while count <= 3:
            #         least1 = self.find_least(swarm, i)
            #         least2 = self.find_least(swarm, i)
            #         if least1[0] == least2[0]:
            #             continue
            #         most1, one1 = self.find_random(swarm, i)
            #         most2, one2 = self.find_random(swarm, i)
            #         least1[0] = 21
            #         least2[0] = 29
            #         if swarm[i].variables[one1[0] + least1[0] * 144] == 0:
            #             swarm[i].variables[one1[0] + least1[0] * 144] = 1
            #             swarm[i].variables[one1[0] + most1[0] * 144] = 0
            #             if not self.test_cons(swarm, i):
            #                 # count -= 1
            #                 swarm[i].variables[one1[0] + least1[0] * 144] = 0
            #                 swarm[i].variables[one1[0] + most1[0] * 144] = 1
            #         if swarm[i].variables[one2[1] + least2[0] * 144] == 0:
            #             swarm[i].variables[one2[1] + least2[0] * 144] = 1
            #             swarm[i].variables[one2[1] + most2[0] * 144] = 0
            #             if not self.test_cons(swarm, i):
            #                 swarm[i].variables[one2[1] + least2[0] * 144] = 0
            #                 swarm[i].variables[one2[1] + most2[0] * 144] = 1
            #                 # count -= 1
            #         count += 1

    def update_position(self, swarm: List[FloatSolution]) -> None:
        k = 1

    def update_global_best(self, swarm: List[FloatSolution]) -> None:
        for particle in swarm:
            if self.leaders.add(copy(particle)):
                self.epsilon_archive.add(copy(particle))

    def update_particle_best(self, swarm: List[FloatSolution]) -> None:
        for i in range(self.swarm_size):
            flag = self.dominance_comparator.compare(swarm[i], swarm[i].attributes["local_best"])
            if flag != -1:
                swarm[i].attributes["local_best"] = copy(swarm[i])

    def perturbation(self, swarm: List[FloatSolution]) -> None:
        self.non_uniform_mutation.set_current_iteration(self.evaluations / self.swarm_size)
        for i in range(self.swarm_size):
            if (i % 3) == 0:
                self.non_uniform_mutation.execute(swarm[i])
            else:
                self.uniform_mutation.execute(swarm[i])

    def select_global_best(self) -> FloatSolution:
        leaders = self.leaders.solution_list
        if len(leaders) > 2:
            particles = random.sample(leaders, 2)
            if self.leaders.comparator.compare(particles[0], particles[1]) < 1:
                best_global = copy(particles[0])
            else:
                best_global = copy(particles[1])
        else:
            if len(self.leaders.solution_list) != 0:
                best_global = copy(self.leaders.solution_list[0])

        return best_global

    def init_progress(self) -> None:
        self.evaluations = self.swarm_size
        self.leaders.compute_density_estimator()

        self.initialize_velocity(self.solutions)
        self.initialize_particle_best(self.solutions)
        self.initialize_global_best(self.solutions)

    def update_progress(self) -> None:
        self.evaluations += self.swarm_size
        self.leaders.compute_density_estimator()

        observable_data = self.observable_data()
        observable_data["SOLUTIONS"] = self.epsilon_archive.solution_list
        self.observable.notify_all(**observable_data)

    def get_result(self) -> List[FloatSolution]:
        return self.epsilon_archive.solution_list

    def get_ones(self) -> List[FloatSolution]:
        return self.one

    def get_zeros(self) -> List[FloatSolution]:
        return self.zero

    def get_leaders(self) -> List[FloatSolution]:
        return self.leaders.solution_list

    def get_evalutions(self) -> int:
        return self.evaluations

    def get_changes(self) -> int:
        return self.change

    def get_change_list(self) -> List[int]:
        return self.change_list

    def get_name(self) -> str:
        return "OMOPSO"
