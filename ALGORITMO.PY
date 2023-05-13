import threading
import time
import random

datos = []
MAX_DATOS = 10

def productor_datos():
    while True:
        time.sleep(random.uniform(1.0, 3.0)) 
        nuevo_dato = random.randint(1, 100)
        

        with threading.Lock():
            if len(datos) < MAX_DATOS:
                datos.append(nuevo_dato)
                print("Nuevo dato producido:", nuevo_dato)
            else:
                print("No se pudo producir el dato. Almacenamiento lleno.")


def consumidor_datos():
    while True:
        time.sleep(random.uniform(2.0, 5.0))  
        
        with threading.Lock():
            if datos:
                dato_consumido = datos.pop(0)
                print("Dato consumido:", dato_consumido)
            else:
                print("No hay datos disponibles para consumir.")


hilo_productor_datos = threading.Thread(target=productor_datos)
hilo_consumidor_datos = threading.Thread(target=consumidor_datos)


hilo_productor_datos.start()
hilo_consumidor_datos.start()


hilo_productor_datos.join()
hilo_consumidor_datos.join()
