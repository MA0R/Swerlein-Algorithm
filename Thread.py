"""
Everything about GPIB control. The GUI should only allow one GPIB thread at a
time.
Thread also writes raw data file as CSV. Log files are written at event termination from graphframe.py.
"""

import stuff
import csv
import time
import wx
import visa
import numpy as np

class Algorithm(stuff.WorkerThread):
    """
    Main algorithm thread
    """
    def __init__(self,**kwargs):
        stuff.WorkerThread.__init__(self,**kwargs)
        #default settings
        self.info = {'port':22,'harmonics' :6,'name':None,'bursts':6,'readings':1,'time':15,'rng':'AUTO','acdc':True,'ac':False,'mean':False,'time':15,'grid':'','LFREQ':False}
        #update info if kwarg is not empty
        self.grid_exists = False
        for key in kwargs:
            if kwargs[key]:
                self.info[key] = kwargs[key]
        if self.info['grid']:
            self.grid_exists = True
            self.row_count = 0
            self.grid = self.info['grid']
        #notify window and event not needed, will simply print to table anyway, and table is to be made optional. if table exists, then print to it
        start_time = time.localtime()
        log_file_name = 'log.'+str(start_time[0])+'.'+str(start_time[1])+'.'+str(start_time[2])+'.'+str(start_time[3])+'.'+str(start_time[4])+".txt"
        raw_file_name = 'raw.'+str(start_time[0])+'.'+str(start_time[1])+'.'+str(start_time[2])+'.'+str(start_time[3])+'.'+str(start_time[4])+".csv"
        self.csvfile = open(raw_file_name,'wb')
        self.logfile = open(log_file_name,'w')
        self.writer = csv.writer(self.csvfile)
        self.row_counter = 0
        grid_row = ["Time stamp [ms]","ACDC [V]","AC [V]","Error [ppm]","Frequency [Hz]"]
        self.print_grid_row(grid_row)
        
        self.start() #important that this is the last statement of initialisation. goes to run()


    def PrintSave(self, text):
        start_time = time.localtime()
        time_string = str(start_time[0])+'.'+str(start_time[1])+'.'+str(start_time[2])+'.'+str(start_time[3])+'.'+str(start_time[4])+'.'+str(start_time[5])+" "
        print(str(time_string)+str(text))
        self.logfile.write(time_string+str(text))
        self.logfile.write('\n')

    def WriteSave(self,text):
        self.PrintSave('writing: '+str(text))
        self.instrument.write(text)

    def ReadSave(self):
        reading = self.instrument.read_raw()
        self.PrintSave('readings from instrument: '+str(reading))
        return reading

    def run(self):
        for run_number in range(self.info['readings']):
            self.single()
        self.csvfile.close()
        self.logfile.close()
        
    def single(self):
        def reset(self):
            self.instrument.write('DISP OFF, RESET')
            self.instrument.write('RESET')
            self.instrument.write('end 2')
            self.instrument.write('DISP OFF, READY')

        rm = visa.ResourceManager()
        self.instrument = rm.open_resource('GPIB0::'+str(self.info['port'])+'::INSTR')
        self.instrument.timeout = 10000

        self.readings = []
        self.times = []
        self.AcdcArray = []
        self.AcArray = []
        self.MeanArray = []
        self.MemArray = []

        reset(self)
        error = self.instrument.query('ERR?')
        if error != '0\r\n':
            self.csvfile.close()
            self.logfile.close()
            return #end the thread

        Meas_time=15.0              # Target measure time
        #Tsampforce=.001           #  FORCED PARAMETER
        #Aperforce=Tsampforce-(3e-5)#  FORCED PARAMETER
        #Numforce=800.0              #  FORCED PARAMETER
        Aper_targ=0.001            #A/D APERTURE TARGET (SEC)
        Nharm_min=self.info['harmonics']                   #MINIMUM # HARMONICS SAMPLED BEFORE ALIAS
        Nbursts=self.info['bursts']                 #NUMBER OF BURSTS USED FOR EACH MEASUREMENT

        #determine input signal RMS,range and frequency
        self.WriteSave("ACDCV")
        RMS = float(self.ReadSave())#read value of AC voltage
        Range = 1.55*RMS #convert RMS to peak voltage, with 10% tolerance
        if self.info['rng'] !='AUTO':
            Range = self.info['rng']
            
        self.WriteSave('DISP OFF, MEASURING')
        
        if self.info['LFREQ']==False:
            self.WriteSave("FREQ")
            Expect_Freq = float(self.ReadSave())
        else:
            self.WriteSave("LINE?")
            Expect_Freq = float(self.ReadSave())
            
        Freq = self.FNFreq(Expect_Freq)
        #SAMP PARAM
        Aper=Aper_targ
        Tsamp=(1e-7)*int((Aper+(3e-5))/(1e-7)+0.5) #rounds to 100ns
        #PrintSave("first Tsamp: "+str(Tsamp))
        Submeas_time=float(Meas_time)/float(Nbursts) #meas_time specified, this is target time per burst
        Burst_time=Submeas_time*Tsamp/(0.0015+Tsamp) #IT TAKES 1.5ms FOR EACH sample to compute Sdev
        Approxnum=int(Burst_time/Tsamp+0.5)
        #PrintSave(Approxnum)
        Ncycle=int(Burst_time*Freq+0.5) # NUMBER OF 1/Freq TO SAMPLE
        #PrintSave(" ")
        #PrintSave("Ncycle: "+str(Ncycle))
        if Ncycle==0:
            self.PrintSave("Ncycle was 0, set to 1")
            Ncycle=1
            Tsamp=(1e-7)*int(1.0/Freq/Approxnum/(1e-7)+0.5)
            Nharm=int(1.0/Tsamp/2.0/Freq)
            #PrintSave("Nharm: "+str(Nharm))
            if Nharm<Nharm_min:
                #PrintSave("Nharm too small, set to 6")
                Nharm=Nharm_min
                Tsamp=(1e-7)*int(1.0/2.0/Nharm/Freq/(1e-7)+0.5)
        else:
            Nharm=int(1/Tsamp/2/Freq)
            #PrintSave("Nharm: "+str(Nharm))
            if Nharm<Nharm_min:
                Nharm = Nharm_min
                #PrintSave("Nharm too small, set to 6")

            Tsamptemp=(1e-7)*int(1.0/2.0/Nharm/Freq/(1e-7)+0.5)
            Burst_time=Submeas_time*Tsamptemp/(0.0015+Tsamptemp)
            Ncycle=int(Burst_time*Freq+1) ##0.5 to 1

            Num=int(Ncycle/Freq/Tsamptemp+0.5)
            #PrintSave("Num: "+str(Num))

            if Ncycle>1:
                K=int(Num/20/Nharm+1) #0.5 to 1
                #PrintSave("K= "+str(K))
            else:
                K=0
                #PrintSave("K=0")
            Tsamp=(1e-7)*int(Ncycle/Freq/(Num-K)/(1e-7)+0.5)
            if Tsamp-Tsamptemp<(1e-7):
                #PrintSave("Tsamp increased from "+str(Tsamp)+"to "+str((Tsamp+1e-7)))
                Tsamp=Tsamp+1e-7

        Aper=Tsamp-(3e-5)
        Num=int(Ncycle/Freq/Tsamp+0.5)
        #PrintSave('NEW NUM '+str(Num))
        if Aper>1.0:
            Aper = 1.0
            self.PrintSave("Aperture too large, automatically set to 1")
        elif Aper<1e-6:
            self.PrintSave("A/D APERTURE IS TOO SMALL")
            self.PrintSave("LOWER Aper_targ, Nharm, OR INPUT Freq")
            self.PrintSave("Aperture set to 1e-6")
            Aper = 1e-6

        self.WriteSave('TARM HOLD;AZERO OFF;DCV '+str(Range))
        self.WriteSave('APER '+str(Aper))
        self.WriteSave('TIMER '+str(Tsamp))
        self.WriteSave('NRDGS '+str(Num)+',TIMER')
        if self.info['LFREQ'] == False: self.WriteSave('TRIG LEVEL;LEVEL 0,DC;DELAY 0;LFILTER ON') #trigger at 0 crossing of DC input
        else: self.WriteSave('TRIG LINE;DELAY 0;LFILTER ON') #Or trigger at the 0 crossing of the line frequency.

        if self.info['LFREQ'] == False: #skip this routine if LFREQ is true, to save time since LFREQ changes rapidly.
            self.WriteSave('MSIZE?')

            memory_available = self.ReadSave().split(',') #generates 2 element list, first element is memory available for measuremnts
            Storage = int( int(memory_available[0])/4 )
            #PrintSave(" ")
            #PrintSave("MACHINE SETUP COMPLETE")
            #PrintSave(" ")
            if Num>Storage:
                self.PrintSave("NOT ENOUGH VOLTMETER MEMORY FOR NEEDED SAMPLES")
                self.PrintSave("TRY A LARGER Aper_targ VALUE OR SMALLER Num")

        ######  PRELIMINARY COMPUTATIONS


        Bw_corr=self.FNVmeter_bw(Freq,Range)
        ##error estimate##
        if Range>120:
            Base = 15.0   #self heating and base error
        else:
            Base = 10.0

        X1=self.FNVmeter_bw(Freq,Range)
        X2=self.FNVmeter_bw(Freq*1.3,Range)
        Vmeter_bw=((1e+6)*abs(X2-X1))   #error due to meter band width, bw.

        Aper_er=(1.0*.002/Aper)       #GAIN UNCERTAINTY - SMALL A/D APERTURE
        if Aper_er>30 and Aper>=1e-5:
            Aper_er=30
        if Aper<1e-5:
            Aper_er=10+(0.0002/Aper)

        X=np.pi*Aper*Freq       #USED TO CORRECT FOR A/D APERTURE ERROR
        Sinc = np.sin(X)/X
        Y=np.pi*Freq*(Aper*1.0001+5.0e-8)
        Sinc2=np.sin(Y)/Y
        Sincerr=(1e+6*abs(Sinc2-Sinc))   #APERTURE UNCERTAINTY ERROR

        Sinc3=np.sin(3*X)/3/X      #SINC CORRECTION NEEDED FOR 3rd HARMONIC
        Harm_er=abs(Sinc3-Sinc)
        Dist=np.sqrt(1.0+(0.01*(1+Harm_er))**2)-np.sqrt(1.0+0.01**2)
        Dist=(Dist*1e+6)

        Tim_er=((1e+6)*1e-7/4/(Aper+(3.0e-5))/20.0)#ERROR DUE TO HALF CYCLE ERROR
        Limit=((1e+6)/4.0/Num/20.0)
        if Tim_er>Limit:
            Tim_er=Limit

        Noiseraw=0.9*np.sqrt(0.001/Aper)       #1 SIGMA NOISE AS PPM OF RANGE
        Noise=Noiseraw/np.sqrt(Nbursts*Num)  #REDUCTION DUE TO MANY SAMPLES
        Noise=10.0*Noise                   #NOISE AT 1/10 FULL SCALE
        #Noise=2.0*Noise                    #2 SIGMA
        #noise kept at 1 standard deviation
        
        if Range<=0.12:               #NOISE IS GREATER ON 0.1 V RANGE
            Noise=7.0*Noise                  #DATA SHEET SAYS USE 20, BUT FOR SMALL
            Noiseraw=7.0*Noiseraw            #APERTURES, 7 IS A BETTER NUMBER
        #Noise=int(Noise)+2.0                  #ERROR DUE TO SAMPLE NOISE
        Noise = Noise+2.0
        
        if Range<=12:
            Rsource=10000
            Cload=1.33e-10
            Df=1.1e-3          #0.11%
        else:
            Rsource=1.0e+5
            Cload=5.00e-11
            Df=3.3e-3
        Df_err=2*np.pi*Rsource*Cload*Df*Freq
        #Df_err=int(1.0e+6*Df_err)#ERROR DUE TO TO PC BOARD DIELECTRIC ABSORBTION
        #no need to round error to significant figures
        #Err IS TOTAL ERROR ESTIMATION.  RANDOM ERRORS ARE ADDED IN RSS FASHION
        Err=np.sqrt(Base**2+Vmeter_bw**2+Aper_er**2+Sincerr**2)
        Err=(Err+Df_err+Tim_er+Noise)


        Sum=0
        Sumsq=0

        for I in range(0,int(Nbursts)):
            Delay=float(I)/Nbursts/Freq+(1e-6)
            self.WriteSave('DELAY '+str(Delay))
            self.WriteSave('TIMER '+str(Tsamp))

            #make measuremnts
            self.WriteSave('MEM FIFO;MFORMAT DINT') #first in first out for memeory
            #clears memeory, sets to 4 bytes per reading
            self.WriteSave('TARM SGL')
            self.WriteSave('MMATH STAT')
            self.WriteSave('RMATH SDEV')
            Sdev = float(self.ReadSave())
            self.WriteSave('RMATH MEAN')
            Mean = float(self.ReadSave())

            
#a=Algorithm(harmonics = 8, readings = 1, LFREQ = True, bursts = 1,mean=True)
            if self.info['mean']==True:
                self.WriteSave('OFORMAT ASCII')
                to_read = min(Num,5120)
                self.WriteSave('DISP OFF,READING_MEM')
                self.WriteSave('RMEM 1,'+str(to_read)+',1')
                
                for l in range(0,to_read):
                    #self.WriteSave('RMEM '+str(l)+',1,1')
                    reading = str(self.instrument.read()) #str gets rid of eol characters
                    reading = float(reading[:-1])
                    self.MemArray.append(reading)

            Sdev=Sdev*np.sqrt((Num-1.0)/Num)     #CORRECT SDEV FORMULA

            Sumsq=Sumsq+Sdev*Sdev+Mean*Mean
            Sum=Sum+Mean
            Temp=Sdev*Bw_corr/Sinc
            #Temp=Range/(1e+7)*int(Temp*(1e+7)/Range)#6 DIGIT TRUNCATION

            I=I+1
        Dcrms=np.sqrt(Sumsq/Nbursts)
        Dc=Sum/Nbursts
        Acrms=np.sqrt(Dcrms**2-Dc**2)
        Acrms=Acrms*Bw_corr/Sinc  #CORRECT A/D Aper AND Vmeter B.W.
        Dcrms=np.sqrt(Acrms*Acrms+Dc*Dc)
        self.WriteSave('DISP ON')

        self.AcdcArray.append(Dcrms)
        self.PrintSave("ACDC "+str(Dcrms))

        self.AcArray.append(Acrms)
        self.PrintSave("AC "+str(Acrms))
            
        if self.info['mean'] == True:
            rms_initial = np.sqrt(np.mean([float(number)**2 for number in self.MemArray]))
            ratio = Dcrms/rms_initial #ratio of true amplitude to measured amplitude
            self.MemArray = [number*ratio for number in self.MemArray] #corrected array of all data
            self.MeanArray.append(np.mean(np.abs(self.MemArray))) #save into array of means
            self.PrintSave("Mean(|V|) "+str(np.mean(np.abs(self.MemArray))))
            start_time = time.localtime()
            mem_file_name = 'mem.'+str(start_time[0])+'.'+str(start_time[1])+'.'+str(start_time[2])+'.'+str(start_time[3])+'.'+str(start_time[4])+".csv"
            self.memfile = open(mem_file_name,'wb')
            self.memwriter = csv.writer(self.memfile)
            self.memwriter.writerow(self.MemArray)
            self.memfile.close()
        self.PrintSave("sinc "+str(Sinc))
        self.PrintSave("Bw_corr "+str(Bw_corr))
        self.PrintSave("Freq "+str(Freq))
        self.PrintSave("Num "+str(Num))
        self.PrintSave("Tsamp "+str(Tsamp))
        self.PrintSave("Ncycle "+str(Ncycle))
        self.PrintSave("Nbursts "+str(Nbursts))
        self.PrintSave("Estimated error "+str(Err))

        grid_row = [time.time(),Dcrms,Acrms,Err,Freq]
        self.print_grid_row(grid_row)
        return grid_row
    def print_grid_row(self,info):
        #save to csv
        row = self.row_counter
        self.writer.writerow(info)
        #now if there is a grid, save to it too.
        if self.grid_exists == True:
            if self.grid.GetNumberRows< row+1:
                self.grid.AppendRow()
            if self.grid.GetNumberCols < len(info):
                self.grid.AppendCol()
            for i in range(len(info)):
                self.grid.SetCellValue(self.row_counter,i,str(info[i]))
        #next time it prints, go to the next row
        self.row_counter = self.row_counter +1
                

        
    def FNFreq(self,Expect):
        self.WriteSave("TARM HOLD;LFILTER ON;LEVEL 0,DC;FSOURCE ACDCV")
        #self.WriteSave("FREQ "+str(Expect*0.9))
        Cal = float(self.instrument.query("CAL? 245"))
        Freq=Expect/Cal
        return Freq

    def FNVmeter_bw(self,Freq,Range):
        Lvfilter = 120000.0  #LOW VOLTAGE INPUT FILTER B.W.
        Hvattn=36000.0     #HIGH VOLTAGE ATTENUATOR B.W.(NUMERATOR)
        Gain100bw=82000.0   #AMP GAIN 100 B.W. PEAKING CORRECTION!
        if Range<=0.12:
            Bw_corr=(1+(Freq/Lvfilter)**2)/(1+(Freq/Gain100bw)**2)
            Bw_corr=np.sqrt(Bw_corr)
        elif Range<=12:
            Bw_corr=(1+(Freq/Lvfilter)**2)
            Bw_corr=np.sqrt(Bw_corr)
        elif Range>12:
            Bw_corr=(1+(Freq/Hvattn)**2)
            Bw_corr=np.sqrt(Bw_corr)

        return Bw_corr


