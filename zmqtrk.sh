#!/bin/bash
#source ~/anaconda3/etc/profile.d/conda.sh
#eval "$(conda shell.bash hook)"
#conda activate py3
source ~/.bashrc
workon py3
cd /usr/local/lib/zmqtracker
python3 zmq_tracker.py -c stoic.json
