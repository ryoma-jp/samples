#! /bin/bash

echo `pwd`
python3 trainer/trainer.py --test_mode ResNet
#python3 -m pdb main.py --data_type ${DATA_TYPE} --dataset_dir ${dataset_dir} --model_type ${MODEL_TYPE}
