from keras.models import load_model
import numpy as np

class CommandPrediction():
    def __init__(self):
        self.model = load_model('model/model-14-08.h5')
        #self.model.summary()
        print('---------------- Load model successfully -----------------')
        
    def predict(self, feature_tensor):
        """
        Return command index (0 - 15) va xac suat predict cua no (0.0 - 1.0)
        """
        probabilities = self.model.predict(feature_tensor)[0]
        command_index = np.argmax(probabilities)
        
        return command_index, probabilities[command_index]
        
    def display_model_architecture(self):
        self.model.summary()
