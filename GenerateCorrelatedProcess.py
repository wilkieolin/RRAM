# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 13:28:14 2018

@author: Sarah Rafiq
"""


import random
import math
from random import choices
import numpy as np

"""---------Latest Generator--------------------"""
def newGen(database,k,c,uc):
    np.random.seed(8)
    random.seed(8)
    p1=0.5
    q1=1-p1

    y=np.zeros((c,k),dtype=int)
    
    corr=0.5

    P11=p1+(corr**(0.5))*q1
    P10=p1*(1-corr**(0.5))
    P0=1-P11-P10

    Xr=np.random.binomial(1,0.5,k)
    print('\n Xr=',Xr)
    #correlated data
    for j in range(c): 
        for i in range(k):
            if Xr[i]==1:
                X1=np.random.binomial(1,P11)
                y[j,i]=X1
            elif Xr[i]==0:
                X1=np.random.binomial(1,P10)
                y[j,i]=X1
            else:
                X1=np.random.binomial(1,P0)
                y[j,i]=X1

    print('correlated',y,np.corrcoef(y))

    """z=np.zeros((uc,k),dtype=int)     
    for j in range(uc):
        for i in range(k):
            z[j,i]=random.randint(0,1)
            
    print('\n z',np.corrcoef(z)) """
    
    z=np.zeros((uc,k),dtype=int)
       
    for i in range(uc):  
        r0=random.uniform(0,0.05)
        r=np.random.binomial(1,r0,k)      
        z[i]=r
    
    for i in range(c):
        database[i]=y[i]
    for i in range(uc):
        database[i+c]=z[i]

    print('\n database=',database, np.corrcoef(database))
    
    a=np.zeros((c+uc,c+uc),dtype=int)
    a=np.corrcoef(database)
    newData=database
      
    #to make sure it is uncorrelated data
    for i in range(uc):
        for j in range(uc):
                  
            if a[i+c,0]!=1 and a[i+c,0]>0:
                
                b=np.corrcoef(newData)
                while b[i+c,0]>0:
                    newData[i+c]=np.random.binomial(1,0.2,k)
                    b=np.corrcoef(newData)
                    print('in while loop',b)
    
    #print('database',database,'\n  and newData',newData,np.corrcoef(newData))
    
    return newData

#database=np.zeros((10,5),dtype=int)  #testing
#print(newGen(database,5,4,6))



"""-----------------Random generator 1---------------------------"""
def generate_random(database):
    
    #used random.choices to set probability,
    #but the plot showed not all the correlated ReRAMs had the same conductance at the end
    
    array=np.zeros((10,10),dtype=int)
    
    population = [1,0]
    weights = [0.1, 0.9]
    
    for i in range(10):
        random.seed( 2 )   #3 1's
        correlated_samples_Nc=choices(population, weights, k=10)
        for j in range(10):
            r=0
            if correlated_samples_Nc[j]==1:
                r+=1
    #print('r before',r)
        while r>=2 or r==0:
            correlated_samples_Nc=choices(population, weights, k=10)
            r=0
            for j in range(10):
                if correlated_samples_Nc[j]==1:
                    r+=1
            if r==1 and r!=0:
                break
            
    #print('r',r)
        array[i]=correlated_samples_Nc

    
    #uncorrelated processes, array y
    y=np.zeros((15,10),dtype=int)
        
    """for i in range(15):
        r=random.randint(2,5)
        weight2=[r*0.1,1-(r*0.1)]
        y[i]=choices(population, weight2, k=10) """
        
    for i in range(15):
        x=random.expovariate(0.4)
        while x>5 or x<2:
            x=random.expovariate(0.4)
        
        weight2=[x/10,1-(x/10)]
        y[i]=choices(population, weight2, k=10)
        
    for i in range(10):
        database[i]=array[i,:]

    for i in range(15):
        database[i+10]=y[i,:]
    
    return database


"""----------------Random generator 2--------------------------"""
def generate_random_seed(database,k,c,uc):
    
    arr=np.zeros((c,k),dtype=int)
    
    random.seed(5)
    np.random.seed( 11 )   #3 1's
    
    for i in range(k):  #gotta generate 10 k(iteration) values
        r=np.random.binomial(1,0.5)
        print("Random number with seed 3 : ", r)
        arr[:,i]=r
    """for i in range(c):  #gotta generate 10 k(iteration) values
        r=np.random.binomial(1,0.5,k)
        print("Random number with seed 3 : ", r)
        arr[i]=r
    
    for i in range(c):  #gotta generate 10 k(iteration) values
        #r=random.randint(0,1)
        r=np.random.binomial(1,0.6,k)
        print("Random number with seed 3 : ", r)
        arr[i]=r
        
    arr1=np.zeros((4,10),dtype=int)    
    #random.seed(3)
    for i in range(10):
        #random.seed( 2 )
        #r=random.randint(0,1)
        r=np.random.binomial(1,0.5)
        #print("Random number with seed 3 : ", r)
        arr1[:,i]=r   """  
        
   
    #Uncorrelated array y  
    y=np.zeros((uc+c,k),dtype=int)
    population = [1,0]
    
    for i in range(c+uc):  
        r0=random.uniform(0,0.05)
        r=np.random.binomial(1,r0,k)      #gives probability 0=<P(X=1)<=0.3
        y[i]=r
        
    """doesnt work, tried to set seed with random numbers 
    unCorrelated=np.zeros((15,10),dtype=int)
    
    seed=random.randint(3,8)
    
    for i in range(15):
        seed=random.randint(3,8)
        random.seed( seed )
        r=random.randint(0,1)
        print("Random number with seed",seed,":", r)
        unCorrelated[i,:]=r

    y=unCorrelated.T
    print('uncorrelated array ',y) """
    
    #putting correlated array (code at top) and uncorelated array 'y' into database
    for i in range(c+uc):
        database[i]=y[i,:]
        
        
    for i in range(c):
        x=c-1
        if i!=0 and i!=(c-1):
            database[2*i+4]=arr[i,:]
        elif i==0:
            database[2]=arr[i,:]
        elif i==x:
            database[22]=arr[i,:]
    """for i in range(c-4):
        database[i+4]=arr1[i,:]"""

    
    
    return database

"""To see plot, please change func. name in line 70 of analysingSoftware and run Main_with_correlation """

"""If you want to run this file only, use the code below: (just call the function you want to test), gives an array. 
"""
