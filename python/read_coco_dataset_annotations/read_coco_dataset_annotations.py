
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
            - df_captions: annotation data of captions
            - df_instances: annotation data of instances
            - df_keypoints: annotation data of person keypoints
    """
    
    def _get_licenses(x, df_licenses=None):
        license = df_licenses[df_licenses['id']==x['license']].iloc[0]
        
        dict_rename = dict(zip(license.index, [f'license_{index}' for index in license.index]))
        license.rename(dict_rename, inplace=True)
        
        return license
    
    def _get_captions_annotations(x, df_annotations=None):
        annotation = df_annotations[df_annotations['image_id']==x['id']].iloc[0]
        annotation.rename({'id': 'caption_id'}, inplace=True)
        annotation.drop(index='image_id', inplace=True)
        
        return annotation
    
    def _get_instances_annotations(x, df_images=None, df_categories=None):
        image = df_images[df_images['id']==x['image_id']].iloc[0]
        image.rename({'id': 'image_id'}, inplace=True)
        
        x.drop(index='image_id', inplace=True)
        x.rename({'id': 'instance_id'}, inplace=True)
        
        category = df_categories[df_categories['id']==x['category_id']].iloc[0]
        category.rename({'id': 'category_id', 'name': 'category_name'}, inplace=True)
        
        x.drop(index='category_id', inplace=True)
        
        annotation = pd.concat([image, x, category])
        
        return annotation
    
    def _get_keypoints_annotations(x, df_images=None, df_categories=None):
        image = df_images[df_images['id']==x['image_id']].iloc[0]
        image.rename({'id': 'image_id'}, inplace=True)
        
        x.drop(index='image_id', inplace=True)
        x.rename({'id': 'keypoint_id'}, inplace=True)
        
        category = df_categories[df_categories['id']==x['category_id']].iloc[0]
        category.rename({'id': 'category_id', 'name': 'category_name'}, inplace=True)
        
        x.drop(index='category_id', inplace=True)
        
        annotation = pd.concat([image, x, category])
        
        return annotation
    
    # --- get captions ---
    with open(captions_json, 'r') as f:
        caption_data = json.load(f)
    
    df_captions = pd.DataFrame(caption_data["images"])
    
    logging.info(f'caption_data.keys(): {caption_data.keys()}')
    
    df_captions_licenses = df_captions.apply(_get_licenses, axis=1, df_licenses=pd.DataFrame(caption_data["licenses"]))
    df_captions = pd.concat([df_captions, df_captions_licenses], axis=1)
    df_captions.drop(columns=['license'], inplace=True)
    
    df_captions_annotations = df_captions.apply(_get_captions_annotations, axis=1, df_annotations=pd.DataFrame(caption_data["annotations"]))
    df_captions.rename(columns={'id': 'image_id'}, inplace=True)
    df_captions = pd.concat([df_captions, df_captions_annotations], axis=1)
    
    logging.info(f'df_captions.columns:\n{df_captions.columns}')
    logging.info(f'df_captions:\n{df_captions}')
    
    # --- get instances ---
    with open(instances_json, 'r') as f:
        instance_data = json.load(f)
    
    df_instances = pd.DataFrame(instance_data["images"])
    
    logging.info(f'instance_data.keys(): {instance_data.keys()}')
    
    df_instances_licenses = df_instances.apply(_get_licenses, axis=1, df_licenses=pd.DataFrame(instance_data["licenses"]))
    df_instances = pd.concat([df_instances, df_instances_licenses], axis=1)
    df_instances.drop(columns=['license'], inplace=True)
    
    df_instances_annotations = pd.DataFrame(instance_data['annotations'])
    df_instances_categories = pd.DataFrame(instance_data['categories'])
    df_instances = df_instances_annotations.apply(
                       _get_instances_annotations,
                       axis=1,
                       df_images=df_instances,
                       df_categories=df_instances_categories)
    
    logging.info(f'df_instances.columns:\n{df_instances.columns}')
    logging.info(f'df_instances:\n{df_instances}')
    
    # --- get keypoints ---
    with open(person_keypoints_json, 'r') as f:
        keypoints_data = json.load(f)
    
    df_keypoints = pd.DataFrame(keypoints_data["images"])
    
    logging.info(f'keypoints_data.keys(): {keypoints_data.keys()}')
    
    df_keypoints_licenses = df_keypoints.apply(_get_licenses, axis=1, df_licenses=pd.DataFrame(keypoints_data["licenses"]))
    df_keypoints = pd.concat([df_keypoints, df_keypoints_licenses], axis=1)
    df_keypoints.drop(columns=['license'], inplace=True)
    
    df_keypoints_annotations = pd.DataFrame(keypoints_data['annotations'])
    df_keypoints_categories = pd.DataFrame(keypoints_data['categories'])
    df_keypoints = df_keypoints_annotations.apply(
                       _get_keypoints_annotations,
                       axis=1,
                       df_images=df_keypoints,
                       df_categories=df_keypoints_categories)
    
    logging.info(f'df_keypoints.columns:\n{df_keypoints.columns}')
    logging.info(f'df_keypoints:\n{df_keypoints}')
    
    return df_captions, df_instances, df_keypoints
    
def main():
    """main
    
    main function
    """
    
    args = argument_parser()
    logging.info('Arguments:')
    logging.info(f'    - args.output_dir: {args.output_dir}')
    
    download_and_extract()
    df_captions, df_instances, df_keypoints = read_coco_annotations(
        Path(args.output_dir, 'annotations', 'captions_val2017.json'),
        Path(args.output_dir, 'annotations', 'instances_val2017.json'),
        Path(args.output_dir, 'annotations', 'person_keypoints_val2017.json'),
    )
    
    df_captions.to_csv(Path(args.output_dir, 'captions.csv'))
    df_instances.to_csv(Path(args.output_dir, 'instances.csv'))
    df_keypoints.to_csv(Path(args.output_dir, 'keypoints.csv'))
    
    return

# --- main routine ---
if __name__=='__main__':
    main()
