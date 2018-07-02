import numpy as np
import random
import matplotlib.pyplot as plt
import GenerateCorrelatedProcess as gen
import recording as rec



class analysing_software():
    def __init__ (self, maxrow, maxcol,C):
        
        self.maxrow=maxrow
        self.maxcol=maxcol
        #total number of process N
        self.N=self.maxrow*self.maxcol
        
        #array that hold value of all N processes at particular time k, same size as RRAM array
        self.y=np.zeros((self.maxrow,self.maxcol),dtype=int)
        
        
        #x is a database array that stores all N processes at total time instants k, N is row and k is column. kn helps iterating till k in next method. 
        self.k=2000
        self.c=4
        self.uc=25-self.c
        
        self.k0=int(rec.getSamples())
        self.kn=0   
        self.x=np.zeros((self.N,self.k),dtype=int)
        self.x1=np.zeros((self.N,self.k0),dtype=int)  #k0 is original 3000k database
        
        #momentum constant, I increased it because otherwise the Vpulse is too low to change resistance
        self.C=C
        
        self.array_read=np.zeros((self.maxrow,self.maxcol))
        
        self.number=np.zeros((self.maxrow,self.maxcol),dtype=int)
        self.n=0
        self.no=np.zeros((self.N,1),dtype=int)
        
    
    #this changes the value of all processes when k/kn is incremented        
    def array_at_time_k(self):
        """if self.k<=self.k0:
            if self.kn<self.k:
                for i in range(self.maxrow):
                    self.y[i,:]=self.x[0+self.maxrow*i:self.maxrow+self.maxrow*i,self.kn] 
        
                self.kn+=1"""
        if self.k<=self.k0:
            if self.kn<self.k:
                a=self.x[:,self.kn]
                self.y=np.reshape(a,(self.maxrow,self.maxcol))
                self.kn+=1
        
        return self.y
    
    #populate the database x (N,k), the x is an array, as the process (1D lists) are converted to array
    def generate_x(self):
         
        #size of x should be (25,any number of k)
        #gen.generate_random_seed(self.x1,self.k0,self.c,self.uc)
        """gen.newGen(self.x1,self.k0,self.c,self.uc)
        for i in range(self.N):
            for j in range(self.k):
                self.x[i,j]=self.x1[i,j] """
        rec.spikeData(self.x1)
        for i in range(self.N):
            for j in range(self.k):
                self.x[i,j]=self.x1[i,j]
        return self.x   
    
    
        
    #calculate momentum from array y at time k, used in interface to modulate Vpulse/pw
    def momentum(self):
        momentum=M(self.y,self.C,self.maxrow,self.maxcol)
        return momentum
    
    
    def check_row_col(self,row,col):
        try:
            if row<self.maxrow or col<self.maxcol:
                if self.y[row,col]==1:
                    return row,col
                else:
                    row=-1
                    col=-1
                    return row,col
        except KeyboardInterrupt:
            print('KeyboardInterrupt occured')
            
    def read_resistance(self, row,col,R):
        self.array_read[row,col]=R
        
    def getResistanceRead(self):
        return self.array_read
    
    def get_total_k(self):
        return self.k
        
    def conductancePlot(self):
        conductance=1/self.array_read
        print(frequency(conductance))
        y=plt.bar(frequency(conductance)[0], frequency(conductance)[1], 1*10**(-6), color="blue")
        plt.xlabel("Conductance (S)")
        plt.ylabel("No. of devices")
        return y
    
    def plotImage(self):
        plt.subplot(211)
        G=plt.imshow(1/self.array_read,vmin=1/40000,vmax=1/7000,origin='upper')
        plt.colorbar()
        plt.title('Conductance')
        plt.show() 
        
        plt.subplot(212)
        R=plt.imshow(self.array_read,vmin=7000,vmax=40000,origin='upper')
        plt.colorbar()       
        
        return G,R
    
    def numberOfOnes(self):
        for i in range(self.N):
            for j in range(self.k):
                if self.x[i,j]==1:
                    self.n+=1
            self.no[i]=self.n
            self.n=0
        
        for i in range(self.maxrow):
            self.number[i,:]=self.no[0+5*i:5+5*i,0]
        return self.number
                    
    
    def corr(self):
        return np.corrcoef(self.x)
    
    def getK0(self):
        return self.k0
    
        
        

        
def frequency(array):
    values, array = np.unique(array, return_inverse=True)
    return values, np.bincount(array.ravel())


        

#calculate momentum, counts how many 1's are in array y
def M(y,C,rmax,cmax):
    M=0
    for i in range(rmax):
        for j in range (cmax):
            if y[i,j]==1:
                M+=1
    momentum=C*M
    return momentum


#testing=analysing_software(2,2,0.2)    