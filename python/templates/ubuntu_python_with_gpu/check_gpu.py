from tensorflow.python.client import device_lib
import torch

def main():
    """main
    
    main function
    """
    
    print('This is the test program')
    
    print('Check devices (TensorFlow)')
    print(device_lib.list_local_devices())
    
    print('Check devices (PyTorch)')
    print(torch.cuda.is_available())
    
    return

# --- main routine ---
if __name__=='__main__':
    main()
