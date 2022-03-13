#Archivo para obtener una lista de los usuarios de los cuales
#aun no se ha hecho una petición
#Se guarda en Usuarios3.txt
arUsu = open("usuarios.txt","r")
textUsu = arUsu.read()
arUsu.close()
usuario=""
usuarios=[]
for i in textUsu:
	if(i=='\n'):
		usuarios.append(usuario[1:])
		usuario=""
	else:
		usuario=usuario+i

usuarios.append(usuario)

arGruUsu = open("gruposUsu.txt","r")
textGruUsu =arGruUsu.read()
arGruUsu.close()

usu3 = open("usuarios3.txt","w")

cont=0
for usu in usuarios:
	if usu not in textGruUsu:
		cont+=1

		if not cont%1000:
			print(str(cont))
		usu3.write("-" + usu + "\n")
usu3.close()
