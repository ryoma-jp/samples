
import os
import cv2
import tqdm
import numpy as np
import logging
import requests
import tarfile

from pathlib import Path

identity = np.eye(10, dtype=np.int32)

def load_cifar10(dataset_dir, img_dir=None, download=True):
    def download_file(url, save_dir='output'):
        """Download file

        This function downloads file to the directory specified ``save_dir`` from ``url``.

        Args:
            url (string): specify URL
            save_dir (string): specify the directory to save file.
        
        Return:
            file path of the downloaded file
        """
        
        save_file = Path(save_dir, Path(url).name)
        with requests.get(url, stream=True) as r:
          with open(save_file, mode='wb') as f:
              for chunk in r.iter_content(chunk_size=1048576):
                  f.write(chunk)
        
        return save_file
        
    def unpickle(file):
        import pickle
        with open(file, 'rb') as fo:
            dict = pickle.load(fo, encoding='bytes')
        return dict
    
    # --- download dataset and extract ---
    if (download):
        logging.info(f'[DataLoaderCIFAR10] {dataset_dir}')
        os.makedirs(dataset_dir, exist_ok=True)
        if (not Path(dataset_dir, 'cifar-10-batches-py').exists()):
            url = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'
            save_file = download_file(url, dataset_dir)
            
            with tarfile.open(save_file) as tar:
                # --- CVE-2007-4559 start ---
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = Path(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                safe_extract(tar, path=dataset_dir)
                # --- CVE-2007-4559 end ---
        else:
            logging.info('CIFAR-10 dataset is exists (Skip Download)')
    dataset_dir = Path(dataset_dir, 'cifar-10-batches-py')
    
    # --- load training data ---
    train_data_list = ["data_batch_1", "data_batch_2", "data_batch_3", "data_batch_4", "data_batch_5"]
    dict_data = unpickle(os.path.join(dataset_dir, train_data_list[0]))
    train_images = dict_data[b'data']
    train_labels = [identity[i] for i in dict_data[b'labels']]
    train_filenames = dict_data[b'filenames']
    for train_data in tqdm.tqdm(train_data_list[1:]):
        dict_data = unpickle(os.path.join(dataset_dir, train_data))
        train_images = np.vstack((train_images, dict_data[b'data']))
        train_labels = np.vstack((train_labels, [identity[i] for i in dict_data[b'labels']]))
        train_filenames = np.hstack((train_filenames, dict_data[b'filenames']))
    
    # --- load test data ---
    test_data = "test_batch"
    dict_data = unpickle(os.path.join(dataset_dir, test_data))
    test_images = dict_data[b'data']
    test_labels = [identity[i] for i in dict_data[b'labels']]
    test_filenames = dict_data[b'filenames']
    
    # --- transpose: [N, C, H, W] -> [N, H, W, C] ---
    train_images = train_images.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
    test_images = test_images.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)

    # --- save image data ---
    #  * if img_dir is not None
    if (img_dir is not None):
        # --- create output directories ---
        os.makedirs(os.path.join(img_dir, 'train'), exist_ok=True)
        os.makedirs(os.path.join(img_dir, 'test'), exist_ok=True)

        # --- train images ---
        for (img, filename) in tqdm.tqdm(zip(train_images, train_filenames), total=len(train_images)):
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imwrite(os.path.join(img_dir, 'train', filename.decode()), img)

        # --- test images ---
        for (img, filename) in tqdm.tqdm(zip(test_images, test_filenames), total=len(test_images)):
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imwrite(os.path.join(img_dir, 'test', filename.decode()), img)
    
    return np.array(train_images), np.array(train_labels), np.array(test_images), np.array(test_labels)



