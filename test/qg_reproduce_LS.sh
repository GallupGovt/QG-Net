#!/usr/bin/env bash
mkdir "$1"/test/attention_visualizations_LSTM_attn
nbest=10
num_sent=1
beam_size=15
debug='False'
selection_criterion='NLL'
model_dir="test/testinput"
model="QG-Net.pt"
alpha=0.2
beta=0.2

python3.6 OpenNMT-py/generate.py \
-model $model_dir/$model \
-src $model_dir/input.txt \
-output "$2"/output_questions_$model.txt \
-dynamic_dict \
-verbose -batch_size 1 -gpu 0 -beam_size $beam_size -replace_unk -n_best $nbest \
-alpha $alpha -beta $beta \
-attn_vis
