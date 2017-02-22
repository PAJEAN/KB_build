#!/bin/python
# -*- coding:utf-8 -*-
import sys

if len(sys.argv) <= 1:
	exit(0)

###### ###### ###### ###### Documentation ###

# TITLE # Suppression d'éléments dans les phrases.

# Description #
	# Permet de supprimer des éléments indésirables dans les phrases.

###### ###### ###### ###### Input(s) & Output(s) ###

# Inputs #
###
f_name = sys.argv[1]
###

# Ouputs #
###
out_f_name = "Data/Phrases/phrases_normaliser.txt"
out = open(out_f_name, "w")
###

###### ###### ###### ###### Parameters ###
###
###

###### ###### ###### ###### Functions ###
###

def normalisation(text):
	phrase = ""
	for s in text:
		if not s in [","]:
			phrase += s
	return phrase

###

###### ###### ###### ###### Program ###
###

with open(f_name) as d_file:
	lignes = d_file.readlines()
	phrases = []
	for ligne in lignes:
		phrases.append(normalisation(ligne.strip()))
for phrase in phrases:
	out.write(phrase+"\n")

###
