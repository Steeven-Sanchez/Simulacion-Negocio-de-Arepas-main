# -*- coding: utf-8 -*-
# Instalar https://simpy.readthedocs.io/en/latest/simpy_intro/installation.html
# Ejemplos https://simpy.readthedocs.io/en/latest/examples/index.html

#Steeven Sanchez Sepulveda

import random
import simpy
import numpy
import math
from random import randint

# Datos de la simulación  ## variables de entrada ___________________________________##
SEMILLA = 40  # Semilla generador
CLIENTES =  100 # Vamos a simular 10 clientes
Minutos_servicio =  8 * 60 # 8 horas de servicio en minutos


##esto nos dira el numero de arepas a vender 
n_no_compro = round(CLIENTES * 0.15)
n_arepa1 = round(CLIENTES * 0.35)
n_arepa2 = round(CLIENTES * 0.25)
n_arepa3 = round(CLIENTES * 0.25)

#crearemos estas copias para los desempeños al final 
a1= n_arepa1
a2 = n_arepa2
a3 = n_arepa3
no =n_no_compro

print ("**********************  numero de arepas que se deberian vender segun porcentajes  *******************")

print ("no compran = " ,n_no_compro)
print ("arepa con todo = ", n_arepa1)
print ("arepa de bebé = ", n_arepa2)
print ("arepa de morcilla = ", n_arepa3)
print ("total = ", n_arepa1+ n_arepa2+ n_arepa3+n_no_compro)       
##_________________________________________________________________________##

# Variables de estado
COLA = 0
tiempo_acumulado = 0

# Variables desempeño

MAX_COLA = 0
ESPERA_CLIENTES = numpy.array([])
max_arepa1 = 0

tiempo_llegada_acumulada = 0  # saber cuanto tiempo se lleva atendiendo
atendiendo = True
tiempo_atencion_acumulada = 0
TIEMPO_PROMEDIO_ATENCION= numpy.array([])


#EN EL INFORME SE EXPLICARA CADA FUNCION DE MANERA GENERAL.



#funcion arepas que recibe por parametros un numero aleatorio entre 0 y 3
# 0 para clientes que no compran
# 1 para arepa1 que son las arepas con todo
# 2 para arepa 2 que es la arepa de morcilla
# 3 para arepa 3 que en la arepa de bebé

def arepas(x):
    #retronaremos un diccionario con el tipo de arepa y el timpo que usa esta arepa
    #para ser preparada . ademas retorna el numero que recibe .
    

    if (x == 0) : 
        t_no_compro = round(10 * (1 - math.exp((- 1 * (random.uniform(0, 1))))))
        return {'compro': "no compro", 'tiempo_atencion': t_no_compro, 'arepa': x}
        


    elif (x == 1):
        t_arepa1 = round(random.uniform(5, 8))
        return {'compro': "compro arepa con todo ", 'tiempo_atencion': t_arepa1, 'arepa': x}
        

    elif (x == 2) :
        t_arepa2 = round(10 * (1 - math.exp((- 4 * (random.uniform(0, 1))))))
        return {'compro': "compro arepa de morcilla ", 'tiempo_atencion': t_arepa2, 'arepa': x}
        

    elif (x == 3) :
        t_arepa3 = round(random.uniform(3, 5))
        return {'compro': "compro arepa de bebé ", 'tiempo_atencion': t_arepa3, 'arepa': x}
        


def llegada(env, numero, contador):
    for i in range(numero):
        c = cliente(env, 'Cliente %02d' % i, contador, i)
        env.process(c)
        
        tiempo_llegada = (
            round(10 * (1 - math.exp((- 4 * (random.uniform(0, 1)))))))  # distribucion exponencial con media 4
        yield env.timeout(tiempo_llegada)  # Yield retorna un objeto iterable
    






def cliente(env, nombre, servidor, i):
    # El cliente llega y se va cuando es atendido
    llegada = env.now

    global COLA
    global MAX_COLA
    global ESPERA_CLIENTES
    global max_arepa1
    global tiempo_llegada_acumulada  #
    global atendiendo  #
    global tiempo_atencion_acumulada  #
    global ultimo_cliente
    global aux
    global TIEMPO_PROMEDIO_ATENCION
    global n_no_compro
    global n_arepa1
    global n_arepa2
    global n_arepa3

    tiempo_llegada_acumulada = llegada  #
    # Atendemos a los clientes (retorno del yield)
    # With ejecuta un iterador sin importar si hay excepciones o no

    # *
    if (atendiendo): #siempre entra al if 
        print ()
        if (tiempo_llegada_acumulada <= Minutos_servicio): # este if controla la entrada de los clientes
            #para que no se ingresen mas clientes al cerrar el negocio 
        
            print('%7.2f' % (llegada), "minutos  Llega ", nombre)
            ultimo_cliente = i + 1
            max_arepa1 += 1

            COLA += 1
            if COLA > MAX_COLA:
                MAX_COLA = COLA
        else:
            print ("*******************      CIERRAN NEGOCIO PERO SIGUEN ATENDIENDO LOS QUE FALTAN  ********************************")
            print ()
            atendiendo = False
            
        ##codigo reusado .... con modificaciones     
        with servidor.request() as req:

                # Hacemos la espera hasta que sea atendido el cliente

                # print("Tamaño cola", COLA)
                results = yield req
                COLA = COLA - 1
                espera = env.now - llegada
                ESPERA_CLIENTES = numpy.append(ESPERA_CLIENTES, espera)

                #se genera el aleatorio para el tipo de arepa 
                tipo_de_arepa = randint(0, 3)
                boleano= True

                #este bucle garantiza que sea valido el numero del tipo de arepa
                #si el numero de arepa ya fue vendida en su totalidad, genere otra hasat que sea valido 
                while boleano :

                            if (tipo_de_arepa == 0 )  and  ( n_no_compro !=0 ):
                                n_no_compro -= 1 
                                tipo_de_arepa = 0
                                boleano =False 
                            elif (tipo_de_arepa == 1 ) and  ( n_arepa1 != 0):
                                n_arepa1 -=1
                                tipo_de_arepa = 1
                                boleano =False
                            elif (tipo_de_arepa == 2 ) and  ( n_arepa2 != 0):
                                n_arepa2 -=1
                                tipo_de_arepa = 2
                                boleano =False 
                            elif (tipo_de_arepa == 3 ) and  ( n_arepa3 != 0):
                                n_arepa3 -=1
                                tipo_de_arepa = 3
                                boleano =False 
                            else :
                                 tipo_de_arepa = randint(0, 3)
                                 boleano= True

                ##llamamos a la funcion arepas y se le envia el numero valido
                # arepa = (es asignado el numero que retorna la funcion para volverlo a usar )                 
                arepa = arepas(tipo_de_arepa)['arepa']
                tiempo_atencion = arepas(arepa)['tiempo_atencion']
                
                TIEMPO_PROMEDIO_ATENCION = numpy.append(TIEMPO_PROMEDIO_ATENCION, tiempo_atencion )
                arepa_comprada = arepas(arepa)['compro']

                
                print('%7.2f' % (env.now), nombre, ", espero a ser atendido : ", espera, "min, ", arepa_comprada,
                                      "  y es atendido ", tiempo_atencion, "min ")
                
                # guardara el tiempo que se lleva atendiendo, esto para saber si el negocio ya cerro 
                tiempo_atencion_acumulada = tiempo_atencion_acumulada + tiempo_atencion

                yield env.timeout(tiempo_atencion)
                print('%7.2f' % (env.now), " Sale", nombre)
        

#funcion para saber el tiempo que el empleado ha atendido despues de cerrar.
#                
def t_empleado(numero, boleano):
    if (numero > 0) and boleano:
        return numero 
    
    elif (numero > 0) and (boleano == False):
        return numero
      
    else:
         return 0


# Inicio de la simulación

print(
    "**************************************             AREPERIA :V       ************************************************")
random.seed(SEMILLA)
env = simpy.Environment()

# Inicio del proceso y ejecución
servidor = simpy.Resource(env, capacity=1)
env.process(llegada(env, CLIENTES, servidor))  #
env.run()
print ()
print("TERMINA JORNADA DE TRABAJO")
print()
print(
    "**************************************             DESEMPEÑO       ************************************************")
# print("Tiempo de llegada  acumulada  = ", tiempo_llegada_acumulada,"minutos " )
print("Cola máxima que se formo =", MAX_COLA)
print("Tiempo promedio que espera el cliente en la cola = ", '%7.2f' % (numpy.mean(ESPERA_CLIENTES)), "minutos ")
print("Tiempo promedio que espera el cliente siendo atendidos  = ", '%7.2f' % (numpy.mean(TIEMPO_PROMEDIO_ATENCION)), "minutos ")
print("Tiempo Total que atendio el empleado = ", tiempo_atencion_acumulada, "minutos ")  #
print(
"Tiempo Total que el empleado estuvo desocupado  = ", t_empleado(Minutos_servicio - tiempo_atencion_acumulada, True),
"minutos ")  #
print("Tiempo  que el empleado trabajo de más  = ", t_empleado(   tiempo_atencion_acumulada - Minutos_servicio  , False),
      "minutos ")
print("Clientes atendidos   = ", ultimo_cliente)  #
print("Clientes NO atendidos   = ", CLIENTES - ultimo_cliente)  #
print ("Arepas con todo  vendidas = ", n_arepa1 , ". utilidad perdida= " ,  n_arepa1*750)
print ("Arepas de bebé  vendidas = ", n_arepa2 , ". utilidad perdida= " , n_arepa2*550 )
print ("Arepas con morcilla   vendidas = ",  n_arepa3 , ". utilidad perdida  = " ,   n_arepa3*500)
print ("UTILIDAD TOTAL  = ",  n_arepa1*750  + n_arepa2*550  +   n_arepa3*500)
print ("Arepas con todo  NO vendidas = ", a1- n_arepa1 , ". utilidad perdida= " , (a1- n_arepa1)*750)
print ("Arepas de bebé NO vendidas = ", a2- n_arepa2 , ". utilidad perdida= " , (a2- n_arepa2)*550 )
print ("Arepas con morcilla  NO vendidas = ", a3- n_arepa3 , ". utilidad perdida  = " ,  (a3- n_arepa3)*500)
print ("UTILIDAD TOTAL QUE NO SE GANO = ", (a1- n_arepa1)*750  + (a2- n_arepa2)*550  +  (a3- n_arepa3)*500)


