#Archivo para encontrar usuarios o grupos duplicados
usuarios = []

arUsu = open("usuarios3.txt","r")
textUsu = arUsu.read()
arUsu.close()
usuario=""
for i in textUsu:
	if(i=='\n'):
		usuarios.append(usuario)
		usuario=""
	else:
		usuario=usuario+i

arNuevo = open("usuarios3N.txt","w")
total=[]
cuenta=0
for i in usuarios:
	if i in total:
		cuenta+=1
		print(str(cuenta))
		print(i)
	else:
		total.append(i)
		arNuevo.write(i + "\n")
		arNuevo.flush()


'''

usuarios = []

arUsu = open("grupos.txt","r")
textUsu = arUsu.read()
arUsu.close()
usuario=""
for i in textUsu:
	if(i=='\n'):
		usuarios.append(usuario)
		usuario=""
	else:
		usuario=usuario+i

arNuevo = open("gruposN.txt","w")
total=[]
cuenta=0
for i in usuarios:
	if i in total:
		cuenta+=1
		print(str(cuenta))
		print(i)
	else:
		total.append(i)
		arNuevo.write(i+ "\n")
		arNuevo.flush()
'''
