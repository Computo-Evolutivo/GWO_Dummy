#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random
import time
import numpy as np
import copy
from math import exp, ceil
import analysis


# In[3]:


class Genotype:

    def __init__(self, dims, bits, function, seed=time.time()):
        self.seed = seed
        self.random = random.Random(seed)
        self.dimensiones = dims
        self.acc = bits
        self.function = function
        self.function_name = type(function).__name__
        if function is not None:
            self.min, self.max = function.get_range()
        else:
            self.min = None
            self.max = None
        self.bits = [False] * (bits * dims)
        self.decs = [0 for _ in range(self.dimensiones)]
        self.eval = 0
        
    def __lt__(self, other):
        return self.eval < other.eval
    
    def __gt__(self, other):
        return self.eval >= other.eval
    
    def set_range(self):
        self.min, self.max = self.function.get_range()

    # Inicializamos el gen de manera aleatoria
    def random_genotype(self):
        self.bits = [self.random.choice([False, True]) for _ in range(self.acc * self.dimensiones)]

    # Convierte un vector de booleanos a decimal
    @staticmethod
    def vector_to_dec(vec):
        val = 0
        for i in range(len(vec)):
            val += vec[i] * (2 ** (len(vec) - 1 - i))
        return val

    # Convierte los bits a un arreglo de reales
    def decodify(self):
        # Establecemos variables para mejor legibilidad
        dims = self.dimensiones
        bits = self.acc
        # Ciclamos nuestro arreglo de booleanos
        for d in range(dims):
            # Inicializamos la memoria necesaria
            bit_vector = [False for _ in range(self.acc)]
            # Ciclamos los bits de una dimensión
            for b in range(bits):
                #print(f"Lugar: {(d * bits) + b}, Rango: {len(self.bits)}")
                #Accedemos al bit actual y lo agregamos al vector
                bit_vector[b] = self.bits[(d * bits) + b]

            # Rango de la representación
            diff = self.max - self.min
            # Representación del vector de booleanos en decimal
            dec = self.vector_to_dec(bit_vector)
            # Máximo posible con los bits dados
            max_num = (2 ** self.acc) - 1
            # Porcentaje de numero dado entre el maximo
            ratio = dec / max_num
            # El decimal de la dimensión d es igual a la tasa por el rango más el minimo
            self.decs[d] = ratio * diff + self.min
        # Una vez tengamos todos los valores decodificados los pasamos a la función
        self.function.set_vals(self.decs)
        return self.decs

    # Una función que imprime los bits de manera legible
    def print_bits(self):
        c = 0
        line = ""
        for b in range(len(self.bits)):
            if (b % self.acc) == 0:
                line = ""
                c += 1
                line += f"Valor {c}:"
            line += str(int(self.bits[b]))
            if ((b + 1) % self.acc) == 0 and b != 0:
                print(line)
            
    # Imprime los valores reales correspondientes a los bits
    def print_decs(self):
        for d in range(len(self.decs)):
            print(f"Valor {d + 1}: {self.decs[d]}")
    
    def deci(self):
        for d in range(len(self.decs)):
            self.decs[d]
            
    # Cambia un gen aleatorio de la solución
    def mutar_gen(self):
        place = self.random.choice(range(len(self.bits)))
        bits_copy = self.bits[:]
        bits_copy[place] = not bits_copy[place]
        #print(f"Rango: {range(len(self.bits))}, Lugar: {place}")
        return bits_copy 
            
    # Evalúa nuestro gen en la función
    def evaluate(self, verbose=True):
        self.eval = self.function.evaluate()
        if verbose:
            print(f"La evaluación de la función {self.function_name} con los valores {self.decs} es de {self.eval}")
        return self.eval
    
    def set_function(self, function):
        self.function = function
    
    def get_eval(self):
        return self.eval
    
    def get_bits(self):
        return self.bits
    
    def set_bits(self, new_bits):
        self.bits = new_bits
        

