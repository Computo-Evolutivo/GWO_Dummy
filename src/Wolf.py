import random
import time


class Wolf:

    def __init__(self, dims, function, seed=time.time()):
        self.dimensiones = dims
        self.function = function
        self.function_name = type(function).__name__
        self.min, self.max = function.get_range()
        self.pos = [0 for _ in range(self.dimensiones)]
        self.fitness = 0
        self.seed = seed
        self.random = random.Random(seed)


    def __lt__(self, other):
        return self.fitness < other.fitness


    def __gt__(self, other):
        return self.fitness >= other.fitness


    # Inicializamos el gen de manera aleatoria
    def random_position(self):
        self.pos = [self.random.random() * (self.max - self.min) + self.min for _ in range(self.dimensiones)]
        self.function.set_vals(self.pos)


    # Imprime los valores reales correspondientes a los bits
    def show_values(self):
        for d in range(len(self.pos)):
            print(f"Posición en dimensión {d + 1}: {self.pos[d]}")
        print(f"Evaluación: {self.fitness}")


    # Evalúa nuestro gen en la función
    def evaluate(self, verbose=False):
        self.fitness = self.function.evaluate()
        if verbose:
            print(f"La evaluación de la función {self.function_name} con los valores {self.pos} es de {self.eval}")
        return self.fitness
    
    def update_position(self, new_position):
        self.pos = new_position
        self.function.set_vals(self.pos)