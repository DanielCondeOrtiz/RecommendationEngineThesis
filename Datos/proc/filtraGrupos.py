#Archivo para filtrar aquellos grupos que no sean deseados
print("Procesando grupos")

#Leemos los grupos y los guardamos en un array
arGru = open("grupos.txt","r")
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

#Cadenas a evitar
evitar = ["www.", ".com", ".org", ".es", ".pl","de", ".se", ".kz", ".info", ".ru",\
".NL",".ORG",".IN",".HR", ".BR", "wWw.", "WWW.", ".COM", "Www.", ".in", ".cOm", "W w W .", ".ir",\
"w w w .", "WwW.", ".uk", ".US", ".net", ".fm", ".CoM", ".Com", "..."]

#Donde se van a guardar los grupos filtrados
arGruProc = open("gruProc.txt", "w")
gruposNuevos = []

#Por cada grupo
for i in range(0,len(grupos)):
	#True = bueno
	flag = True

	#Logs
	if not i%1000:
		print("Grupo numero: " + str(i))

	#Si ya lo hemos escrito
	for j  in range(0,len(gruposNuevos)):
		if grupos[i].lower() in gruposNuevos[j].lower() or gruposNuevos[j].lower() in grupos[i].lower():
			flag = False

	#Si contiene alguna cadena no deseada
	if "." in grupos[i]:
		for k in range(0,len(evitar)):
			if evitar[k] in grupos[i]:
				flag = False

	#Ests cadenas tampoco son deseadas
	if "<" in grupos[i] or ">" in grupos[i]:
		flag=False

	#Si ha pasado los filtros, los escribimos
	if flag:
		gruposNuevos.append(grupos[i])
		arGruProc.write("-" + grupos[i] + "\n")

arGruProc.close()
