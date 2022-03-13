# -*- coding: utf-8 -*-
#Programa para pedir los grupos más escuchados de cada usuario

import requests
#from requests.auth import HTTPBasicAuth
#import json
import time
import datetime
import sys
import traceback



#API <CODE>

#Obtenemos los usuarios guardados
#y los guardamos en este array
usuarios = []

arUsu = open("usuarios.txt","r")
textUsu = arUsu.read()
arUsu.close()
usuario=""
for i in textUsu:
	if(i=='\n'):
		usuarios.append(usuario[1:])
		usuario=""
	else:
		usuario=usuario+i

usuarios.append(usuario)



#Obtenemos los usuarios con error
arErr = open("usuErr.txt","r")
textErr = arErr.read()
arErr.close()

#Obtenemos los grupos guardados
grupos = []

arGru = open("grupos.txt","r")
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



arGruUsu = open("gruposUsu.txt","r")
textGruUsu =arGruUsu.read()
arGruUsu.close()

#Para guardar las relaciones usuarios-grupos
arGruUsu = open("gruposUsu.txt","a")

#Para guardar los grupos
arGru = open("grupos.txt","a")

#Archivo para guardar a los usuarios cuyos grupos hayan dado error
arErr = open("usuErr.txt", "a")

cont=0
contErr=0

#Por si surge algun error
try:
	#Para cada usuario guardado
	for usuario in usuarios:
		cont+=1
		cadena = "-Usuario: " + usuario
		#Para ir viendo en consola la ejecucion
		#print("-----------------------------------------------------")
		#print("Hora: " + str(datetime.datetime.now().time()))
		#print("Repetido: " + str(sys.argv[1]))
		#print("Usuario: " + usuario)
		#print("Numero: " + str(cont))
		#print("Errores: " + str(contErr))

		#Si no se ha escrito ya y no tiene error
		if cadena not in textGruUsu and usuario not in textErr:
			#Esperamos lo minimo posible para que la API no de error
			time.sleep(0.7)
			r = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=' + usuario + '&limit=10&api_key=<CODE>&period=overall&format=json')

			#Si respuesta correcta
			if 'topartists' in r.json():
				texto = "*"
				añadidosGru=0
				añadidosGruUsu=0

				#Por cada artista devuelto
				for artist in r.json()['topartists']['artist']:
					if 'name' in artist:
						nombre = artist['name']

						#Si no tenemos guardado el grupo, lo guardamos
						if nombre not in grupos:
							añadidosGru+=1
							grupos.append(nombre)
							try:
								arGru.write("-" + nombre + "\n")
							except (UnicodeEncodeError):
								pass

						#Para añadir la coma
						if(texto!="*"):
							texto = texto + ","

						#Añadimos el grupo al texto del usuario
						añadidosGruUsu+=1
						texto=texto + nombre

				#Añadimos los grupos al archivo de relaciones
				if(añadidosGruUsu >0):
					try:
						arGruUsu.write(cadena + texto + "\n")
					except (UnicodeEncodeError):
						contErr+=1
						arErr.write("-" + usuario + "\n")

				#Para ver en consola
				print("Añadidos archivo grupos: " + str(añadidosGru))
				print("Añadidos archivo gruUsu: " + str(añadidosGruUsu))

			#Error en peticion
			else:
				print("Error")


			#Hacemos flush a los archivos
			arGruUsu.flush()
			arGru.flush()
			arErr.flush()

		#Si ya se ha escrito antes el usuario
		else:
			print("Ya esta")

	#Cerramos los archivos
	arGru.close()
	arGruUsu.close()

#Si surge algun error
except:
	traceback.print_exc()
	arGruUsu.flush()
	arErr.flush()
	arGru.flush()
	arGru.close()
	arErr.close()
	arGruUsu.close()

#subprocess.call("procesar.py", shell=True)
