#Programa para convertir los grupos en numeros en el archivo de relaciones

#Leemos los grupos y los guardamos
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

#Leemos las relaciones
arGruUsu = open("gruposUsu.txt","r")
textGruUsu = arGruUsu.read()
arGruUsu.close()
gruposUsu = []
grupoUsu = ""
for i in textGruUsu:
	if(i=='\n'):
		gruposUsu.append(grupoUsu[1:])
		grupoUsu=""
	else:
		grupoUsu=grupoUsu+i

if(gruposUsu[-1] != grupoUsu):
	gruposUsu.append(grupoUsu)

#Archivo donde vamos a guardar
arProc = open("arProc.txt","w")

contUsu=0

print("Procesando")

#Por cada relacion
for linea in gruposUsu:
	contUsu+=1

	#Log
	if not contUsu%1000:
		print("Usuarios: " + str(contUsu))

	texto = "-"
	flagStart = 0
	grupo=""
	contGru=0

	#Parar de leer
	flagStop=False

	#Los grupos empiezan en el caracter *
	for i in linea:
		#Se detecta el caracter
		if(i=="*"):
			flagStart=1

		#Leemos
		if(flagStart==2 and not flagStop):
			#Fin de grupo
			if(i==","):
				try:
					#Si existe el grupo, lo guardamos
					if grupo in grupos:
						texto = texto + str(grupos.index(grupo) +1 ) + ","
						contGru+=1
						grupo=""
					else:
						#Si no hemos encontrado el grupo, probamos una busqueda mas profunda
						flagBucle = True
						for j in range(0,len(grupos)):
							if ((grupo.lower() in grupos[j].lower()) or (grupos[j].lower() in grupo.lower())) and flagBucle:
								texto = texto + str(j+1 ) + ","
								contGru+=1
								grupo=""
								flagBucle= False
				except:
					flagStop=True

			#Vamos guardando el grupo
			else:
				grupo = grupo+i


		#Empezamos a leer
		if(flagStart==1):
			flagStart=2


	#Para el ultimo grupo de cada linea
	try:
		#Si existe el grupo, lo guardamos
		if grupo in grupos:
			texto = texto + str(grupos.index(grupo) +1 ) + "*\n"
			contGru+=1
			grupo=""
		else:
			#Si no hemos encontrado el grupo, probamos una busqueda mas profunda
			flagBucle = True
			for j in range(0,len(grupos)):
				if ((grupo.lower() in grupos[j].lower()) or (grupos[j].lower() in grupo.lower())) and flagBucle:
					texto = texto + str(j+1 ) + "*\n"
					contGru+=1
					grupo=""
					flagBucle= False
	except:
		flagStop=True

	#Si no ha habido ningun error y hemos leido 10 grupos, escribimos
	if(not flagStop and contGru==10):
		arProc.write(texto)
		arProc.flush()

arProc.close()
