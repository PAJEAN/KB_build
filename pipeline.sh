#!/bin/bash

# Name of your file.
f_name="Data/phrases.txt"

python sentence_processing.py $f_name
java -Xmx512m -jar reverb-latest.jar Data/Phrases/phrases_normaliser.txt > Data/Reverb/reverb.tsv
# Don'f forget to precise your predicats in the follow script.
python extract_relation_reverb.py
python KB_builder.py

# Visualisation.
#dot -Tpdf Data/Graphes/kb.dot -o graph_file.pdf
#evince graph_file.pdf
