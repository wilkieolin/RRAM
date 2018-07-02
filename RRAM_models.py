#Create a class to access Vtp, Vtn from the RRAM array
                   
class RRAM_model_sherif():
    """polynomial model without window function---equation 6 from Sheriff's ISCAS paper was 
       used to calculate change in resistance """
    
    """Parameters for HfOx device---other than those listed below, Vset,Vreset, 
    pulse_width were taken from Karsten's paper"""
    def __init__(self):
        #self.Vin=Vswitch
        self.Vtp=0.75
        self.Vtn=-0.5
        
        self.InitRes=40000
        self.HRS=30000
        self.LRS=7000
   
        self.t_swp=10*(10**(-9))
        self.t_swn=10**(-6)
        self.P_LRS=3
        self.P_HRS=3
        self.del_r=self.HRS-self.LRS
    
    def rate_of_change_of_R(self,Vin):
        if Vin>self.Vtp:
            rate_of_change_of_R=(-(self.del_r/self.t_swp)*(((Vin-self.Vtp)/self.Vtp)**self.P_LRS))
        elif Vin<self.Vtn:
            rate_of_change_of_R=((self.del_r/self.t_swn)*(((Vin-self.Vtn)/self.Vtn)**self.P_HRS))
        else:
            rate_of_change_of_R=0
        
        return(rate_of_change_of_R)

    def getVtp(self):
        return self.Vtp

    def getVtn(self):
        return self.Vtn

    def getLRS(self):
        return self.LRS
    
    def getHRS(self):
        return self.HRS

    def getInitRes(self):
        return self.InitRes
