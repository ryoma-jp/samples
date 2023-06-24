
import logging
import tensorflow as tf

from external.yolov3.yolov3_tf2 import models as yolov3_models

logging.basicConfig(level=logging.INFO)

def main():
    # --- Load model ---
    model = yolov3_models.YoloV3(size=416, classes=80, training=True)
    model.summary()
    
    # --- Get features ---
    #  * get output attributes of 'Conv2D'
    inputs = model.input
    feature_attr = ['Conv2D']
    feature_list = []
    feature_list.append(model.output)
    for i, layer in enumerate(model.layers):
        if (layer.__class__.__name__ in feature_attr):
            feature_list.append(layer.output)
        elif (layer.__class__.__name__ == 'Functional'):
            layer_config = layer.get_config()
            for j, func_layer in enumerate(layer_config['layers']):
                logging.info(func_layer['class_name'])
                if (func_layer['class_name'] in feature_attr):
                    feature_list.append(layer.layers[j].output)
    logging.info(feature_list)
    
    model = tf.keras.models.Model(inputs=inputs, outputs=feature_list)
    
if __name__=='__main__':
    main()


