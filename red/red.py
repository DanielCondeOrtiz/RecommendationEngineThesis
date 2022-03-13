import pandas as pd
import tensorflow as tf
from scipy.sparse import lil_matrix
import time
import numpy as np

print('Comenzando programa')

start_time = time.time()


#### Lectura de datos
numGrupos = 93579
numUsu = 276083

# Matriz para datos
matriz = lil_matrix((numUsu,numGrupos))

arProc = open("./datos/arProc.txt", "r")
textProc = arProc.read()
arProc.close()

grupo = ""
start= False
contUsu = 0
contGru=0

contador = 0

# Bucle para leer lineas del archivo y guardar los datos
for i in textProc:
	if start:
		if(i=="*"):
			start=False
			matriz[contUsu,int(grupo)-1]=0.4
			grupo=""
			contUsu+=1
			contador = 0

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



end_processing = time.time()

print('Lectura de datos finalizada después de ' + str(end_processing - start_time) + ' segundos')

#### Parametros de la red

num_input = numGrupos
num_hidden_1 = 235
num_hidden_2 = 100

X = tf.placeholder(tf.float64, [None, num_input], name="X1")

weights = {
    'encoder_h1': tf.Variable(tf.random_normal([num_input, num_hidden_1], dtype=tf.float64)),
    'encoder_h2': tf.Variable(tf.random_normal([num_hidden_1, num_hidden_2], dtype=tf.float64)),
    'decoder_h1': tf.Variable(tf.random_normal([num_hidden_2, num_hidden_1], dtype=tf.float64)),
    'decoder_h2': tf.Variable(tf.random_normal([num_hidden_1, num_input], dtype=tf.float64)),
}

biases = {
    'encoder_b1': tf.Variable(tf.random_normal([num_hidden_1], dtype=tf.float64)),
    'encoder_b2': tf.Variable(tf.random_normal([num_hidden_2], dtype=tf.float64)),
    'decoder_b1': tf.Variable(tf.random_normal([num_hidden_1], dtype=tf.float64)),
    'decoder_b2': tf.Variable(tf.random_normal([num_input], dtype=tf.float64)),
}

# Construyendo el codificador

def encoder(x):
    # Capa oculta 1 del codificador con activacion de sigmoide
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']), biases['encoder_b1']))
    # Capa oculta 2 del codificador con activacion de sigmoide
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['encoder_h2']), biases['encoder_b2']))
    return layer_2


# Construyendo el decodificador

def decoder(x):
    # Capa oculta 1 del decodificador con activacion de sigmoide
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h1']), biases['decoder_b1']))
    # Capa oculta 2 del decodificador con activacion de sigmoide
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['decoder_h2']), biases['decoder_b2']))
    return layer_2


#### Construimos el modelo

encoder_op = encoder(X)
decoder_op = decoder(encoder_op)

# Prediccion
y_pred = decoder_op

# Los objetivos son
#los datos de entrada.
y_true = X


# Definimos la pérdida y el optimizador.
# Minimizamos el error al cuadrado
with tf.name_scope("Loss"):
	loss = tf.losses.mean_squared_error(y_true, y_pred)

with tf.name_scope("Optimizer"):
	optimizer = tf.train.RMSPropOptimizer(0.06).minimize(loss)

predictions = pd.DataFrame()

# Definimos las métricas de evaluación

eval_x = tf.placeholder(tf.int32, )
eval_y = tf.placeholder(tf.int32, )
pre, pre_op = tf.metrics.precision(labels=eval_x, predictions=eval_y)

# Para inicializar las variables
init = tf.global_variables_initializer()
local_init = tf.local_variables_initializer()

# Para guardar la red neuronal
#Antes de iniciar la sesión
saver = tf.train.Saver()

#Para la visualizacion
tf.summary.scalar("loss", loss)
merged_summary_op = tf.summary.merge_all()

#Para los logs
fecha = time.strftime("%H_%M_%S")
arLogs = open("./logs/log_" + fecha + ".txt","w+")

print("Comenzando entrenamiento")
arLogs.write("Comenzando entrenamiento: \n" + fecha)

#### Iniciamos la sesion
with tf.Session() as session:
	# Parámetros de entrenamiento
	epochs = 150
	batch_size = 300

	session.run(init)
	session.run(local_init)

	num_batches = int(numUsu / batch_size)

	summary_writer = tf.summary.FileWriter('./graph5', graph=tf.get_default_graph())

	# Entrenamos la red
	for i in range(epochs):

		avg_cost = 0

		start_epoch = time.time()

		# Dividimos la matriz de entrada en diferentes batches mas pequeños
		# Cada uno se lo damos a la red para entrenarla
		for num_batch in range(0, num_batches):
			batch = matriz[num_batch*batch_size:(((num_batch+1)*batch_size) -1 ),:].todense()
			_, l, summary_str = session.run([optimizer, loss, merged_summary_op], feed_dict={X: batch})

summary_writer.add_summary(summary_str, i*num_batches + num_batch)

			avg_cost += l

			print('Batch: ' + str(num_batch) + '/' + str(num_batches))


		avg_cost /= num_batches

		end_epoch = time.time()
		print("Epoch: {} Loss: {}".format(i + 1, avg_cost))
		print('Tiempo para epoch: ' + str(end_epoch - start_epoch) + ' segundos')

		arLogs.write("Epoch: {} Loss: {}\n".format(i + 1, avg_cost))
		arLogs.write("Tiempo para epoch: " + str(end_epoch - start_epoch) + " segundos\n")
		arLogs.flush()

	#Tras haber acabado el entrenamiento
	saver.save(session, './red5/')

	end_program = time.time()
	print('Entrenamiento finalizado despues de: ' + str(end_program - start_time) + ' segundos. ' + fecha)
	arLogs.write('Entrenamiento finalizado despues de: ' + str(end_program - start_time) + ' segundos. ' + fecha + '\n')
	arLogs.flush()
	arLogs.close()

	#### Predicciones
	#print("Predicciones")

	#preds = session.run(decoder_op, feed_dict={X: matriz[0,:].todense()})

	#predictions = predictions.append(pd.DataFrame(preds))

	#indexes = np.flipud(np.argpartition(preds[0], -4)[-10:])
	#print(indexes)
	#print(preds[0][indexes])

	#real_end_program = time.time()
	#print('Programa finalizado después de: ' + str(real_end_program - start_time) + ' segundos')
