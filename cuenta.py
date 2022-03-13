import operator

archivos=["./cuenta.py","./grupos.html","./grupos.py","./index.html","./peticion.py","./recom.py","./script.js",
"./server.py","./style.css"]

letras = 0
lineas = 0

dict={}

for i in archivos:
    letrasInd = 0
    lineasInd = 0

    ar = open(i,"r")
    texto = ar.read()
    ar.close()

    lineas+=1
    lineasInd+=1

    for j in texto:
        letras+=1
        letrasInd+=1

        if '\n' in j:
            lineas+=1
            lineasInd+=1

        if j in dict:
            dict[j] = dict[j] + 1
        else:
            dict[j] = 1


    print("----------")
    print(i)
    print("Letras: " + str(letrasInd))
    print("Lineas: " + str(lineasInd))

print("----------")
print("Total:")
print("Letras: " + str(letras))
print("Lineas: " + str(lineas))
print("----------")

sorted_x = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)

for i in sorted_x:
    print("Letra: " + i[0])
    print("Total: " + str(i[1]))
    print(str(i[1]/letras) + "%")
