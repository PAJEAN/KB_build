#!/bin/python
# -*- coding:utf-8 -*-
import re
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize 


###### ###### ###### ###### Documentation ###

# TITLE # Structuration des syntagmes.

# Description #
	# Structuration des syntagmes.

###### ###### ###### ###### Input(s) & Output(s) ###

# Inputs #
###
syntagm_file = "Data/Reverb/reverb_normaliser.tsv"
syntagm_pos_file = "Data/Reverb/reverb_pos_normaliser.tsv"
###

# Ouputs #
###
graph_file = "Data/Graphes/kb.dot"
###

###### ###### ###### ###### Parameters ###
###
###

###### ###### ###### ###### Functions ###
###

def getGeneralForms(ordering, w):
	s = set()
	s.add(w)
	if(w in ordering): s.update(ordering[w])
	return s

def abstract(ordering,syntagm):
	
	grams = syntagm.split()
	abstracted = []
	
	generalForms = []
	for w in grams:
		generalForms.append(getGeneralForms(ordering, w))
		
	queue = []
	for w in generalForms[0]:
		l = list()
		l.append((0,w))
		queue.append(l)
	
	
	while(len(queue) != 0):
		w = queue.pop(0)
		
		#print w
		depth = w[-1][0]
		if(depth+1 < len(grams)):
			for n in generalForms[depth+1]:
				wn = list(w)
				wn.append((depth+1,n))
				queue.append(wn)
		
		if(len(w) == len(generalForms)):
			#print "*** ",w
			form = w[0][1]
			for i in range(1,len(w)):
				form += " "+w[i][1]
			abstracted.append(form)
			
	return abstracted
				
		
def getDirectGeneralForm(grams):
	if(len(grams) == 1): return None
	grams.pop(0)
	return " ".join(grams)

# Linguistic & syntactic rules.
def invertedLocOf(t, pos):
	n = t
	n_pos = pos
	t = t.strip().split()
	pos = pos.strip().split()
	
	ofLoc = None
	# 1 to n pour l'id.
	for i in range(1,len(t)):
		if(t[i] == "of" and not(i == 0) and not(i == len(t)) ):
			ofLoc = i
			
	if(ofLoc != None):
		nsyntagm = ""
		nsyntagm_pos = ""
		for i in range(ofLoc+1,len(t)):
			nsyntagm += t[i]+" "
			nsyntagm_pos += pos[i]+" "
			
		for i in range(0,ofLoc):
			if not pos[i] in ["DT", "IN"]:
				nsyntagm += t[i]+" "
				nsyntagm_pos += pos[i]+" "
			
		n = nsyntagm.strip()
		n_pos = nsyntagm_pos.strip()

	return n, n_pos
		
def and_or(so, pos):
	# On récupère uniquement la partie après le and ou le or.
	spl_str = so.strip().split(" ")
	spl_str_pos = pos.strip().split(" ")
	s_nsyntagm = so
	s_nsyntagm_pos = pos
	
	ofLoc = None
	nsyntagm = []
	nsyntagm_pos = []
	
	nb_andOr = 0
	for i in range(0,len(spl_str)):
		if((spl_str[i] == "and" or spl_str[i] == "or") and not(i == 0) and not(i == len(spl_str)) ):
			ofLoc = i
			nb_andOr += 1
	if(ofLoc != None) and nb_andOr == 1:
		for i in range(ofLoc+1,len(spl_str)):
			nsyntagm.append(spl_str[i])
			nsyntagm_pos.append(spl_str_pos[i])
				
		s_nsyntagm = " ".join(nsyntagm)
		s_nsyntagm = s_nsyntagm.strip()
		s_nsyntagm_pos = " ".join(nsyntagm_pos)
		s_nsyntagm_pos = s_nsyntagm_pos.strip()

	return s_nsyntagm, s_nsyntagm_pos
	
def with_format(so, pos):
	# On récupère uniquement la partie avant le with.
	spl_str = so.strip().split(" ")
	spl_str_pos = pos.strip().split(" ")
	s_nsyntagm = so
	s_nsyntagm_pos = pos
	
	ofLoc = None
	nsyntagm = []
	nsyntagm_pos = []
	
	nb_andOr = 0
	for i in range(0,len(spl_str)):
		if((spl_str[i] == "with") and not(i == 0) and not(i == len(spl_str)) ):
			ofLoc = i
			nb_andOr += 1
	if(ofLoc != None) and nb_andOr == 1:
		for i in range(0,ofLoc):
			nsyntagm.append(spl_str[i])
			nsyntagm_pos.append(spl_str_pos[i])
				
		s_nsyntagm = " ".join(nsyntagm)
		s_nsyntagm = s_nsyntagm.strip()
		s_nsyntagm_pos = " ".join(nsyntagm_pos)
		s_nsyntagm_pos = s_nsyntagm_pos.strip()

	return s_nsyntagm, s_nsyntagm_pos

def pos_pattern(entity, pos):
	
	spl_pos = pos.split()
	spl_entity = entity.split()
	
	n_entity = []
	n_pos = []
	for i in range(len(spl_pos)):
		n_entity.append("")
		n_pos.append("")
	
	for i in reversed(range(len(spl_pos))):
		if not spl_pos[i] in ["DT","IN"]:
			n_entity[i] = spl_entity[i]
			n_pos[i] = spl_pos[i]
		else:
			break
	
	# The first word have to be a NN (NN, NNS, NNP).
	ok = 0
	if len(n_pos) > 0:
		m = re.compile("NN")
		f = m.findall(n_pos[(len(n_pos)-1)])
		if len(f) > 0:
			ok = 1
	
	# We do not consider a number (CD).
	if "CD" in n_pos:
		ok = 0
	
	if ok == 1:
		entity = " ".join(n_entity)
		entity = entity.strip()
		pos = " ".join(n_pos)
		pos = pos.strip()
	else:
		entity = ""
		pos = ""
	
	
	return entity, pos
	
def lemmatisation(entity):
	
	tokens = word_tokenize(entity)
	stemmer = WordNetLemmatizer()
	texts = [stemmer.lemmatize(word) for word in tokens]
	entity = " ".join(texts)
	return entity

def entities_normalization(entity, pos):
	
	entity = lemmatisation(entity)
	
	if "with" in entity.split():
		entity, pos = with_format(entity, pos)
	if "and" in entity.split() or "or" in entity.split(): 
		entity, pos = and_or(entity, pos)
	if "of" in entity.split():
		entity, pos = invertedLocOf(entity, pos)
		print entity
	
	entity, pos = pos_pattern(entity, pos)
	print entity, pos
	return entity

###

###### ###### ###### ###### Program ###
###

#entities_normalization("the establishment of the mature t cell phenotype", "DT NN IN DT JJ NNP NN NN")
#quit()

# Construction des syntagmes.
# Exemple : syntagms = ["Liver_Cancer", "Hepatite", "Quick Development"]

syntagms = [] 

pos = []
with open(syntagm_pos_file) as pos_file:
	pos = pos_file.readlines()

with open(syntagm_file) as f:
	
	sentences = f.readlines()
	for line in range(len(sentences)):
		
		s = sentences[line].strip()
		t = s.split("\t")
		s_pos = pos[line].strip()
		t_pos = s_pos.split("\t")
		

		if len(t) == 4:
			suj = t[1].strip()
			obj = t[3].strip()
			pos_suj = t_pos[1].strip()
			pos_obj = t_pos[3].strip()
			
			suj = entities_normalization(suj, pos_suj)
			obj = entities_normalization(obj, pos_obj)
			
			print suj+"\t"+obj
			
			# We consider only full relations.
			if len(suj) > 0 and len(obj) > 0:
				syntagms.append(suj)
				syntagms.append(obj)
				


ordering = {
	#"homeostasis" : ["property_of_a_system"]
	#"Acute_Disease" : ["Disease"],
	#"Cancer" : ["Acute_Disease"],
	#"Meningite" : ["Acute Disease", "Disease"],
	#"Reduction" : ["Modification"],
	#"Augmentation" : ["Modification"],
	#"Rapid" : ["[CUI:30]"],
	#"[CUI:30]" : ["[CUI:31]"],
	#"Quick" : ["[CUI:31]"],
	#"Renal" : ["organ-related"]
	#"Renal" : ["organ-related"]
}


"""
with open("Data/Ancestors/dbpedia_places_ancestors.csv") as f:
	for line in f:
		data = line.strip().split("\t")
		id_mesh = data[0]
		#id_mesh_ancestors = data[1].split(", ")
		id_mesh_ancestors = data[1].split(";")
		
		ordering[id_mesh] = id_mesh_ancestors
"""		
		
	


print "Building graph"
graph = {}

graph["[ROOT_SYNTAGME]"] = set()

for syntagm in syntagms:
	
	syntagm = syntagm.strip()
	print "syntagm:" ,syntagm


	grams = syntagm.split()

	print grams

	node_queue = [syntagm]

	graph[syntagm] = set()
	graph[syntagm].add("[ROOT_SYNTAGME]")

	while(len(node_queue) != 0):
		
		node = node_queue.pop(0)
		syntagm_node_grams = node.split()
		
		print "--------------------"
		print node
		print "--------------------"
		
		
		general_nodes = abstract(ordering,node)
		
		for general_node in general_nodes:
			
			if(node != general_node):
				#print "*** '",node,"' -> '",general_node,"'"
				graph[node].add(general_node)
				
				if(general_node not in graph): 
					node_queue.append(general_node)
					graph[general_node] = set()
					graph[general_node].add("[ROOT_SYNTAGME]")
				
		direct_general_form = getDirectGeneralForm(syntagm_node_grams)
		
		if(direct_general_form != None): 
				graph[node].add(direct_general_form)
				
				if(direct_general_form not in graph): 
					node_queue.append(direct_general_form)
					graph[direct_general_form] = set()
					graph[direct_general_form].add("[ROOT_SYNTAGME]")
		
		#print "direct general form: ",direct_general_form


# Transitive reduction to remove useless edges

nb_desc = {}

leaves = list()

for n in graph:

    if not n in nb_desc: nb_desc[n] = 0

    for a in graph[n]:
        if not a in nb_desc: nb_desc[a] = 1
        else: nb_desc[a] += 1

for n in nb_desc:
    if nb_desc[n] == 0: leaves.append(n)

print "leaves", len(leaves)

queue = leaves
propagated = {}
while(len(queue) != 0):
	
	
	n = queue.pop()
	if(not n in propagated): propagated[n] = set()
	propagated[n].add(n)
	toRemove = []
	#if(n not in graph): continue
	for p in graph[n]:
		nb_desc[p] -= 1
		if(not p in propagated): propagated[p] = set()
		
		inter = propagated[n].intersection(propagated[p])
		
		for i in inter: 
			if(i in graph and p in graph[i]):
				graph[i].remove(p)
				print "remove: ",i,"\t",p
			
		propagated[p].update(propagated[n])
			
		if(nb_desc[p] == 0):
			queue.append(p)


			

# Build graph 
# command dot -Tpdf graph_file -o graph_file.pdf 
with open(graph_file,"w") as output :
	output.write("digraph word_graph {\n \t rankdir=BT\n")
	for node in graph:
		for adj in graph[node]:
			output.write( "\t\""+node+"\" -> \""+adj+"\""+"\n")
	output.write("}\n")
	
###
