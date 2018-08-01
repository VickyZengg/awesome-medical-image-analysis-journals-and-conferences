
import keras
import numpy as np

import utils.boxes as util_box

class RegressBoxes(keras.layers.Layer):
    
    def __init__(self, mean=None, std=None, *args, **kwargs):
        """Initializer for RegressBoxes layer

        Args:
            mean: The mean value of regression values

        """
        if mean is None:
            mean = np.array([0, 0, 0, 0])
        
        if std is None:
            std = np.array([0.2, 0.2, 0.2, 0.2])
        
        if isinstance(mean, (list, tuple)):
            mean = np.array(mean)
        elif not isinstance(mean, np.ndarray):
            raise ValueError('Excepted mean to be a np.ndarry, list, or a tuple, received: {}'.format(type(mean)))
        
        if isinstance(std, (tuple, list)):
            std = np.array(std)
        elif not isinstance(std, np.ndarray):
            raise ValueError('Excepted std to be a np.ndarry, list, or a tuple, received: {}'.format(type(std)))
        
        self.mean = mean
        self.std = std
        super().__init__(*args, **kwargs)

    def call(self, inputs, **kwargs):
        anchors, regression = inputs
        return util_box.bbox_transform_inv(anchors, regression, mean=self.mean, std=self.std)
    
    def compute_output_shape(self, input_shape):
        return input_shape[0]
    
    def get_config(self):
        config = super().get_config()
        config.update({
            'mean' : self.mean.tolist(),
            'std' : self.std.tolist()
        })

        return config