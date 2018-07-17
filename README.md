<<<<<<< HEAD
# RRAM
Software for interfacing in-memory computation methods to physical/virtual RRAM.

RRAM models and RRAM array do not change, they simulate the hardware RRAM array. 

analysingSoftware.py is the correlation detection code; it takes input from either Recording.py or GenerateCorrelatedProcess.py.

Recording.py is spiking data input, it samples spiking data and converts it to input array. 

GenerateCorrelatedProcess.py is an input array to the algorithm, where correlated/uncorrelated processes are generated using random generators. 

=======
# RRAM
Software for interfacing in-memory computation methods to physical/virtual RRAM.

RRAM models and RRAM array do not change, they simulate the hardware RRAM array. 

analysingSoftware.py is the correlation detection code; it takes input from either Recording.py or GenerateCorrelatedProcess.py.

Recording.py is spiking data input, it samples spiking data and converts it to input array. 

GenerateCorrelatedProcess.py is an input array to the algorithm, where correlated/uncorrelated processes are generated using random generators.

Main_with_correlation.py is the interface that links the RRAM array, models to analysingSoftware. It runs all the files together. 

>>>>>>> 8ce4fad92f31594b974549b31864483cbebfb29f
