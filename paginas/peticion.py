#Módulo encargado de las peticiones a la api de LastFM
import requests

#Diccionario de python para guardar las url de las imágenes de los
#grupos que ya se haya hecho petición
dictGrupos = {}

#Método para, dado un grupo, buscar su imagen haciendo una petición a la API
def buscaImagen(group):

    result = None

    #Si ya hemos hecho la petición antes
    if group in dictGrupos:
        result = dictGrupos[group]
    #Si no se ha hehco la petición antes
    else:
        group = group.replace("+","%252B")
        r = requests.get('http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist='
         + group + '&api_key=<CODE>&period=overall&format=json'
          ).json()

        #Comprobamos si la respuesta contiene lo que necesitamos
        if 'artist' in r:
            for image in r['artist']['image']:
                #Nos quedamos con la imagen de tamaño mediano
                if(image['size'] == 'medium'):
                    if 'http' in image['#text']:
                        dictGrupos[group] = image['#text']
                        result = image['#text']

    #Si no hemos obtenido resultado válido, se pondría la imagen por defecto
    if result is None:
        result = './datos/imagenes/default.png'
    return result

#Método para incluir en la página la información del grupo proporcionado
#Devuelve la cadena a incluir
def info(group):
    result = None

    group = group.replace("+","%252B")
    #Hacemos la petición al servidor
    r = requests.get('http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist='
    + group + '&api_key=<CODE>&period=overall&format=json'
     ).json()

    #Si la respuesta es correcta
    if 'artist' in r:
        #Seleccionamos la imagen por defecto, que será la de mayor tamaño
        for image in r['artist']['image']:
            if(image['size'] == 'medium'):
                if 'http' in image['#text']:
                    #Lo hacemos itroduciendo un número aleatoriamente grande
                    result = "<br><img src=" + image['#text'].replace("/64s/","/80000/",1)\
                    + " class='groImg'  alt='Group Image'>" +"<br>"

        #Si no hemos obtenido imagen, ponemos la imagen por defecto
        if result is None:
            result = "<br><img src='./datos/imagenes/default.png' class='groImg'alt='Group Image'><br>"

        #Añadimos la biografía del artista
        if 'bio' in r['artist'] and r['artist']['bio']['content'] is not "":
            result = result + "<p id='bio'><strong>Biography: </strong>" +\
            r['artist']['bio']['summary'].replace("Read more on Last.fm","",1)

    #Si no hemos obtenido ningún resultado del servidor
    if result is None:
        result = "<br><img src='./datos/imagenes/default.png' class='groImg' alt='Group Image'><br>"

    #Grupo que se ha recibido del servidor pero que no es un grupo
    if "This is not an artist" in result:
        result=None

    return result
