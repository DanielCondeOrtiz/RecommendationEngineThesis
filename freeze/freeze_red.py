import tensorflow as tf

saver = tf.train.import_meta_graph('./red4/red4.meta')
graph = tf.get_default_graph()
input_graph_def = graph.as_graph_def()
session = tf.Session()
saver.restore(session,tf.train.latest_checkpoint('./red4/'))

input_graph_def = graph.as_graph_def()
output_graph_def = tf.graph_util.convert_variables_to_constants(
            session, # The session
            input_graph_def,
            ("X1,Variable,Variable_1,Variable_2,Variable_3,
            Variable_4,Variable_5,Variable_6,Variable_7").split(",")
)

output_graph="./freeze/red.pb"
with tf.gfile.GFile(output_graph, "wb") as f:
    f.write(output_graph_def.SerializeToString())

session.close()
