#Programa para ordenar los grupos segun el numero de personas que los escuchen
#Sirve para hacer el Top y búsqueda de la web

#Guardamos los grupos en un array
arGru = open("gruProc.txt","r")
textGru = arGru.read()
arGru.close()
grupos = []
grupo = ""
for i in textGru:
	if(i=='\n'):
		grupos.append(grupo[1:])
		grupo=""
	else:
		grupo=grupo+i

if(len(grupos) > 0 and grupos[-1] != grupo):
	grupos.append(grupo)

#Leemos el archivo que tiene la relacion usuarios - grupos
arProc = open("arProc.txt","r")
textProc = arProc.read()
arProc.close()

#Contamos el numero de veces que aparece cada grupo
arrayVeces=[]
for i in range(0,len(grupos)):
	texto1="," + str(i + 1) + ","
	texto2="-" + str(i + 1) + ","
	texto3="," + str(i + 1) + "-"

	arrayVeces.append(textProc.count(texto1) + textProc.count(texto2) + textProc.count(texto3))
	if not i%1000:
		print(i)

#Ordenamos el array de mayor a menor en un nuevo array
arrayVeces2 = list(arrayVeces)
arrayVeces2.sort(key=None, reverse=True)

#Archivo donde se guardaran los grupos ordenados
arGruOrd = open("gruOrd.txt","w")

#Archivo donde se guardan estadisticas sobre esta ordenacion
gruOrdDat = open("gruOrdDat.txt","w")

numAnterior = 0

#Por cada grupo
for j in range(0,len(arrayVeces2)):

	#Varios grupos pueden aparecer el mismo numero de veces,
	#Solo se lee la primera ves y se escriben todos de golpe
	if arrayVeces2[j] != numAnterior:
		numAnterior=arrayVeces2[j]

		#Indices de los grupos que aparecen las mismas veces
		indices = [h for h, x in enumerate(arrayVeces) if x == arrayVeces2[j]]
		cuenta = len(indices);
		print("Num: " + str(j) + ", cuenta: " + str(cuenta))

		#Escribimos cada grupo
		for k in range(0,cuenta):
			arGruOrd.write("-" + grupos[indices[k]] + "\n")
			gruOrdDat.write("-" + grupos[indices[k]] + "**" + arrayVeces2[j] + "\n")
			
		arGruOrd.flush()
		gruOrdDat.flush()

arGruOrd.close()
gruOrdDat.close()
