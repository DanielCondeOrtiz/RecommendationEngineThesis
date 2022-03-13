#Programa para pedir y guardar los amigos de los usuarios
import requests
#from requests.auth import HTTPBasicAuth
import time


#Codigo de la api
#API <CODE>

#Obtenemos los usuarios guardados
usuarios = []

arUsu = open("usuarios.txt","r")
textUsu = arUsu.read()
arUsu.close()
usuario=""

#Leemos el archivo
for i in textUsu:
    if(i=='\n'):
        usuarios.append(usuario[1:])
        usuario=""
    else:
        usuario=usuario+i

usuarios.append(usuario)


textUsu=""

#Archivo donde escribir a los usuarios
arUsu = open("usuarios.txt","a")

#Logs de lo que se va leyendo
arAmi = open("amigos.txt","r")
textAmi =arAmi.read()
arAmi.close()

#Para escribir nuevos logs
arAmi = open("amigos.txt","a")

#Por si surgen excepciones
try:
    #Para cada usuario guardado
    for usuario in usuarios:
        #Para log
        cadenaFin = "-Fin usuario: " + usuario
        print(usuario)
        añadidos =0

        #Si no se ha hecho ya este usuario
        if cadenaFin not in textAmi:
            #Esperamos 1 segundo por limite de la API y hacemos la peticion
            time.sleep(1)
            r = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.getfriends&user=' + usuario + '&limit=500&api_key=<CODE>&period=overall&format=json')

            #Si respuesta es correcta
            if 'friends' in r.json():
                peticion = r.json()['friends']

                #Total de paginas en la peticion
                pagtotal = int(peticion['@attr']['totalPages'])

                #Por cada pagina
                for i in range(1,pagtotal +1):
                    print("Pag " + str(i) + "/" + str(pagtotal))

                    #Para cada amigo
                    for user in peticion['user']:

                        if 'name' in user:

                            #Si ese amigo no está escrito en el fichero, lo escribimos
                            nombre = user['name']
                            if nombre not in usuarios:
                                usuarios.append(nombre)
                                arUsu.write("-" + nombre + "\n")
                                añadidos+= 1

                    #Hacemos la peticion para la siguiente pagina
                    num=i+1
                    if(num <= pagtotal):
                        time.sleep(1)
                        r = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.getfriends&user=' + usuario + '&limit=500&api_key=<CODE>&period=overall&page=' + str(num) + '&format=json')
            else:
                print("Error")

            #Escribimos en los ficheros
            arAmi.write("Añadidos: " + str(añadidos) + "\n")
            print("Añadidos: " + str(añadidos))
            arAmi.write(cadenaFin + "\n")
        else:
            print("Ya está")

        arAmi.flush()
        arUsu.flush()

#Si surge alguna excepcion, pasaremos al siguiente usuario
except:
    print("Error")
