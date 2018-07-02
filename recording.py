
import numpy as np
import matplotlib.pyplot as plt

a=np.load('recording.npz')
print(a['arr_0'], a['arr_1'])
#print('\n', len(a['arr_1']), a['arr_1'][1552])

t=0.03    #time interval in seconds
samples=(60)/t   #number of time intervals
database=np.zeros((25,int(samples)),dtype=int)

def getSamples():
        return samples

def spikeData(data):
    
    def pair(t0,k):
        for i in range(4):     #compare neuron 0 with the other 4 neurons
            if data[0,t0]==1 and data[(i+1)*5+(i+1),t0]==1:
                data[i+1,t0]=1
        #if data[0,t0]==1 and data[6,t0]==1:
            #print(a['arr_1'][k-1],a['arr_1'][k])
        
        for i in range(3):       #compare neuron 1 with neurons 2,3,4
            if data[6,t0]==1 and data[(i+2)*5+(i+2),t0]==1:
                data[i+7,t0]=1
        for i in range(2):       #compare neuron 2 with neurons 3,4
            if data[12,t0]==1 and data[(i+3)*5+(i+3),t0]==1:
                data[i+13,t0]=1
        if data[18,t0]==1 and data[24,t0]==1:  #compare neurons 3 and 4
            data[19,t0]=1

    k=0
    for i in range(int(samples)):                  #i is time interval 
        while i==1 and 0<a['arr_1'][k]<i*t:
            data[a['arr_0'][k]*5+a['arr_0'][k],i]=1
            k+=1
            #print(i,k,a['arr_0'][k-1])
            pair(i,k-1)
        while i!=1 and (i-1)*t<a['arr_1'][k]<i*t and k<(len(a['arr_0'])-1): 
            data[a['arr_0'][k]*5+a['arr_0'][k],i]=1
            k+=1
            #print(i,k,a['arr_0'][k-1])
            pair(i,k-1)
        while i==samples and k<(len(a['arr_0'])):
            if (i-1)*t<a['arr_1'][k]<i*t:
                data[a['arr_0'][k]*5+a['arr_0'][k],i]=1
                k+=1
                #print(i,k,a['arr_0'][k-1])
                pair(i,k-1)

    
    """print(np.shape(data))
    for i in range(50):
        f=data[:,i+3]
        print(np.reshape(f,(5,5))) """
        
    return data

#print(spikeData(database))

"""d = dict(zip(("data1A","data1B"), (a[k] for k in a)))
d = dict(zip(("data1{}".format(k) for k in a), (a[k] for k in a)))
print(a.keys(),'\n', a.f.arr_0, '\n', a.f.arr_1) """