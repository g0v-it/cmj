import numpy as np
import copy

class MajorityGrade:
	
	def __init__(self,score,find_median=-1):
		
		if find_median==-1:
			find_median=1+np.sum(score)/2
		
		conta=0
		i=0
		self.p=0
		self.q=0
		self.sgn = 0
		self.score=score
		
		while conta<find_median and i<len(score):
			conta += score[i]
			if conta<find_median:
				self.p += score[i]
			i += 1

		self.alpha= i-1
		
		while i<len(score):
			self.q += score[i]
			i += 1
		
		if self.p>self.q:
			self.sgn=1
		elif self.p<self.q:
			self.sgn=-1
		
		#print(self)
	'''
	Clona l'istanza diminuendo di una unita la mediana 
	'''
	def reduce_clone(self):
		temp=copy.deepcopy(self.score)
		temp[self.alpha] -= 1
		return MajorityGrade(temp)
	
	def __str__(self):
		return str(self.score)+" ("+str(self.p)+","+str(self.alpha)+" "+str(self.sgn)+","+str(self.q)+")"
	
	def __eq__(self,other):
		return (self.alpha==other.alpha and self.sgn==other.sgn and self.p==other.p and self.q==other.q)
	
	def __ne__(self,other):
		return not(self==other)
	
	def __lt__(self, other):
		return (self != other and not self > other)
			
	def __gt__(self, other):
		if self.alpha==other.alpha:
			if self.sgn!=other.sgn:
				return self.sgn>other.sgn
			elif self.sgn==1:
				return (self.p>other.p or (self.p==other.p and self.q<other.q))
			elif self.sgn==0:
				return (self.p>other.p)
			elif self.sgn==-1:
				return (self.q<other.q or (self.q==other.q and self.p>other.p))
		else:
			return self.alpha<other.alpha