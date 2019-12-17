import pandas as pd
#from sklearn.cluster import KMeans
import numpy as np
import utils

from CMJ import MultiWinner

#Numero di vincitori
k=2
n_voters=100
v=pd.read_csv("data/votanti3.csv", delimiter=";",header=None)
c=pd.read_csv("data/candidati3.csv", delimiter=";",header=None)
total_order=pd.read_csv("data/total_order3.csv", delimiter=";",header=None)
print(v)
#Cambio le etichette con numeri per una gestione migliore
map_dict={}
for i in total_order:
	map_dict[total_order[i][0]]=i
print(map_dict)

for column in v:
	v[column]=v[column].map(map_dict)


#np.random.seed(0)
'''v=np.random.randint(6, size=(n_voters,9))
print(v)
v=utils.gen_profile(len(c),n_voters,1)
v=v-1'''
print(v)

cmj = MultiWinner(v,c,total_order,k)
#backtracking, n_cluster = cmj.clusterize()

#print(backtracking, n_cluster)

'''#Numero di votanti per eleggere un candidato
p=1/k

n_cluster=1
backtracking=[]
continua = True

#
#Aumento il numero di cluster fino a trovare il numero cluster più piccolo che non può eleggere
#neanche un candidato
#
while(n_cluster<= k and continua==True):
	#Creazione dei cluster
	kmeans = KMeans(n_cluster, random_state=0).fit_predict(v)
	print(kmeans)
	#Verifico se i cluster hanno tutti dimensione minima per eleggere almeno un candidato
	for i in range(n_cluster):
		temp_p=len(np.where(kmeans==i)[0])
		print(temp_p)
		if(temp_p/(len(v)*p)<0.75):
			continua=False
			
	#se tutti i cluster hanno dimensione minima provo a suddividere lo spazio dei votanti
	if continua:
		backtracking=kmeans
		n_cluster += 1
	else:
		n_cluster -= 1

if n_cluster>k : 
	n_cluster=k

#Un array per ogni candidato in ogni cluster
score=np.zeros((n_cluster, len(c), len(total_order.values[0])))
voters_per_cluster=np.zeros(n_cluster)
median_per_cluster=np.zeros((n_cluster, len(c)))

#
#MAJORITY JUDGEMENT
#
v=np.array(v)
c=np.array(c)
total_order=np.array(total_order)
n_voters=len(v)
n_candidates=len(c)
n_grades=len(total_order[0])

#
#Computo il punteggio per ogni candidato
#
for cluster in range(n_cluster):
	cluster_indexes=np.where(backtracking==cluster)[0]
	voters_per_cluster[cluster]=len(cluster_indexes)
	
	for voter in cluster_indexes:
		for candidate in range(len(v[voter])):
			score[cluster][candidate][v[voter][candidate]] += 1
			

#
#Trovo la mediana per ogni candidato
#	
for cluster in range(n_cluster):
	find_median=1+voters_per_cluster[cluster]/2
	
	for candidate in range(n_candidates):
		sum=0
		i=0
		while sum<find_median and i<n_grades:
			point = score[cluster][candidate][i]
			sum += point
			i += 1
		
		i -= 1
		median_per_cluster[cluster][candidate]=i
'''

score, weights, p, real_score, winners = cmj.cmj()

print([chr(i+65) for i in score[0]])
#print(real_score,score,weights, k, p, winners)

	
