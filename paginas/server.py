#Módulo principal, actúa de servidor y atiende las peticiones entrantes

from bottle import route, run, get,static_file, redirect, request, response
import grupos
import threading

#Para devolver ficheros .css
@route('/<filename>.css')
def stylesheets(filename):
	with open(filename + '.css', 'r') as archivo:
		response.content_type = 'text/css;charset=utf-8'
		return archivo.read()

#Para devolver ficheros .js
@route('/<filename>.js')
def javascript(filename):
	with open(filename + '.js', 'r') as archivo:
		response.content_type = 'text/javascript;charset=utf-8'
		return archivo.read()

#Para devolver ficheros .png
@route('/datos/imagenes/<filename>.png')
def png(filename):
	response.content_type = 'image/png'
	return static_file("datos/imagenes/" + filename + ".png",
					   root=".",
					   mimetype='image/png')

#Para devolver ficheros .jpg
@route('/datos/imagenes/<filename>.jpg')
def jpg(filename):
	response.content_type = 'image/jpeg'
	return static_file("datos/imagenes/" + filename + ".jpg",
					   root=".",
					   mimetype='image/jpeg')

#Para devolver ficheros .gif
@route('/datos/imagenes/<filename>.gif')
def gif(filename):
	response.content_type = 'image/gif'
	return static_file("datos/imagenes/" + filename + ".gif",
					   root=".",
					   mimetype='image/gif')


#Para devolver el favicon
@get('/favicon.ico')
def get_favicon():
	response.content_type = 'image/x-icon'
	return static_file('favicon.ico', root='.')

#Método al que se llama cuando se accede a cualquier grupo
@route('/grupos/<nombre>')
def gruposIndex(nombre):

	#Hilo para calcular los grupos aleatorios
	cadenaResultadoAleatorio=[]
	tAleatorio = threading.Thread(target=grupos.aleatorioNum, args=(3,cadenaResultadoAleatorio,))
	tAleatorio.start()

	#Hilo para calcular los grupos para recomendar
	cadenaResultadoCookies=[]
	tCookies = threading.Thread(target=leeCookies, args=(request.get_header("Cookie"),cadenaResultadoCookies,nombre,))
	tCookies.start()

	pagina=""

	#Leemos el archivo grupos.html
	with open('grupos.html', 'r', encoding='utf-8') as inicio:
		pagina = pagina+inicio.read()


	#Insertamos el top de grupos
	pagina = pagina.replace("_Top_", grupos.top(0),1)

	#Insertamos la información sobre el grupo (nombre, biografía, imagen,...)
	pagina = grupos.info(nombre, pagina)

	tAleatorio.join()

	#Insertamos los grupos aleatorios
	pagina = pagina.replace("_Aleatorio_", cadenaResultadoAleatorio[0],1)

	tCookies.join()

	#Insertamos los grupos recomendados
	pagina = pagina.replace("_Recomendados_", cadenaResultadoCookies[0],1)

	return pagina

#Método al que se llama desde el frontend cada vez que se introducen cambios en
#la caja de búsqueda
@route('/buscar/<nombre>')
def busqueda(nombre):
	return grupos.busca(grupos.inverseReplaceName(nombre))

#Método al que se llamaría si no hay nada en la caja de texto
#No debería pasar ya que el código de Javascript previene esto,
#pero por si acaso
@route('/buscar/')
def noBusca():
	return ""

#Método al que se llama desde el frontend para obtener 3 nuevos grupos aleatorios
@route('/aleatorio')
def aleatorio():
	cadenaResultadoAleatorio=[]
	tAleatorio = threading.Thread(target=grupos.aleatorioNum, args=(3,cadenaResultadoAleatorio,))
	tAleatorio.start()
	tAleatorio.join()
	return cadenaResultadoAleatorio[0]

#Método al que se llama para obtener los 100 primeros grupos en el top
@route('/top')
def top():
	return grupos.top(1)

#Método para redirigir cualquier url errónea al inicio
@route("/<url:re:.+>")
def redir(url):
	redirect('/')

#Método para la página de inicio
@route('/')
def index():

	#Hilo para calcular los grupos aleatorios
	cadenaResultadoAleatorio=[]
	tAleatorio = threading.Thread(target=grupos.aleatorioNum, args=(3,cadenaResultadoAleatorio,))
	tAleatorio.start()

	#Hilo para calcular los grupos para recomendar
	cadenaResultadoCookies=[]
	tCookies = threading.Thread(target=leeCookies, args=(request.get_header("Cookie"),cadenaResultadoCookies,None,))
	tCookies.start()

	#Leemos el archivo index.html
	pagina=""
	with open('index.html', 'r', encoding='utf-8') as inicio:
		pagina = pagina+inicio.read()

	#Insertamos el top de grupos
	pagina = pagina.replace("_Top_", grupos.top(0),1)

	tAleatorio.join()

	#Insertamos los grupos aleatorios
	pagina = pagina.replace("_Aleatorio_", cadenaResultadoAleatorio[0],1)

	tCookies.join()

	#Insertamos los grupos recomendados
	pagina = pagina.replace("_Recomendados_", cadenaResultadoCookies[0],1)

	return pagina


#Método para leer las cookies de la petición y calcular los grupos recomendados
def leeCookies(cookies,cadenaResultado,grupoNuevo):
	listaGrupos = []
	apodo="Desconocido"

	#Buscamos la cookie 'visita', que es la que nos interesa
	if cookies is not None:
		for i in cookies.split(";"):
			if "visita" in i:
				#Obtenemos los grupos de esta cookie
				gruposCookies = i.split("=")[1].split("*TFG*")
				for j in gruposCookies:
					listaGrupos.append(j)

			elif "apodo" in i:
				apodo = i.split("=")[1]

	#En un hilo aparte, llamamos a la función de log
	threading.Thread(target=logGrupos, args=(listaGrupos,apodo,grupoNuevo,)).start()

	#Llamamos al módulo grupos para que procese esta información
	cadenaResultado.append(grupos.buscaRecomienda(listaGrupos, grupoNuevo))




#Método para ir guardando en un archivo los grupos que visitan los usuarios
def logGrupos(listaGrupos,apodo,grupoNuevo):

	cadenaGrupos=""

	#Construimos la cadena con los grupos ya visitados
	if len(listaGrupos) > 0:
		for i in listaGrupos:
			if i:
				cadenaGrupos = cadenaGrupos + "," + i

	#Añadimos el grupo nuevo a la cadena
	if grupoNuevo:
		cadenaGrupos = cadenaGrupos + "," + grupoNuevo

	#Escribimos la cadena en el archivo
	if cadenaGrupos:
		arGrupos = open("./logs/log.txt", "a", encoding='utf-8')
		#Escribimos la información en el archivo
		arGrupos.write("*" + apodo + ":" + cadenaGrupos[1:] + "-\n")
		arGrupos.close()


#Lanzamos el servidor en esta IP y puerto
run(host='localhost', port=8090)
