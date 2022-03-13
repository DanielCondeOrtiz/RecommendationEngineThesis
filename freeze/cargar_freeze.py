#Cargamos la red

frozen_graph="./freeze/red.pb"
with tf.gfile.GFile(frozen_graph, "rb") as f:
    restored_graph_def = tf.GraphDef()
    restored_graph_def.ParseFromString(f.read())


with tf.Graph().as_default() as graph:
    tf.import_graph_def(
        restored_graph_def,
        input_map=None,
        return_elements=None,
        name=""
        )

session=tf.Session(graph=graph)

#### Parametros de la red

X = graph.get_tensor_by_name("X1:0")

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


encoder_op = encoder(X)
decoder_op = decoder(encoder_op)
