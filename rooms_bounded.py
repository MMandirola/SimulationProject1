import numpy as np
import csv
# Variables de entrada
variaciones = (lambda : np.random.triangular(-20,-10,0), lambda : np.random.triangular(-15, -7.5, 0)
,lambda : np.random.triangular(-5, -2, 0), lambda : np.random.triangular(0, 1, 5))

# Variables de decision

grado_de_multiplicidad = range(0, 12)

# Parametros

precios = (78, 97, 120, 180)

demandas = (175, 140, 115, 75)

reacciones = (5, 2.5, 0.5, 0.01)

proporciones = (2, 2, 2, 1)

habitaciones_existentes = (200, 200, 200, 100)

cant_repeticiones = 100000

#Calculo de la ganancia
multiplicidad = 0
mejor_caso = 0
data = []
# para cada valor que puede tomar la variable de decision
for j in grado_de_multiplicidad:
    ganancias = []
    # Simulo k repeticiones de la simulacion
    for k in range(0, cant_repeticiones):
        ganancia = 0
        # Para cada uno de los tipos de casas
        for i in range(0, len(variaciones)):
            #Instancio la variable aleatoria
            precio_variado = variaciones[i]()
            #Calculo la ganancia de esa corrida
            precio_total = precios[i] * (1 + precio_variado/100)
            variacion_demanda = reacciones[i] * (-precio_variado) / 100 + 1
            demanda_total = demandas[i] * variacion_demanda
            habitaciones_construidas = habitaciones_existentes[i] + j * proporciones[i]
            habitaciones_alquiladas = min(demanda_total, habitaciones_construidas)
            ganancia += habitaciones_alquiladas * precio_total
        ganancias.append(ganancia)
    # Calculo media y varianza de las corridas
    p = np.mean(ganancias)
    v = np.var(ganancias)
    data.append([str(p), str(v), str(j)])
    # Me quedo con la mejor ganancia y multiplicidad
    if mejor_caso < p:
        mejor_caso = p
        multiplicidad = j

# Guardo los datos en un csv
with open('data-bounded.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in data:
        spamwriter.writerow(row)

# imporimo la mejor solucion
print("%d Economico, %d Negocios, %d Ejecutiva, %d Premium,  %f Ganancia" %
    ( multiplicidad * proporciones[0], multiplicidad * proporciones[1], multiplicidad * proporciones[2], multiplicidad * proporciones[3] , mejor_caso))

            
    




