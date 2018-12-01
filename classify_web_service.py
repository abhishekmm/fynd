import tensorflow as tf
def classify(image_path):
    # Read in the image_data
    #image_data = tf.gfile.FastGFile('/home/tensorflow/tensorflow/examples/method3mod/dataset/dataset/T', 'rb').read()
    #print(image_path)
    print("==========================")
    image_path=image_path.replace('\\', '/')
     #print(image_path)
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()
    #print(image_data)
    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line 
                       # in tf.gfile.GFile("/tf_files/retrained_labels.txt")]
                       in tf.gfile.GFile("retrained_labels3.txt")]

    # Unpersists graph from file
    # with tf.gfile.FastGFile("/tf_files/retrained_graph.pb", 'rb') as f:
    with tf.gfile.FastGFile("D:/POCs/TransferLearning/retailDemo/transferlearnmodels/retrained_graph_half_full.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        
        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
        
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        output=""
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            output=output+"<br> "+label_lines[node_id] + "=>{:.5f}".format(score) 
            print('%s (score = %.5f)' % (human_string, score))
            
        return output
