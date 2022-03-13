import tensorflow as tf
from scipy.sparse import lil_matrix
import numpy as np
import operator

#### Lectura de datos
numGrupos = 93579
numUsu = 276083

# Matriz para datos
matriz = lil_matrix((numUsu,numGrupos))

arProc = open("./datos/arProc_ale.txt", "r")
textProc = arProc.read()
arProc.close()

grupo = ""
start= False
contUsu = 0
contGru=0

contador=0

# Bucle para leer lineas del archivo y guardar los datos
for i in textProc:
	if start:
		if(i=="*"):
			start=False
			matriz[contUsu,int(grupo)-1]=0.4
			grupo=""
			contUsu+=1
			contador=0

			if not contUsu%10000:
				print(str(contUsu))
		elif(i==","):
			matriz[contUsu,int(grupo)-1]=1-contador*0.06
			contador+=1
			grupo=""
		elif(i!='\n'):
			grupo = grupo+i
	else:
		if(i=="-"):
			start=True


session = tf.Session()
saver = tf.train.import_meta_graph('./red4/red4.meta')
saver.restore(session,tf.train.latest_checkpoint('./red4/'))

graph = tf.get_default_graph()
#### Parametros de la red

weights = {
    'encoder_h1': graph.get_tensor_by_name("Variable:0"),
    'encoder_h2': graph.get_tensor_by_name("Variable_1:0"),
    'decoder_h1': graph.get_tensor_by_name("Variable_2:0"),
    'decoder_h2': graph.get_tensor_by_name("Variable_3:0"),
}

biases = {
    'encoder_b1': graph.get_tensor_by_name("Variable_4:0"),
    'encoder_b2': graph.get_tensor_by_name("Variable_5:0"),
    'decoder_b1': graph.get_tensor_by_name("Variable_6:0"),
    'decoder_b2': graph.get_tensor_by_name("Variable_7:0"),
}

# Construyendo el codificador

def encoder(x):
    # Capa oculta del codificador con activacion de sigmoide #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']), biases['encoder_b1']))
    # Capa oculta del codificador con activacion de sigmoide #2
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['encoder_h2']), biases['encoder_b2']))
    return layer_2


# Construyendo el decodificador

def decoder(x):
    # Capa oculta del decodificador con activacion de sigmoide #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h1']), biases['decoder_b1']))
    # Capa oculta del decodificador con activacion de sigmoide #1
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['decoder_h2']), biases['decoder_b2']))
    return layer_2


#### Construimos el modelo
X = graph.get_tensor_by_name("X1:0")

encoder_op = encoder(X)
decoder_op = decoder(encoder_op)

# Inicializamos las variables

init = tf.global_variables_initializer()
local_init = tf.local_variables_initializer()
session.run(init)
session.run(local_init)


















batch_size = 600
num_batches = int(numUsu / batch_size)

dict1 = {}
dict10 = {}
dict20 = {}

for num_batch in range(0, num_batches):
	print('Batch: ' + str(num_batch) + '/' + str(num_batches))

	batch = matriz[num_batch*batch_size:(((num_batch+1)*batch_size) -1 ),:].todense()

	preds = session.run(decoder_op, feed_dict={X: batch})


	for i in preds:
		indexes = np.flipud(np.argpartition(i, -4)[-1:])

		for j in indexes:
			if j in dict1:
				dict1[j] = dict1[j] +1
			else:
				dict1[j] = 1

		indexes = np.flipud(np.argpartition(i, -4)[-10:])

		for j in indexes:
			if j in dict10:
				dict10[j] = dict10[j] +1
			else:
				dict10[j] = 1

		indexes = np.flipud(np.argpartition(i, -4)[-20:])

		for j in indexes:
			if j in dict20:
				dict20[j] = dict20[j] +1
			else:
				dict20[j] = 1

#Max 1
sorted_1 = sorted(dict1.items(), key=operator.itemgetter(1))

archivo  = open("./2max1.txt", "w")

for i in sorted_1:
	archivo.write("Grupo: " + str(i[0]) + " -> veces: " + str(i[1]) + "\n")

archivo.flush()
archivo.close()

#Max 10
sorted_10 = sorted(dict10.items(), key=operator.itemgetter(1))

archivo  = open("./2max10.txt", "w")

for i in sorted_10:
	archivo.write("Grupo: " + str(i[0]) + " -> veces: " + str(i[1]) + "\n")

archivo.flush()
archivo.close()

#Max 20
sorted_20 = sorted(dict20.items(), key=operator.itemgetter(1))

archivo  = open("./2max20.txt", "w")

for i in sorted_20:
	archivo.write("Grupo: " + str(i[0]) + " -> veces: " + str(i[1]) + "\n")

archivo.flush()
archivo.close()
