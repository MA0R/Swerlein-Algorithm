# Swerlein-Algorithm
A python implementation of the Swerlein Algorithm (digital sampling for the HP3458A digital volt meter)
The Thread is stand alone and can be used with a gui, for example wx.
It contains a pythonised version of the algorithm first published in the 1980s in BASIC.
The algorithm consists of one main error computation followed by the result measuring.
Many constants in error calculation are due to the inherent innacuracies specific to the HP3458A.
This means that if the machiene hardware is improved, they should be changed.

To run the program:
1) At the bottom of 'Thread.py' write the desired key word arguments in a=Algorithm() (example provided)
2) Hit F5!
To change into real-instrument mode from simulated:
1) At the top of the program, change "import visa_simulated as visa" into "import visa".
2) Ensure to include the key word "simulated=False" when running an instance of the thread.
3) Send the adress of the DVM as a key word, "port="

To stop the program:
Click into the interactive window in IDLE and type a.abort() (or whatever name you call the algorithm).
This will flag it to stop, printing will terminate and the thread will stop shortly after. Before fully terminating
it will attempt to send "DCV AUTO" to the DVM, this is to protect the instrument.
If a GUI is made, it can call the abort method too as some kind of emergency stop. Ideally though the DVM should be allowed to 
finish its operations.

Outputs of the program:
It saves a raw data file as csv, and a log file of all communications it made including a time stamp.
The program also prints out everything that gets saved as it goes.

To use the program within a larger program:
the if statement at the bottom is only run if the module is the main module.
This means that it can be imported into larger programs. Notice that once the program ends,
it has 'return grid_row'. This means that once a parent program can have acess to it, if needed.
At the moment it returns the data but it is not picked up by anything, it is simply ignored in 'run'.

