#!/bin/sh

python3 ./core/ner_text_mining.py > result_step_001.csv
python3 ./core/lematization.py > result.csv