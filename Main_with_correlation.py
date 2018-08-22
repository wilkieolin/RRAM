import RRAM_array_v2 as RRAMArray
import RRAM_models as RRAMMod
import analysingSoftware as software


#Creating the array and initialization

ReRAM = RRAMMod.RRAM_model_sherif()
array= RRAMArray.RRAM_ARRAY_sim(5,5, ReRAM)
correlation=software.analysing_software(5,5,0.1) #the tricky part is choosing C=0.1, otherwise 
                                                    #resistance is either clipped to LRS or it doesnt change
                                                    #from 50000 (V<Vtp). 


print('After initialization of created array: ')
array.show_R()

def interface(Array, Vp, CC, pw, r, c, SR):
    try:
        #print(Array.checkForExceptions(Vp))
        newR = Array.read_or_write(r,c,Vp,pw, SR, CC)
        print("extracted resistance from col ", c, " and row ", r," is ", newR, ".")
        return newR
        
    except RRAMArray.MyError as error:
        print(error.value)


print('Database:  \n',correlation.generate_x())        #generate database array x 



CC = 100*10**(-6)
SR = True
pw = 5*10**(-9)



#the following passes the processes through the RRAM, modulates resistance where X(k)=1            
for i in range(correlation.get_total_k()):
    print('Array at time k:\n',correlation.array_at_time_k())  #this changes the value of all processes when k/kn is incremented, taking values from x  
    Vp = 1.5*correlation.momentum()
    print(Vp,'V')
    for r in range(5):
        for c in range(5):
            row=correlation.check_row_col(r,c)[0]
            col=correlation.check_row_col(r,c)[1]
            #interface(array, Vp, CC, pw, r, c, SR)
            if row>=0 or col>=0:
                interface(array, Vp, CC, pw, row, col, SR)
                print('Process X(k)=1 at row ',row,' and column ',col)

#Read resistance from array and store in analysing software
print('Read: \n')
for r in range(5):
    for c in range(5):
        Vread=0.2
        pwread=300*10**(-9)
        R=interface(array, Vread, CC, pwread, r, c, SR)
        correlation.read_resistance(r,c,R)
print('\n Storing the resistance read in an array=\n',correlation.getResistanceRead())


#print(correlation.numberOfOnes())
print(correlation.plotImage()) 
#print(correlation.conductancePlot(),'\n')
print('total samples',correlation.getK0())
print(correlation.uncenteredCovariance())

