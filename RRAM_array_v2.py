# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 23:55:39 2018

@author: Sarah Rafiq
"""
"""Summary: 
Last time:
created and initialized array in class array;
calculated resistance change using RRAM model=dR/dt*pulse width; 
added an arbitrary current compliance Imax in SET;
last part of code is sequential access

New changes:
Raises error if voltage applied is negative.
Both read and write use boolean SR to switch polarity of voltage when needed
Read detected using voltage (Vtn<V<Vtp) and pulse_width, Set/Reset operated by voltage 
RRAM model is a class that uses Vtp and Vtn 
"""
 

#i would recommend to define rows and columns"

# lets call it RRAM_ARRAY_sim to identify it as a simulation
class RRAM_ARRAY_sim():
    
    def __init__(self, rowMax, colMax, ReRAM_model):
        # you have to define the array here, I renamed row and column so they represent the max Col. number
        self.rowMax=rowMax                    
        self.colMax=colMax
        self.RRAM=ReRAM_model      
        
        #Array in class            
        self.arr=[[self.RRAM.getInitRes() for j in range(self.colMax)] for i in range(self.rowMax)]
            
        #You should retrieve this from the RRAM model, it is property of ReRAM not the array
        
        #you handover the RRAM model to this class in during the class creation
        self.RRAM=ReRAM_model
        
    def show_R(self):
        print(str(self.arr))
    #you need to plug in the current even though you dont need it

        """Since Vpulse is always positive, lets switch the polarity when SR=0 (Reset)"""
    # I would use bool, it is either 0 or VDD
    def adjVolPol(self, SR,Vpulse):
        if SR:
            """Reset device so need to apply negative voltage"""
            return (Vpulse)
        else:
            Vpulse=Vpulse*(-1)
            return (Vpulse)

   
    def read_or_write(self,row,col,Vpulse,pulse_width, SR, MaxCur = 0):
        # again create a return value (it can be an error)
        # Check for negative values too as well as if it is a float Val
        """To check whether the row and column entered are valid or not"""
        
        if row>=self.rowMax:
            raise(MyError("Error: Row exceeded dimension of array"))
        
        elif col>=self.colMax:
            raise(MyError("Error: Column exceeded dimension of array"))
        
        elif row<0:
            raise(MyError("Error: Row must be positive integer")) 
        
        elif col<0:
            raise(MyError("Error: Column must be positive integer")) 
            
        elif pulse_width<(5*10**(-9)):
            raise(MyError("Error: Pulse width is less than 5ns")) 
        
        else:
            
            if Vpulse<0:
                raise(MyError("Applied voltage must be positive"))
               
            elif Vpulse>3.3:
                raise(MyError("Applied voltage cannot exceed 3.3 V"))
                
            elif 0<Vpulse<=3.3:
                #Vpulse is positive, so switch polarity when required(Vreset, maybe Vread)
                Vpulse = self.adjVolPol(SR,Vpulse)
                
                #You need to verify that the voltage is within the threshold voltage
                if self.RRAM.getVtn() < Vpulse < self.RRAM.getVtp() and pulse_width > 200*(10**(-9)):
                    """Read pulse is received, outputs current at that row and column"""
                    # not neccarily, Vpulse needs to be below a certain value too
                    # don't define values in your class. These should be defined during __init__ if at all. 
                    # you have to return a value (either R or I, up to you)
                    I=Vpulse/self.arr[row][col]
                    #print('Current read at R'+str(row)+str(col)+':'+str(I)+'A') #prints current at that row and column
                    print('Resistance read: '+str(self.arr[row][col])+' ohm')
                    return self.arr[row][col]
                    
                else:
                    """SET/RESET Operation """
                    # why is SR a list, Binary vales (1 or 0 or in voltages 0V or VDD) should always be boolean?
                    # throw an exception if Vpulse is negative
                    #Set and Reset operation are basically the same, you need to adjust Vpulse to be positive or negative in dependence of S/R
                    #Follow the following procedure: handle the voltage - print Set/Reset status - get R change from the model - change R - print new R
                    # Vpulse is only positive by definition (as a result of our physical aray design)
                    # set reset are defined as an integer 
                    if Vpulse > self.RRAM.getVtp():
                        print('SET pulse applied to '+'R'+str(row)+str(col))
                        
                    elif Vpulse < self.RRAM.getVtn():
                        print('RESET pulse applied to '+'R'+str(row)+str(col))
                        #print(self.RRAM.getVtn())
                    
                    Rchange = self.RRAM.rate_of_change_of_R(Vpulse) * pulse_width
                    self.arr[row][col] += Rchange
                            
                    if Rchange != 0:
                        #please redefine your array, row and col get submitted as part of the function
                        print('New resistance: '+str(self.arr[row][col])+' ohm')
                    
                        """If resistance exceeds HRS, clip resistance to HRS (window=0 in model)"""
                        if  self.arr[row][col] <= self.RRAM.getLRS():
                            self.arr[row][col] = self.RRAM.getLRS()
                            print('R'+str(row)+str(col)+' is clipped to LRS state: '+str(self.arr[row][col]))
                        
                        """If resistance goes below LRS, clip resistance to LRS (window=0 in model)"""
                        if self.arr[row][col] >= self.RRAM.getHRS():
                            self.arr[row][col] = self.RRAM.getHRS()
                            print('R'+str(row)+str(col)+' is clipped to HRS state: '+str(self.arr[row][col]))
                            
                            """Current compliance Imax=Current_Compliance(Vg) in real array later"""
                            #  Imax=75*(10**(-6))  #this'll give R=16k ohm for Vpulse of 1 V
                            #  if Vpulse/self.arr[row][col]>Imax:
                            #      print('New current ',Vpulse/self.arr[row][col],'exceeded Imax')
                            #     self.arr[row][col]=Vpulse/Imax
                            #    print('So new R: ',self.arr[row][col],'ohm')
                            #To see effect of current compliance, please initialize R of array to a value close to 7000 ohm
                    else:
                        print('No resistance change')
                    
                    return self.arr[row][col]
                            
            
#Base class is a derived class from Exception class         
class Error(Exception):
    pass


class MyError(Error):
    
    def __init__(self, value):
        self.value=value



