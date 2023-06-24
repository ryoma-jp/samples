
import os
import cv2
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
                if (func_layer['class_name'] in feature_attr):
                    feature_list.append(layer.layers[j].output)
    
    # --- Build model to get feature maps ---
    model = tf.keras.models.Model(inputs=inputs, outputs=feature_list)
    
    # --- Show feature_list ---
    logging.info(feature_list)
    
    # --- Load CIFAR-10 dataset ---
    train_images, train_labels, test_images, test_labels = load_cifar10('dataset', img_dir='dataset/img')
    logging.info(f'Downloaded CIFAR-10 dataset')
    logging.info(f'  * train_images.shape: {train_images.shape}')
    logging.info(f'  * train_labels.shape: {train_labels.shape}')
    logging.info(f'  * test_images.shape: {test_images.shape}')
    logging.info(f'  * test_labels.shape: {test_labels.shape}')
    
    # --- Prediction ---
    test_num = 10
    input_tensor = test_images[0:test_num] / 255.
    output_tensor = model.predict(input_tensor)
    prediction = output_tensor[0]
    logging.info(f'prediction.shape: {prediction.shape}')
    logging.info(f'prediction.argmax: {prediction.argmax(axis=1)}')
    
    # --- Save test images ---
    for img_no, test_image in enumerate(test_images[0:test_num]):
        os.makedirs('test_image', exist_ok=True)
        save_file = str(Path('test_image', f'img{img_no}.png'))
        cv2.imwrite(save_file, cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR))
    
    # --- Calc accuracy ---
    acc = accuracy_score(test_labels[0:test_num].argmax(axis=1), prediction.argmax(axis=1))
    logging.info(f'accuracy: {acc}')
    
    # --- Get feature maps ---
    for i, feature in enumerate(output_tensor[1:]):
        logging.info(f'Feature #{i}: {feature.shape}')
        
        for img_no, feature_per_img in enumerate(feature):
            # --- convert to [0 .. 255] to save image ---
            min = feature_per_img.min()
            max = feature_per_img.max()
            feature_per_img_norm = ((feature_per_img - min) / (max - min) * 255).astype(np.uint8)
            
            for filter_no, feature_per_filter in enumerate(feature_per_img_norm.transpose(2, 0, 1)):
                feature_map_dir = Path('feature_maps', f'img{img_no}')
                feature_file = f'feature{i}_filter{filter_no}.png'
                save_file = str(Path(feature_map_dir, feature_file))
                
                os.makedirs(feature_map_dir, exist_ok=True)
                cv2.imwrite(save_file, feature_per_filter)
                
    
if __name__=='__main__':
    main()


