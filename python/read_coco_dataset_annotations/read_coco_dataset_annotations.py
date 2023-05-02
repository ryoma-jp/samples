
import os
import logging
import requests
import shutil

from pathlib import Path

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

def download_and_extract(output_dir='downloads'):
    """Download and extract COCO Dataset
    
    Download and extract COCO Dataset.
    
    Args:
        output_dir (string): directory path of output files
    """
    
    # --- create output directory ---
    os.makedirs(output_dir, exist_ok=True)
    
    # --- download COCO annotations ---
    url = 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'
    save_file = Path(output_dir, Path(url).name)
    if (not save_file.exists()):
        logging.info(f'annotations_trainval2017.zip downloading ...')
        with requests.get(url, stream=True) as r:
          with open(save_file, mode='wb') as f:
              for chunk in r.iter_content(chunk_size=1048576):
                  f.write(chunk)
        logging.info(f'DONE')
    else:
        logging.info(f'Download skipped, because {save_file} is exist')
    
    # --- extract zip file ---
    if (not Path(output_dir, 'annotations').exists()):
        logging.info(f'annotations_trainval2017.zip extracting ...')
        shutil.unpack_archive(save_file, output_dir)
        logging.info(f'DONE')
    else:
        logging.info(f'Extract is skipped, because {Path(output_dir, "annotations")} is exist')

def main():
    """main
    
    main function
    """
    
    download_and_extract()
    
    return

# --- main routine ---
if __name__=='__main__':
    main()
