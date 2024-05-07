from math import sqrt, e, cos, pi, exp
import numpy as np


def square_vector(vec):
    return [v ** 2 for v in vec]


class Function:

    def __init__(self, min_range, max_range, vals):
        self.min = min_range
        self.max = max_range
        self.vals = vals
        self.eval = 0

    def set_vals(self, vals):
        self.vals = vals

    def get_range(self):
        return self.min, self.max

    def evaluate(self):
        return 0


class Sphere(Function):

    def __init__(self, vals=None):
        super().__init__(-5.12, 5.12, vals)

    def evaluate(self):

        self.eval = np.sum(square_vector(self.vals))
        return self.eval


class Ackley(Function):

    def __init__(self, vals=None):
        super().__init__(-32.768, 32.768, vals)

    def evaluate(self):
        val = 20 + e
        sum1 = np.sum(np.square(self.vals))  # Corregido: Se usa np.square en lugar de square_vector
        n = len(self.vals)
        val -= 20 * exp(-0.2 * sqrt((1 / n) * sum1))
        aux = 2 * pi * np.array(self.vals)  # Convertir a array de numpy
        sum2 = np.sum(np.cos(aux))
        val -= exp((1 / n) * sum2)

        self.eval = val
        return self.eval
    
    
class Griewank(Function):

    def __init__(self, vals=None):
        super().__init__(-600, 600, vals)

    def evaluate(self):
        val = 1
        sum1 = np.sum(square_vector(self.vals))
        val += sum1/4000
        aux = (self.vals[i] / sqrt(i + 1) for i in range(len(self.vals)))
        aux2 = [cos(val) for val in aux]
        val -= np.prod(aux2)
        self.eval = val
        return self.eval


class Rastrigin(Function):

    def __init__(self, vals=None):
        super().__init__(-5.12, 5.12, vals)

    def evaluate(self):
        n = len(self.vals)
        val = 10 * n
        aux = list(self.vals[i] / np.sqrt(i + 1) for i in range(len(self.vals)))  # Convertir el generador en una lista
        val -= np.prod(np.cos(aux))  # Aplicar np.cos a cada elemento de aux y luego calcular el producto
        self.eval = val
        return self.eval


class Rosenbrock(Function):
    def __init__(self, vals=None):
        super().__init__(-2.048, 2.048, vals)

    def evaluate(self):
        term1 = [(self.vals[i + 1] - self.vals[i] ** 2) ** 2 for i in range(len(self.vals) - 1)]
        term2 = [(self.vals[i] - 1) ** 2 for i in range(len(self.vals) - 1)]

        self.eval = np.sum(100 * term1 + term2)
        return self.eval

