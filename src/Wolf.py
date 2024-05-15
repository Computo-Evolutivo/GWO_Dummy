import random
import time
from sklearn.metrics import accuracy_score
from math import exp


class Wolf:

    def __init__(self, features, train_target, test_features, test_target, seed=time.time()):
        self.features = features
        self.test_features = test_features
        self.dimensiones = len(features)
        self.function = accuracy_score
        # El valor mínimo y máximo que puede tomar un coeficiente
        self.min, self.max = -1000, 1000
        self.pos = [0 for _ in range(self.dimensiones + 1)]
        self.fitness = 0
        self.seed = seed
        self.random = random.Random(seed)
        self.predictions = [0 * len(self.features)]
        self.test_predictions = [0 * len(self.features)]
        self.expected = train_target
        self.test_expected = test_target

        # Inicializamos a la población
        self.random_position()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness >= other.fitness

    # Inicializamos el gen de manera aleatoria
    def random_position(self):
        self.pos = [self.random.random() for _ in range(self.dimensiones + 1)]

    # Imprime los valores reales correspondientes a los bits
    def show_values(self):
        for d in range(len(self.pos)):
            print(f"Posición en dimensión {d + 1}: {self.pos[d]}")
        print(f"Evaluación: {self.fitness}")

    # Evalúa nuestro gen en el conjunto de entranamiento (con sezgo)
    def evaluate_train(self):
        self.fitness = accuracy_score(self.expected, self.predictions)
        return self.fitness

    # Evalúa nuestro gen en el conjunto de prueba (sin sezgo)
    def evaluate_test(self):
        test_error = accuracy_score(self.test_expected, self.test_predictions)
        return test_error

    def calculate_probabilities(self):
        for p in range(len(self.features)):
            # Inicializamos la suma como el valor independiente
            val = self.pos[0]
            for index in range(len(self.features)):
                # Sumamos el valor de la variable por el peso asociado (se desplaza 1 ya que tenemos el valor independiente)
                val += self.features[index] * self.pos[index + 1]
            # Una vez que tengamos eso calculamos el valor de la prediccion
            exp_val = exp(val)
            prob = exp_val / 1 + exp_val
            # Despues si la probabilidad es mayor a 50% consideramos que está prendido el valor y predecimos un positivo
            if prob >= .5:
                self.predictions[p] = 1
            else:
                self.predictions[p] = 0
    
    def update_position(self, new_position):
        self.pos = new_position
        self.function.set_vals(self.pos)