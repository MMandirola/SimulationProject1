import numpy as np
from multiprocessing import Pool
import time
import csv

# Especifico los rangos de valores que puede tomar las variables de decision
cantidades = (range(0,78), range(0,78), range(0,78), range(0,78))
# Especifico la maxima cantidad de habitaciones
maximas_habitaciones = 77
# Calculo todas las combinaciones posibles de las variables de decision
combinaciones_posibles = [[x,y,z,w] for x in cantidades[0] for y in cantidades[1] for z in cantidades[2] for w in cantidades[3] if x + y + z + w <= maximas_habitaciones]

# funcion que ejecuta una simulacion
def simulation(combinations):
    data = []
    # Digo como se van a calcular las variables aleatorias
    variaciones = (lambda : np.random.triangular(-20,-10,0), lambda : np.random.triangular(-15, -7.5, 0)
    ,lambda : np.random.triangular(-5, -2, 0), lambda : np.random.triangular(0, 1, 5))
    #Seteo los parametros
    precios = (78, 97, 120, 180)
    demandas = (175, 140, 115, 75)
    reacciones = (5, 2.5, 0.5, 0.01)
    habitaciones_existentes = (200, 200, 200, 100)
    # Se setea la cantidad de repeticiones
    cant_repeticiones = 500
    # se guara el mejor caso y la combinacion que la genera
    multiplicidad = 0
    mejor_caso = 0
    # Para cada una de las combinaciones de las variables de decision
    for z in range(len(combinations)):
        j = combinations[z]
        ganancias = 0
        varianza = 0
        # Para cada una de las repeticiones
        for k in range(0, cant_repeticiones):
            ganancia = 0
            # Para cada uno de los tipos de apartamentos
            for i in range(0, len(variaciones)):
                # Se calcula la ganancia
                precio_variado = variaciones[i]()
                precio_total = precios[i] * (1 + precio_variado/100)
                variacion_demanda = reacciones[i] * (-precio_variado) / 100 + 1
                demanda_total = demandas[i] * variacion_demanda
                habitaciones_construidas = habitaciones_existentes[i] +  j[i]
                habitaciones_alquiladas = min(demanda_total, habitaciones_construidas)
                ganancia += habitaciones_alquiladas * precio_total
            ganancias += ganancia
            varianza += ganancia ** 2 / cant_repeticiones
        # se calcula la media y la varianza
        p = ganancias / cant_repeticiones
        v = varianza - p ** 2
        data.append(j + [p,v])
        # Nos quedamos con el mejor caso
        if mejor_caso < p:
            mejor_caso = p
            multiplicidad = j
    return multiplicidad, mejor_caso, data

# Se parte la lista de comibaciones en 8 para utilizar varios hilos de ejecucion
partition_size = round(len(combinaciones_posibles) / 8)
print (partition_size)
threads = []
# Se utiliza un objeto pool para manejar el paralelismo
pool = Pool()
for i in range(0, 8):
    partition_start = partition_size * i
    partition_end = partition_size * (i + 1)
    # Se ejecuta un thread con una paticion de la lista de combinaciones
    threads.append(pool.apply_async(simulation, args=[combinaciones_posibles[partition_start: partition_end]]) )

# Se espera a qe terminen los threads y se queda con el mejor candidato
combination = []
revenue = 0
all_data = []
for thread in threads:
    perm, profit, data = thread.get()
    all_data += data
    if profit > revenue:
        revenue = profit
        combination = perm

# Se escriben las observaciones
with open('data.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in all_data:
        spamwriter.writerow(row)

#Se muestra el mejor candidato
print("%d Economico, %d Negocios, %d Ejecutiva, %d Premium,  %f Ganancia" %
    ( combination[0], combination[1], combination[2], combination[3] , revenue))