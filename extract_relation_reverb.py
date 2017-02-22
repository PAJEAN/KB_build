#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

###### ###### ###### ###### Documentation ###

# TITLE # Extraction et normalisation des relations de reverb.

# Description #
	# Extrait les relations de ReVerb.
	# Permet de normaliser les phrases.
	# Supprime les relations avec un sujet ou un objet (#)

###### ###### ###### ###### Input(s) & Output(s) ###

# Inputs #
###
f_name = "Data/Reverb/reverb.tsv"
fichier_relations = open(f_name, "r").readlines()
###

# Ouputs #
###
out_f_name = "Data/Reverb/reverb_normaliser.tsv"
sortie = open(out_f_name, "w")
pos_out_f_name = "Data/Reverb/reverb_pos_normaliser.tsv"
sortie_pos = open(pos_out_f_name, "w")
###

###### ###### ###### ###### Parameters ###
###
normalization = 1
predicats = ["born", "bear"]
###

###### ###### ###### ###### Functions ###
###
###

###### ###### ###### ###### Program ###
###

if len(predicats) > 0:
	pattern = ""
	for p in range(len(predicats)):
		pattern += predicats[p]
		if p != (len(predicats)-1):
			pattern += "|"
	
	print("\nPrédicats: "+pattern+"\n")
	pattern_predicat = re.compile(pattern)

	print("Initializing formatting ReVerb data.")

	id_relation = 0
	for phrase in fichier_relations:
		if normalization == 1:
			subs = []
			# Permet de supprimer les caracteres non ASCII.
			for line in enumerate(phrase):
				if ord(line[1]) > 127:
					subs.append(line[0])
		
			if len(subs) > 0:
				phrase_list = list(phrase)
				for i in subs:
					phrase_list[i] = " "
				phrase = ''.join(phrase_list)
			
		phrase = phrase.encode("utf8")
		
		# relation[5] = start suj.
		# relation[6] = end suj (-1).
		# relation[7] = start predicat.
		# relation[8] = end predicat (-1).
		# relation[9] = start obj.
		# relation[10] = end obj (-1).
		
		# POS = # Sujet = relation[-5].
		# Sujet = relation[-3].
		# Predicat = relation[-2].
		# Objet = relation[-1].	
		relation = phrase.strip().split("\t")
		
		# Recherche predicat.		
		re_predicat = pattern_predicat.findall(relation[-2])
		
		if relation[-3] != "#" and relation[-1] != "#" and len(re_predicat) > 0:
			# Les deux entites
			sortie.write(str(id_relation)+"\t"+relation[-3]+"\t"+relation[-2]+"\t"+relation[-1]+"\n")
			
			pos = relation[-5].split()
			suj_pos = pos[int(relation[5]): int(relation[6])]
			predicat_pos = pos[int(relation[7]): int(relation[8])]
			obj_pos = pos[int(relation[9]): int(relation[10])]
			
			sortie_pos.write(str(id_relation)+"\t"+" ".join(suj_pos)+"\t"+" ".join(predicat_pos)+"\t"+" ".join(obj_pos)+"\n")
			
			id_relation += 1
		
print("Done formatting.")














