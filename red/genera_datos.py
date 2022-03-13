import random

#Numero de datos
numGrupos = 93579
numUsu = 276083

#Archivo en el que vamos a guardar los datos
arProc = open("./datos/arProc_ale.txt", "w")

#Generamos 'numUsu' lineas diferentes
for i in range(numUsu):
    cadena=""

    #10 grupos en cada linea
    for j in range(10):
        cadena = cadena + "," + str(random.randint(0,numGrupos))

    #Escribimos en el fichero
    arProc.write("-" + cadena[1:] + "*\n")
    arProc.flush()

    if not i%10000:
        print("Escritos: " + str(i))

arProc.close()
