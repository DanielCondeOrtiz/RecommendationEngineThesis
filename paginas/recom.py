#Módulo encargado de la red neuronal
import tensorflow as tf
from scipy.sparse import lil_matrix
import numpy as np

numGrupos = 93579

#Iniciamos la sesión y cargamos la red
session = tf.Session()
saver = tf.train.import_meta_graph('../red/red4/red4.meta')
saver.restore(session,tf.train.latest_checkpoint('../red/red4/'))

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

X = graph.get_tensor_by_name("X1:0")

#### Construimos el modelo
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




encoder_op = encoder(X)
decoder_op = decoder(encoder_op)

# Inicializamos las variables

init = tf.global_variables_initializer()
local_init = tf.local_variables_initializer()
session.run(init)
session.run(local_init)


#Método que recibe una lista de grupos y recomienda
def recomendar(lista):

	nuevaLista = lil_matrix((1,numGrupos))

	for i in range(0,len(lista)):
		nuevaLista[0,lista[i]] = 1 - 0.06*i


	preds = session.run(decoder_op, feed_dict={X: nuevaLista.todense()})

	indexes = np.flipud(np.argpartition(preds[0], -4)[-13:])

	return indexes
