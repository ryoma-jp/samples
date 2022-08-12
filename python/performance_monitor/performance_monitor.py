import argparse
import psutil

def ArgParser():
    """ArgParser

    引数処理

    Returns:
        ロードした引数

        - args(namespace object): 引数オブジェクト
    """
    parser = argparse.ArgumentParser(description='システムモニタリングのサンプル',
                formatter_class=argparse.RawTextHelpFormatter)

    # --- 引数を追加 ---
    parser.add_argument('--log_file', dest='log_file', type=str, default=None, required=False, \
            help='モニタリング結果を保存するログファイルを指定する(*.csv)')
    parser.add_argument('--loop', dest='loop', action='store_true', required=False, \
            help='連続表示(1秒毎)する場合に指定')

    args = parser.parse_args()

    return args

def main():
    """main

    メイン処理

    Returns:
        なし
    """

    # --- 引数処理 ---
    args = ArgParser()
    print(f'args.log_file : {args.log_file}')
    print(f'args.loop     : {args.loop}')

    # --- システムモニタリング ---
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    virtual_memory = psutil.virtual_memory()

    cpu_num = len(cpu_percent)
    cpu_names = [f'cpu{x}[%]' for x in range(cpu_num)]

    utilities = cpu_names + ['memory[%]']
    utilities_str = ",".join(utilities)

    utility_vals = cpu_percent + [virtual_memory.percent]
    utility_vals_str = ",".join(map(str, utility_vals))

    if (args.loop):
        print('\n  *** Please Ctrl+C to stop monitoring ***\n')
    print(utilities_str)
    print(utility_vals_str)
    if (args.log_file is not None):
        with open(args.log_file, 'w') as f:
            f.write(f'{utilities_str}\n')
            f.write(f'{utility_vals_str}\n')

    while (args.loop):
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        virtual_memory = psutil.virtual_memory()
    
        utility_vals = cpu_percent + [virtual_memory.percent]
        utility_vals_str = ",".join(map(str, utility_vals))

        print(utility_vals_str)
        if (args.log_file is not None):
            with open(args.log_file, 'a') as f:
                f.write(f'{utility_vals_str}\n')

    return

if __name__ == '__main__':
    main()

