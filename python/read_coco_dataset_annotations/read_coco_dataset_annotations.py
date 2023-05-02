
import os
import argparse
import logging
import requests
import shutil
import json
import pandas as pd

from pathlib import Path

logging.basicConfig(filename='/tmp/log.txt', encoding='utf-8', level=logging.DEBUG)

def argument_parser():
    """Argument Parser
    
    Parse arguments.
    
    Returns:
        Arguments as argparse.Namespace
    """
    
    parser = argparse.ArgumentParser(description='Read Annotations of COCO Dataset',
                formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--output_dir', dest='output_dir', type=str, default='downloads', required=False, \
            help='Directory path to save files')

    args = parser.parse_args()

    return args

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

def read_coco_annotations(captions_json, instances_json, person_keypoints_json):
    """Read COCO Annotations
    
    Read COCO Annotations from captions, instances and person keypoints json files.
    
    Args:
        captions_json (string): json file path of captions
        instances_json (string): json file path of instances
        person_keypoints_json (string): json file path of person_keypoints
    
    Returns:
        COCO Annotations as pandas.DataFrame
    """
    
    def _get_captions_licenses(x, dict_caption_licenses=None):
        license = dict_caption_licenses[x.license]
        
        dict_rename = dict(zip(license.keys(), [f'license_{key}' for key in license.keys()]))
        ret = pd.Series(license)
        ret.rename(dict_rename, inplace=True)
        
        return ret
    
    def _get_captions_annotations(x, df_annotations=None):
        annotation = df_annotations[df_annotations['image_id']==x['id']].iloc[0]
        annotation.rename({'id': 'caption_id'}, inplace=True)
        annotation.drop(index='image_id', inplace=True)
        
        return annotation
    
    with open(captions_json, 'r') as f:
        caption_data = json.load(f)
    
    logging.info(f'caption_data.keys(): {caption_data.keys()}')
    
    dict_caption_licenses_key = [l['id'] for l in caption_data["licenses"]]
    dict_caption_licenses = dict(zip(dict_caption_licenses_key, caption_data["licenses"]))
    
    df_coco_annotations = pd.DataFrame(caption_data["images"])
    
    df_captions_licenses = df_coco_annotations.apply(_get_captions_licenses, axis=1, dict_caption_licenses=dict_caption_licenses)
    
    df_coco_annotations = pd.concat([df_coco_annotations, df_captions_licenses], axis=1)
    df_coco_annotations.drop(columns=['license'], inplace=True)
    
    df_captions_annotations = df_coco_annotations.apply(_get_captions_annotations, axis=1, df_annotations=pd.DataFrame(caption_data["annotations"]))
    
    df_coco_annotations.rename(columns={'id': 'image_id'}, inplace=True)
    df_coco_annotations = pd.concat([df_coco_annotations, df_captions_annotations], axis=1)
    
    logging.info(f'df_coco_annotations.columns:\n{df_coco_annotations.columns}')
    logging.info(f'df_coco_annotations:\n{df_coco_annotations}')
    

def main():
    """main
    
    main function
    """
    
    args = argument_parser()
    logging.info('Arguments:')
    logging.info(f'    - args.output_dir: {args.output_dir}')
    
    download_and_extract()
    read_coco_annotations(
        Path(args.output_dir, 'annotations', 'captions_val2017.json'),
        Path(args.output_dir, 'annotations', 'instances_val2017.json'),
        Path(args.output_dir, 'annotations', 'person_keypoints_val2017.json'),
    )
    
    return

# --- main routine ---
if __name__=='__main__':
    main()
