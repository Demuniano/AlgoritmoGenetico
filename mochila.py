## CREADO Versión inicial NDD Sept 2020
## Modificaciones posteriores

import random
import numpy as np

#### Parametros #####
x=4  #numero de variables de decision - Elementos diferentes: x
n=4  #numero de individuos en la poblacion - cromosomas: n
Pcruce=0.98  #Probabilidad de Cruce
Pmuta=0.1   #Probabilidad de Mutación

"""   Comentarios son Una Linea: #
O triple comilla doble: Un bloque"""


# Ingresar los datos del Problema de la Mochila - Peso y Utilidad de los Elementos
pesos = [7, 6, 8, 2]
utilidad = [4, 5, 6, 3]
# cromosoma1 = [0, 1, 0, 1]
# cromosoma2 = [1, 0, 0, 0]
# cromosoma3 = [0, 0, 0, 1]
# cromosoma4 = [0, 1, 1, 0]
# poblInicial = np.array([cromosoma1, cromosoma2, cromosoma3, cromosoma4])
poblInicial = np.zeros((n, x), dtype=int)



# MEJORA: Tamaño de la Población como parametro 
#random.seed(1)
#print("\n","aletorio:", random.randrange(2)) #Entero 0 o 1

##### FUNCIONES PARA OPERADORES


def evalua(n, x, poblIt, utilidad, pesos):
    suma = 0
    pesoTemp = 0
    total = 0
    for i in range(0, n):
        for j in range(0, x):
            suma += poblIt[i, j] * utilidad[j]
            pesoTemp += poblIt[i, j] * pesos[j]

        fitness[i] = suma
        pesosIndividuos[i] = pesoTemp
        total += suma
        suma = 0
        pesoTemp = 0  
    return fitness, pesosIndividuos, total
def evaluarHijo(hijo, pesos):
    valido = True
    pesoTemp = 0
    for j in range(0, x):
        pesoTemp += hijo[j] * pesos[j]
    if pesoTemp > 15:
      valido = False
    return valido
def imprime(n,total,fitness,pesosIndividuos,poblIt):
    print("------------------------------------")
    #Tabla de evaluación de la Población
    acumula=0
    print ("\n",'Tabla Iteración:',"\n")
    for i in range(0, n):
      probab=fitness[i]/total
      acumula+=probab
      print(f"{i+1} {' ' * 3} {poblIt[i]} {' ' * 3} {fitness[i]} {' ' * 3} {pesosIndividuos[i]} {' ' * 3} {probab:.3f} {' ' * 3} {acumula:.3f}")

      acumulado[i]=acumula
    print("Total Fitness:      ", total)
    return acumulado

def seleccion(acumulado):
    escoje=np.random.rand()
    print("escoje:      ", escoje)
    
    for i in range(0,n):
      if acumulado[i]>escoje:
         padre=poblIt[i]
         break
    return (padre)
    
    

def cruce(a1,p1,p2,puntoCorte):
    if a1 < Pcruce:
        print("Más pequeño", Pcruce, "que", a1, "-> Si cruzan")
        print("Punto de Cruce: ", puntoCorte)

        temp1 = p1[:puntoCorte]
        temp2 = p1[puntoCorte:]
        temp3 = p2[:puntoCorte]
        temp4 = p2[puntoCorte:]
        hijo1 = np.concatenate((temp1, temp4))
        hijo2 = np.concatenate((temp3, temp2))

        print(temp1, temp2)
        print(temp3, temp4)
        print(hijo1, hijo2)
        hijo1 = mutacion(hijo1, Pmuta)
        hijo2 = mutacion(hijo2, Pmuta)
        valh1 = evaluarHijo(hijo1, pesos)
        valh2 = evaluarHijo(hijo2, pesos)
        if valh1 and valh2:
            print("Ambos hijos validos")
            return hijo1, hijo2
        elif valh1:
            print("Hijo 2 no valido")
            return hijo1, [-1]
        elif valh2:
            print("Hijo 1 no valido")
            return [-1], hijo2
        else:
            print("Ambos hijos no validos")
            return [-1], [-1]
    else:
        print("Mayor", Pcruce, "que ", a1, "-> NO Cruzan")
        hijo1 = p1
        hijo2 = p2
        return hijo1, hijo2
        

    # else:
    #   print("Mayor", Pcruce, "que ", a1, "-> NO Cruzan")
    #   hijo1=p1
    #   hijo2=p2
    
    # return hijo1,hijo2

def mutacion(hijo, Pmuta):
    for i in range(0, x):
        mutaBite = np.random.rand()
        if mutaBite < Pmuta:
            #print("Muta en el bit: ", i)
            if hijo[i] == 0:
                hijo[i] = 1
            else:
                hijo[i] = 0
    return hijo
def convergenciaMejorInd(pesosIndividuos, mejor_aptitud_anterior, iter_sin_mejora):
    mejor_aptitud_actual = np.max(pesosIndividuos)
    if mejor_aptitud_actual > mejor_aptitud_anterior:  
        iter_sin_mejora = 0
    else:
        iter_sin_mejora += 1

    return iter_sin_mejora

#generar la población inicial de forma aleatoria
ind = 0
while ind<n:    
    cromosoma = [random.randint(0, 1) for i in range(4)]
    if evaluarHijo(cromosoma, pesos):
        poblInicial[ind]=cromosoma
        ind += 1

fitness= np.empty((n))
pesosIndividuos = np.empty((n))
acumulado= np.empty((n))
suma=0
total=0

#Individuos, soluciones o cromosomas 
#poblInicial = np.random.randint(0, 2, (n, x)) # aleatorios (n por x) enteros entre [0 y2)
#random.random((4,5)) # 4 individuos 5 genes

#pesos = [5, 7, 10, 30, 25]
#utilidad = [10, 20, 15, 30,15]

print("Poblacion inicial Aleatoria:","\n", poblInicial)
print("\n","Utilidad:", utilidad) 
print("\n","Pesos", pesos )   
poblIt=poblInicial

######  FIN DE LOS DATOS INICIALES



##Llama función evalua, para calcular el fitness de cada individuo
fitness,pesosIndividuos,total=evalua(n,x,poblIt,utilidad,pesos)
#####print("\n","Funcion Fitness por individuos",  fitness)
#####print("\n","Suma fitness: ",  total)

##### imprime la tabla de la iteracion
imprime(n,total,fitness,pesosIndividuos,poblIt)

##### ***************************************

max_iter_sin_mejora = 10
iter_sin_mejora = 0
mejor_aptitud_anterior = float('-inf')
# Inicia Iteraciones
# Crear vector de 5x2 vacio  a = numpy.zeros(shape=(5,2))
for iter in range(100):
    poblacion = 0
    print("\n","----------Iteración ", iter+1,"----------")
    pobTemo = np.zeros((n, x), dtype=int)
    while poblacion < n:
        for i in [0,2]:  ## Para el bloque de 2 hijos cada vez
            papa1=seleccion(acumulado) # Padre 1
            print("padre 1:", papa1)
            papa2=seleccion(acumulado) # Padre 2
            print("padre 2:", papa2)

            hijoA,hijoB=cruce(np.random.rand(),papa1,papa2,np.random.randint(1, x - 1))
            if (hijoA[0]!=-1)  and poblacion < n:
                poblacion += 1
                pobTemo[i]=hijoA
            if (hijoB[0]!=-1) and poblacion < n: 
                poblacion += 1  
                pobTemo[i+1]=hijoB
    poblIt=pobTemo

    
    print("\n","Poblacion Iteración ", iter+1,"\n", poblIt)
    fitness,pesosIndividuos,total=evalua(n,x,poblIt,utilidad,pesos)
    #### print("\n","Funcion Fitness por individuos",  fitness)
    #### print("\n","Suma fitness: ",  total)

    ##### imprime la tabla de la iteracion
    imprime(n,total,fitness,pesosIndividuos,poblIt)
    iter_sin_mejora=convergenciaMejorInd(pesosIndividuos, mejor_aptitud_anterior, iter_sin_mejora)
    if iter_sin_mejora >= max_iter_sin_mejora:
            print("El algoritmo ha convergido. Terminando las iteraciones.")
            break
    else:
        mejor_aptitud_anterior = np.max(pesosIndividuos)
