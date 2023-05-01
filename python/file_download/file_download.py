
import os
import argparse
import requests

from pathlib import Path

def ArgParser():
    """ArgParser
    
    Argument parser
    """
    parser = argparse.ArgumentParser(description='ファイルをダウンロードするプログラムのサンプル',
                formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--file_size', dest='file_size', type=str, default='small', choices=['small', 'big'], \
            help='ダウンロードするファイルの大きさを選択する\n'
                 '    - small: ``2017 Train/Val annotations``を一括でダウンロードする\n'
                 '    - big  : ``2017 Train images``を分割してダウンロードする\n')
    parser.add_argument('--download_dir', dest='download_dir', type=str, default='downloads', \
            help='ダウンロードしたファイルを格納するディレクトリを指定する')

    args = parser.parse_args()

    return args
def main():
    args = ArgParser()
    print(f'args.file_size : {args.file_size}')
    print(f'args.download_dir : {args.download_dir}')
    
    os.makedirs(args.download_dir, exist_ok=True)
    
    if (args.file_size == 'small'):
        url = 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'
        
        save_file = Path(args.download_dir, Path(url).name)
        content = requests.get(url).content
        
        with open(save_file, mode='wb') as f:
            f.write(content)
    else:
        url = 'http://images.cocodataset.org/zips/train2017.zip'
        
        save_file = Path(args.download_dir, Path(url).name)
        with requests.get(url, stream=True) as r:
          with open(save_file, mode='wb') as f:
              for chunk in r.iter_content(chunk_size=1048576):
                  f.write(chunk)

# --- main routine ---
if __name__=='__main__':
    main()

