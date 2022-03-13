#Módulo para procesar todo lo relacionado con grupos

from random import randint
import peticion
import recom

#Array donde se van a guardar todos los grupos
grupos = []

#Leemos y guardamos los grupos
arGru = open("./datos/gruProc.txt","r")
textGru = arGru.read()
arGru.close()
grupo = ""
for i in textGru:
	if(i=='\n'):
		grupos.append(grupo[1:])
		grupo=""
	else:
		grupo=grupo+i

if(len(grupos) > 0 and grupos[-1] != grupo):
	grupos.append(grupo)

#Array donde se van a guardar todos los grupos
gruposTop = []

#Leemos y guardamos los grupos
arGruTop = open("./datos/gruOrd.txt","r")
textGruTop = arGruTop.read()
arGruTop.close()
grupo = ""
for i in textGruTop:
	if(i=='\n'):
		gruposTop.append(grupo[1:])
		grupo=""
	else:
		grupo=grupo+i

if(len(gruposTop) > 0 and gruposTop[-1] != grupo):
	gruposTop.append(grupo)

#Cadena con el top 3 de los grupos
cadenaTop3 = ""

#Método para generar num grupos aleatorios
def aleatorioNum(num,cadenaResultadoAleatorio):
	cadena=""
	for i in range(0,num):
		grup = grupos[randint(0,len(grupos))]

		if "<" not in grup and ">" not in grup:
			cadena = cadena + "<a href='/grupos/" + grup + "' class='link'>" + grup + "</a><br><img src=" + \
			peticion.buscaImagen(grup) + " class='aleaImg'  alt='Group Image'><br>"
		else:
			i-=1

	cadenaResultadoAleatorio.append(cadena)

#Método al que se llama cuando buscamos un grupo en la caja de búsqueda
def busca(nombre):
	lista=[]
	for i in range(0,len(gruposTop)):
		if (gruposTop[i].lower().startswith(nombre.lower()) or nombre.lower() in gruposTop[i].lower()):
			lista.append(gruposTop[i])

		#Devolvemos los 5 primeros
		if len(lista) == 5:
			break

	cadenaBusca=""

	#Procesamos el resultado
	for j in range(0,min(5,len(lista))):
		cadenaBusca= cadenaBusca + "<li><a href='/grupos/"+ replaceName(lista[j]) + "' class='link'>" + lista[j] + "</a></li>"

	if(len(lista)==0):
		cadenaBusca="<li>No se ha encontrado ningún grupo</li>"

	return cadenaBusca

#Método que nos devuelve los primeros grupos en la lista (ordenados)
#num = 0 -> 3 primeros
#num > 0, Se devuelven en saltos de 100, identificando la página deseada
def top(num):
	cadenaTop=""

	global cadenaTop3

	if num == 0:
		#El top 3 solo lo calculamos 1 vez
		if cadenaTop3 == "":
			for i in range(0,3):
				cadenaTop = cadenaTop + "#" + str(i+1) + ": <a href='/grupos/" + \
				replaceName(gruposTop[i]) + "' class='link' >" + gruposTop[i] + "</a><br><img src=" + \
				peticion.buscaImagen(gruposTop[i]) + " class='topImg' alt='Group Image'><br>"
				cadenaTop3 = cadenaTop
		else:
			cadenaTop = cadenaTop3
	else:
		for i in range((num-1)*100,num*100):
			cadenaTop = cadenaTop + "#" + str(i+1) + ": <a href='/grupos/" + \
			replaceName(gruposTop[i]) + "' class='link' >" + gruposTop[i] + "</a><br><img src=" + \
			peticion.buscaImagen(gruposTop[i]) + " class='topImg' alt='Group Image'><br>"
	return cadenaTop

#Comprueba si un grupo existe
def exists(nombre):
	if nombre in grupos:
		return True
	else:
		return False

#Nos sirve para enviar datos a la página y que se muestren bien,
#procesándolos en el frontend con javascript
def replaceName(name):
	return name.replace("'","%TFGComa").replace("/","%TFGBarra").replace("?","%TFGPregunta").replace(".","%TFGPunto")

#Igual que el método anterior pero a la inversa
def inverseReplaceName(name):
	return name.replace("%TFGComa","'").replace("%TFGBarra","/").replace("%TFGPregunta","?").replace("%TFGPunto",".")

#Método para usar la red neuronal
#Recibe la lista de grupos visitados por el usuario y devuelve
#Una cadena conteniendo los grupos recomendados
def buscaRecomienda(lista,grupo):
	listaNumeros = []

	if grupo is not None:
		#Añadimos el grupo que estamos visitando a la lista
		nombreBien = inverseReplaceName(grupo)
		lista.append(nombreBien)

	#Transformamos los nombres de los grupos en índices
	for i in lista:
		if i in grupos:
			listaNumeros.append(grupos.index(i))
		else:
			flag = True
			j=0
			while (j < len(grupos)) and flag:
				gr = grupos[j]
				if (i in gr) or (gr in i):
					flag=False
					listaNumeros.append(grupos.index(gr))
				j +=1

	#Llamamos a la red neuronal
	gruposRec = recom.recomendar(listaNumeros)

	cadena=""

	#Procesamos el resultado de la red
	#Solo nos quedamos con los 3 primeros que no estén en la lista
	#que ya le pasamos a la red
	contador = 0
	for i in gruposRec:
		if (i not in listaNumeros) and contador < 3:
			contador+=1
			cadena = cadena + "<a href='/grupos/" + grupos[i] + "' class='link' >" + \
			grupos[i] + "</a><br><img src=" + peticion.buscaImagen(grupos[i]) \
			+ " class='recImg' alt='Group Image'><br>"

	return cadena

#Método para incluir nombre, foto e información sobre el grupo en la página
def info(nombre, pagina):
	nombreBien = inverseReplaceName(nombre)

	titulo = "<h1 id='nombreGrupo'>_Nombre_</h1>"

	if exists(nombreBien):
		info = peticion.info(nombreBien)

		if info is None:
			result = pagina.replace("_Nombre_","Este grupo no existe",1).replace("_Info_",titulo.replace("_Nombre_","Este grupo no existe",1),1)
		else:
			result = pagina.replace("_Nombre_",nombreBien,1).replace("_Info_",titulo.replace("_Nombre_",nombreBien,1) + info,1)
	else:
		result = pagina.replace("_Nombre_","Este grupo no existe",1).replace("_Info_",titulo.replace("_Nombre_","Este grupo no existe",1),1)

	return result
