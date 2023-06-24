
import logging
import tensorflow as tf
import tensorflow_hub as hub

logging.basicConfig(level=logging.INFO)

def main():
    # --- Load model ---
    url = 'https://tfhub.dev/tensorflow/centernet/hourglass_512x512/1'
    model = hub.load(url)
    model.summary()
    
if __name__=='__main__':
    main()


