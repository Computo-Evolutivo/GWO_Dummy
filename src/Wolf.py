import random
import time
from sklearn.metrics import accuracy_score
from math import exp


class Wolf:

    def __init__(self, features, target, seed=time.time()):
        self.features = features
        self.dimensions = len(features) + 1
        self.function = accuracy_score
        # El valor mínimo y máximo que puede tomar un coeficiente
        self.min, self.max = -10, 10
        self.pos = [0] * self.dimensions
        self.fitness = 0
        self.seed = seed
        self.random = random.Random(seed)
        self.predictions = [0] * len(self.features)
        self.expected = target

        # Inicializamos a la población
        self.random_position()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __gt__(self, other):
        return self.fitness >= other.fitness

    # Inicializamos el gen de manera aleatoria
    def random_position(self):
        self.pos = [(self.random.random() * (self.max - self.min) + self.min) for _ in range(self.dimensions)]

    # Evalúa nuestro gen en el conjunto de entranamiento (con sezgo)
    def evaluate(self):
        self.calculate_probabilities()
        self.fitness = accuracy_score(self.expected, self.predictions)
        return self.fitness

    def calculate_probabilities(self):
        for p in range(len(self.features)):
            # Inicializamos la suma como el valor independiente
            val = self.pos[0]
            for index in range(len(self.features[0])):
                # Sumamos el valor de la variable por el peso asociado (se desplaza 1 ya que tenemos el valor independiente)
                val += self.features[p][index] * self.pos[index + 1]
            # Una vez que tengamos eso calculamos el valor de la prediccion
            exp_val = exp(val)
            prob = exp_val / (1 + exp_val)
            # Despues si la probabilidad es mayor a 50% consideramos que está prendido el valor y predecimos un positivo
            if prob >= .5:
                self.predictions[p] = 1
            else:
                self.predictions[p] = 0
    
    def update_position(self, new_position):
        self.pos = new_position

    def get_position(self):
        return self.pos

    def __str__(self):
        return f"Predicciones: {self.predictions}\nAptitud: {self.fitness}"
