#! /bin/bash

# --- 必要なパッケージのインストール
pip3 install tfds-nightly==4.4.0.dev202201220107 tensorflow==2.8.0rc0

# --- 関数: version ---
function version {
    echo "$(basename ${0}) version 0.0.1 "
}

# --- 関数: usage ---
function usage {
    cat <<EOF
$(basename ${0}) is a tool for save images from tensorflow_dataset

Usage:
    $(basename ${0}) [command] [<options>]

Options:
    --log, -l         specify log file
    --version, -v     print $(basename ${0}) version
    --help, -h        print this
EOF
}

# --- 引数処理 ---
while [ $# -gt 0 ];
do
    case ${1} in
        --version|-v)
            version
            exit
        ;;
        
        --help|-h)
            usage
            exit
        ;;
        
        --log|-l)
            LOG_FILE=${2}
            shift
        ;;

        *)
            echo "[ERROR] Invalid option '${1}'"
            usage
            exit 1
        ;;
    esac
    shift
done

if [ ! ${LOG_FILE} ]; then
    LOG_FILE="download_images.log"
fi

python download_images.py --dataset imagenet_v2 > ${LOG_FILE}

