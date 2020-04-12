import os
import logging
import tensorflow as tf
from keras.models import model_from_json

class NeuralNetwork:
    def __init__(self, folder="."):
        self.session = tf.Session()
        self.graph = tf.get_default_graph()
        # the folder in which the model and weights are stored
        self.model_folder = folder #os.path.join(os.path.abspath("src"), "static")
        self.model = None
        # for some reason in a flask app the graph/session needs to be used in the init else it hangs on other threads
        with self.graph.as_default():
            with self.session.as_default():
                logging.info("neural network initialised")

    def load(self, file_name=None):
        """
        :param file_name: [model_file_name, weights_file_name]
        :return:
        """
        with self.graph.as_default():
            with self.session.as_default():
                try:
                    model_name = file_name[0]
                    weights_name = file_name[1]

                    if model_name is not None:
                        # load the model
                        json_file_path = os.path.join(self.model_folder, model_name)
                        json_file = open(json_file_path, 'r')
                        loaded_model_json = json_file.read()
                        json_file.close()
                        self.model = model_from_json(loaded_model_json)
                    if weights_name is not None:
                        # load the weights
                        weights_path = os.path.join(self.model_folder, weights_name)
                        self.model.load_weights(weights_path)
                    logging.info("Neural Network loaded: ")
                    logging.info('\t' + "Neural Network model: " + model_name)
                    logging.info('\t' + "Neural Network weights: " + weights_name)
                    return True
                except Exception as e:
                    logging.exception(e)
                    return False

    def predict(self, x):
        with self.graph.as_default():
            with self.session.as_default():
                y = self.model.predict(x)
        return y

