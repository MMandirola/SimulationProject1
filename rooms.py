import numpy as np
from multiprocessing import Pool

cantidades = (range(0,77), range(0,77), range(0,77), range(0,77))
maximas_habitaciones = 77
combinaciones_posibles = [(x,y,z,w) for x in cantidades[0] for y in cantidades[1] for z in cantidades[2] for w in cantidades[3] if x + y + z + w <= maximas_habitaciones]

def simulation(combinations):
    variaciones = (lambda : np.random.triangular(-20,-10,0), lambda : np.random.triangular(-15, -7.5, 0)
    ,lambda : np.random.triangular(-5, -2, 0), lambda : np.random.triangular(0, 1, 5))
    precios = (78, 97, 120, 180)
    demandas = (175, 140, 115, 75)
    reacciones = (5, 2.5, 0.5, 0.01)
    habitaciones_existentes = (200, 200, 200, 100)
    cant_repeticiones = 1
    total_simulaciones = len(combinations) * cant_repeticiones
    multiplicidad = 0
    mejor_caso = 0
    for z in range(len(combinations)):
        j = combinations[z]
        ganancias = 0
        for k in range(0, cant_repeticiones):
            ganancia = 0
            for i in range(0, len(variaciones)):
                precio_variado = variaciones[i]()
                precio_total = precios[i] * (1 + precio_variado/100)
                variacion_demanda = reacciones[i] * (-precio_variado) / 100 + 1
                demanda_total = demandas[i] * variacion_demanda
                habitaciones_construidas = habitaciones_existentes[i] +  j[i]
                habitaciones_alquiladas = min(demanda_total, habitaciones_construidas)
                ganancia += habitaciones_alquiladas * precio_total
            ganancias += ganancia
        print("%d / %d" % ((z + 1) * cant_repeticiones, total_simulaciones) )
        if mejor_caso < ganancias / float(cant_repeticiones):
            mejor_caso = ganancias / float(cant_repeticiones)
            multiplicidad = j
    return multiplicidad, mejor_caso

partition_size = round(len(combinaciones_posibles) / 7)
print (partition_size)
threads = []
pool = Pool()
for i in range(0, 7):
    partition_start = partition_size * i
    partition_end = partition_size * (i + 1)
    threads.append(pool.apply_async(simulation, args=[combinaciones_posibles[partition_start: partition_end]]) )

combination = []
revenue = 0
for thread in threads:
    perm, profit = thread.get()
    if profit > revenue:
        revenue = profit
        combination = perm

print("%d Economico, %d Negocios, %d Ejecutiva, %d Premium,  %f Ganancia" %
    ( combination[0], combination[1], combination[2], combination[3] , revenue))