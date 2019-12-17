import pandas as pd
import numpy as np

from preflibtools import generate_profiles as gp
from preflibtools import io

def gen_profile(ncand, nvoter, model):
	cmap = gp.gen_cand_map(ncand)
	
	profile=np.ndarray(shape=(0,ncand), dtype="int")
	
	if model == 1:
		# Generate an instance of Impartial Culture
		rmaps, rmapscounts = gp.gen_impartial_culture_strict(nvoter, cmap)
	elif model == 2:	
		# Generate an instance of Single Peaked Impartial Culture
		rmaps, rmapscounts = gp.gen_single_peaked_impartial_culture_strict(nvoter, cmap)
	elif model == 3:	
		# Generate an instance of Impartial Aynonmous Culture
		rmaps, rmapscounts = gp.gen_impartial_aynonmous_culture_strict(nvoter, cmap)
	elif model == 4:	
		# Generate a Mallows Mixture with 5 random reference orders.					
		rmaps, rmapscounts = gp.gen_mallows_mix(nvoter, cmap, 5)
	elif model == 5:	
		# Generate a Mallows Mixture with 1 reference.					
		rmaps, rmapscounts = gp.gen_mallows_mix(nvoter, cmap, 1)
	elif model == 6:
		#We can also do replacement rates, recall that there are items! orders, so 
		#if we want a 50% chance the second preference is like the first, then 
		#we set replacement to items!
		rmaps, rmapscounts = gp.gen_urn_strict(nvoter, math.factorial(ncand), cmap)	
	else:
		print("Not a valid model")
		exit()
	
	for i in range(len(rmapscounts)):
		v=io.rankmap_to_order(rmaps[i])
		v=np.tile(v,(rmapscounts[i],1))
		profile=np.vstack((profile,v))
		
	return profile