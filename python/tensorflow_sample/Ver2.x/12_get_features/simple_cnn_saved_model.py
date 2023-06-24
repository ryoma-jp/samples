
import logging
import numpy as np
import tensorflow as tf

from pathlib import Path
from sklearn.metrics import accuracy_score
from lib.data_loader.cifar10 import load_cifar10

logging.basicConfig(level=logging.INFO)

def main():
    # --- Load model ---
    saved_model_path = Path('sample_model', 'saved_model')
    model = tf.keras.models.load_model(saved_model_path)
    model.summary()
    
    # --- Get features ---
    #  * get output attributes of 'Conv2D' and 'Dense'
    feature_attr = ['Conv2D', 'Dense']
    feature_list = []
    for i, layer in enumerate(model.layers):
        if (layer.__class__.__name__ in feature_attr):
            feature_list.append(layer.output)
        elif (layer.__class__.__name__ == 'Functional'):
            layer_config = layer.get_config()
            for j, func_layer in enumerate(layer_config['layers']):
                if (func_layer['class_name'] in feature_attr):
                    feature_list.append(layer.layers[j].output)
    
    # --- Show feature_list ---
    logging.info(feature_list)
    
    # --- Load CIFAR-10 dataset ---
    train_images, train_labels, test_images, test_labels = load_cifar10('dataset', img_dir='dataset/img')
    logging.info(f'Downloaded CIFAR-10 dataset')
    logging.info(f'  * train_images.shape: {train_images.shape}')
    logging.info(f'  * train_labels.shape: {train_labels.shape}')
    logging.info(f'  * test_images.shape: {test_images.shape}')
    logging.info(f'  * test_labels.shape: {test_labels.shape}')
    
    # --- Preciction ---
    input_tensor = test_images / 255.
    prediction = model.predict(input_tensor)
    logging.info(f'prediction.shape: {prediction.shape}')
    logging.info(f'prediction.argmax: {prediction.argmax(axis=1)}')
    
    # --- Calc accuracy ---
    acc = accuracy_score(test_labels.argmax(axis=1), prediction.argmax(axis=1))
    logging.info(f'accuracy: {acc}')
    
if __name__=='__main__':
    main()


