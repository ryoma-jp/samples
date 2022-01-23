#! /bin/bash

# --- 環境設定 --
SCRIPT_DIR=$(cd $(dirname $0); pwd)

# --- デフォルト値 --
DEFAULT_DATASET="imagenet_v2"
DEFAULT_DATASET_DIR="_download"
DEFAULT_IMAGE_DIR="_images"
DEFAULT_LOG_FILE="download_images.log"

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
    --dataset         specify dataset name(ex: cifar10, mnist, imagenet_v2, ...)
                      see https://www.tensorflow.org/datasets/catalog/overview#image_classification
                      default: ${DEFAULT_DATASET}
    --dataset_dir     specify directory to save dataset
                      default: ${DEFAULT_DATASET_DIR}
    --image_dir       specify directory to save images
                      default: ${DEFAULT_IMAGE_DIR}
    --log, -l         specify log file
                      default: ${DEFAULT_LOG_FILE}
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
        
        --dataset)
            DATASET=${2}
            shift
        ;;

        --dataset_dir)
            DATASET_DIR=${2}
            shift
        ;;

        --image_dir)
            IMAGE_DIR=${2}
            shift
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

if [ ! ${DATASET} ]; then
    DATASET=${DEFAULT_DATASET}
fi
if [ ! ${DATASET_DIR} ]; then
    DATASET_DIR=${DEFAULT_DATASET_DIR}
fi
if [ ! ${IMAGE_DIR} ]; then
    IMAGE_DIR=${DEFAULT_IMAGE_DIR}
fi
if [ ! ${LOG_FILE} ]; then
    LOG_FILE=${DEFAULT_LOG_FILE}
fi

python ${SCRIPT_DIR}/download_images.py \
    --dataset ${DATASET} \
    --dataset_dir ${DATASET_DIR} \
    --image_dir ${IMAGE_DIR} \
    > ${LOG_FILE}

