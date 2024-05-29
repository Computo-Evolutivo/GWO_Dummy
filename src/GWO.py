from Wolf import Wolf
import random
import numpy as np
import time
import matplotlib.pyplot as plt


class GWO:

    def __init__(self, population_size, iterations, train_set, train_target, random_seed=time.time()):
        self.dimensions = len(train_set[0])
        self.population_size = population_size
        self.iterations = iterations
        self.rand = random.Random(random_seed)

        # Inicializamos la población
        self.population = [Wolf(train_set, train_target, self.rand.randint(0, 10000)) for _ in range(population_size)]

        # Datos que utilizaremos para ajustar parametros
        self.train_set = train_set
        self.train_target = train_target

        # Jerarquia de la poblacion
        self.alpha = None
        self.beta = None
        self.delta = None

        self.alpha_eval = []
        self.beta_eval = []
        self.delta_eval = []

        self.set_hierarchy()


    def initialize_population(self):
        for individual in self.population:
            individual.random_position()

    def evaluate_population(self):
        for individual in self.population:
            individual.evaluate()

    # Establecemos la jerarquia de la población
    def set_hierarchy(self):

        self.evaluate_population()

        # Ahora tomamos al mejor como el alfa, al segundo como beta, tercero como delta y todos los demas son omegas
        self.alpha = self.population[-1]
        self.beta = self.population[-2]
        self.delta = self.population[-3]

        self.generation_data()

    def generation_data(self):

        self.alpha_eval.append(self.alpha.fitness)
        self.beta_eval.append(self.beta.fitness)
        self.delta_eval.append(self.delta.fitness)

    def plot_generations(self):
        x = np.arange(0, self.iterations + 1, 1)

        self.alpha_eval = np.array(self.alpha_eval)
        self.beta_eval = np.array(self.beta_eval)
        self.delta_eval = np.array(self.delta_eval)

        plt.plot(x, self.alpha_eval, label="Alpha")
        plt.plot(x, self.beta_eval, label="Beta")
        plt.plot(x, self.delta_eval, label="Delta")

        plt.title("Evolución de los mejores ejemplares por generación")
        plt.xlabel("Generación")
        plt.ylabel("Aptitud")

        plt.legend()

        plt.show()

    def hunt(self):
        # Realizamos los ciclos especificados
        for iteration in range(self.iterations):

            # a decrementa paulatinamente de 2 a 0
            a = 2 - iteration * (2 / self.iterations)

            # Actualizamos la posicion de todos los miembros de la población
            for wolf in range(self.population_size):

                # Ecuación 3.3

                A_1 = 2 * a * random.random() - a
                A_2 = 2 * a * random.random() - a
                A_3 = 2 * a * random.random() - a

                # Ecuación 3.4

                C_1 = 2 * random.random()
                C_2 = 2 * random.random()
                C_3 = 2 * random.random()

                X_1 = [0 for _ in range(self.dimensions)]
                X_2 = [0 for _ in range(self.dimensions)]
                X_3 = [0 for _ in range(self.dimensions)]
                X_t_prime = [0 for _ in range(self.dimensions)]

                # Ecuaciones 3.5, 3.6 y 3.7
                for dim in range(self.dimensions):
                    X_1[dim] = self.alpha.pos[dim] - A_1 * abs(
                        C_1 * self.alpha.pos[dim] - self.population[wolf].pos[dim])
                    X_2[dim] = self.beta.pos[dim] - A_2 * abs(C_2 * self.beta.pos[dim] - self.population[wolf].pos[dim])
                    X_3[dim] = self.delta.pos[dim] - A_3 * abs(
                        C_3 * self.delta.pos[dim] - self.population[wolf].pos[dim])
                    X_t_prime[dim] = (X_1[dim] + X_2[dim] + X_3[dim]) / 3

                old_eval = self.population[wolf].fitness
                old_position = self.population[wolf].pos
                self.population[wolf].update_position = X_t_prime
                new_eval = self.population[wolf].fitness
                if old_eval > new_eval:
                    self.population[wolf].update_position = old_position

            self.population = np.sort(self.population)
            self.set_hierarchy()

        self.plot_generations()

        return self.alpha
