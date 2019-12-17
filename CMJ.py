from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from MajorityGrade import MajorityGrade

class MultiWinner:
	
	def __init__(self,voters,candidates,pref_order,k):
		self.voters=np.array(voters)
		self.candidates=np.array(candidates)
		self.pref_order=np.array(pref_order)
		self.k=k
		
		self.n_voters=len(self.voters)
		self.n_candidates=len(self.candidates)
		self.n_grades=len(self.pref_order[0])
		
	'''
	Compute clusters given the maximal number of clusters
	'''
	def clusterize(self, max_cluster):
		p=1/max_cluster

		n_cluster=1
		backtracking=[]
		continua = True
		#
		#Aumento il numero di cluster fino a trovare il numero cluster più piccolo che non può eleggere
		#neanche un candidato
		#
		while(n_cluster<= self.k and continua==True):
			#Creazione dei cluster
			kmeans = KMeans(n_cluster, random_state=0).fit_predict(self.voters)
			#print(kmeans)
			#Verifico se i cluster hanno tutti dimensione minima per eleggere almeno un candidato
			for i in range(n_cluster):
				temp_p=len(np.where(kmeans==i)[0])
				print("Dimensione cluster: ",n_cluster, temp_p,self.n_voters,p,temp_p/(self.n_voters * p))
				#print("Dimensione cluster: ", temp_p/(self.n_voters * p))
				if(temp_p/(self.n_voters * p)<1.):
					continua=False

			#se tutti i cluster hanno dimensione minima provo a suddividere lo spazio dei votanti
			if continua:
				backtracking=kmeans
				n_cluster += 1
			else:
				n_cluster -= 1

		if n_cluster>self.k : 
			n_cluster=self.k
		'''
		Restituisce:
		backtracking	una lista che descrive per ogni votante il cluster di appartenenza
		n_cluster		il numero di cluster formati
		'''	
		return backtracking, n_cluster
	
	def compute_scores(self, indexes):
		
		score=np.zeros((self.n_candidates, self.n_grades))
		
		for voter in indexes:
			for candidate in range(len(self.voters[voter])):
				#print(cluster,candidate,self.voters[voter][candidate])
				#print(self.voters[voter][candidate])
				score[candidate][self.voters[voter][candidate]] += 1
		
		return score
		
	def compute_majority_grades(self, backtracking, n_cluster, score=[]):
		if score==[]: 
			score=np.zeros((n_cluster, self.n_candidates, self.n_grades))
			
		voters_per_cluster = np.zeros(n_cluster)
		median_per_cluster = np.zeros((n_cluster, self.n_candidates))
		#majority_grades = np.zeros((n_cluster, self.n_candidates, 3))

		#
		#Computo il punteggio per ogni candidato
		#
		for cluster in range(n_cluster):
			cluster_indexes=np.where(backtracking==cluster)[0]
			voters_per_cluster[cluster]=len(cluster_indexes)
			
			#print("Prima ",score[cluster])
			score[cluster]=score[cluster]/voters_per_cluster[cluster]
			#print("Dopo ",score[cluster])
			
			
		#print("Tutti ",score)
		
		
		
	def compute_medians(self, backtracking, n_cluster):
		
		#backtracking, n_cluster = self.clusterize()
		
		#Un array per ogni candidato in ogni cluster
		#print(n_cluster, self.n_candidates, self.n_grades)
		#print(n_cluster, self.n_candidates, self.n_grades)
		#score=np.zeros((n_cluster, self.n_candidates, self.n_grades))
		score=np.zeros((n_cluster, self.n_candidates, self.n_grades))
		voters_per_cluster=np.zeros(n_cluster)
		median_per_cluster=np.empty((n_cluster, self.n_candidates), dtype=MajorityGrade)

		#
		#Computo il punteggio per ogni candidato
		#
		for cluster in range(n_cluster):
			cluster_indexes=np.where(backtracking==cluster)[0]
			voters_per_cluster[cluster]=len(cluster_indexes)
			
			score[cluster]=self.compute_scores(cluster_indexes)
			'''for voter in cluster_indexes:
				for candidate in range(len(self.voters[voter])):
					#print(cluster,candidate,self.voters[voter][candidate])
					#print(self.voters[voter][candidate])
					score[cluster][candidate][self.voters[voter][candidate]] += 1'''


		#
		#Trovo la mediana per ogni candidato
		#	
		for cluster in range(n_cluster):
			#
			# La mediana è data dal valore a metà dato il numero di votanti
			#
			find_median=1+voters_per_cluster[cluster]/2
			print()
			for candidate in range(self.n_candidates):
				'''conta=0
				i=0
				while conta<find_median and i<self.n_grades:
					point = score[cluster][candidate][i]
					conta += point
					i += 1

				i -= 1
				median_per_cluster[cluster][candidate]=i'''
				median_per_cluster[cluster][candidate]=MajorityGrade(score[cluster][candidate],find_median)
				print(candidate,". ",median_per_cluster[cluster][candidate])
		
		'''
		Restituisce:
		median_per_cluster.argsort()	ranking sui candidati ###DA SISTEMARE CON TIEBREAK
		voters_per_cluster				numero di votanti per ogni cluster 
		1./self.k						costo candidato
		score							punteggio assegnato ad ogni candidato 
		'''	
		return median_per_cluster.argsort(), voters_per_cluster, 1./self.k, score
	
	'''
	Compute clusterized majority judgement
	'''
	def cmj(self):
		
		remaining_candidates = self.k
		remaining_cluster = self.k
		
		winners=[]
		
		while remaining_cluster > 1:
			# Clusterizza i votanti
			p=1/remaining_candidates
			backtracking, n_cluster = self.clusterize(remaining_cluster)

			# Calcola le mediane sui cluster 
			ranking, weights, _, real_score = self.compute_medians(backtracking, n_cluster)

			print("n_cluster: ",n_cluster," ranking: ",ranking)
			#self.compute_majority_grades(backtracking, n_cluster, real_score)
			# Calcola quanti candidati può eleggere ogni cluster
			#print(weights,p)
			#print(real_score)
			candidate_per_cluster = np.floor(weights/self.n_voters/p)
			candidate_per_cluster=candidate_per_cluster.astype(int)

			for cluster in range(len(candidate_per_cluster)):
				#Take the number of candidate to elect for each cluster
				c=candidate_per_cluster[cluster]
				# For each cluster select due number of candidates to elect
				# In case of tie no other candidate is elected
				for winner in range(c):
					#print(ranking[cluster])
					#print(ranking[cluster][winner])
					
					# Reduce the number of remaining number of candidates to elect and thus 
					# the maximal number of clusters
					#Indice rovesciato perchè il ranking va del meno preferito al più preferito
					i=len(ranking[cluster])-1-winner
					print(c," ",winner," ",ranking[cluster][i])
					if ranking[cluster][i] not in winners:
						winners.append(ranking[cluster][i])
						remaining_candidates -= 1
						
			# Se il numero di candidati è minore dei cluster allineo i conteggi			
			if remaining_candidates < remaining_cluster: 
				remaining_cluster=remaining_candidates
			else:
				remaining_cluster -= 1
				
			
			print("#: ",candidate_per_cluster," #left: ",remaining_candidates, " #winners: ",winners)
		
		#Se rimangono candidati da eleggere alla fine, li scelgo dal ranking di MJ su un cluster
		if remaining_candidates>=1 :
			backtracking, n_cluster = self.clusterize(remaining_cluster)

			# Calcola le mediane sui cluster 
			ranking, weights, _, real_score = self.compute_medians(backtracking, n_cluster)
			#Indice rovesciato perchè il ranking va del meno preferito al più preferito
			i=len(ranking[0])-1
			print(ranking)
			while remaining_candidates>0:
				if ranking[0][i] not in winners:
					winners.append(ranking[0][i])
					remaining_candidates -= 1
				i -= 1

				
		print("#: ",candidate_per_cluster," #left: ",remaining_candidates, " #winners: ",winners)
		
		return ranking, weights, p, real_score, winners
		