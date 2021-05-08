#! /bin/bash

git clone https://github.com/google-research/google-research.git
cd google-research/tabnet

python3 download_prepare_covertype.py
python3 experiment_covertype.py

