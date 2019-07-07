# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit evironment
# https://github.com/dpploy/cortix
#
# All rights reserved, see COPYRIGHT for full restrictions.
# https://github.com/dpploy/COPYRIGHT....
#
# Licensed under the GNU General Public License v. 3, please see LICENSE file.
# https://www.gnu.org/licenses/gpl-3.0.txt
'''
IR 7040 "intelligent ratemeter from Mirion Tech. Inc.
'''
#*********************************************************************************
import os, sys, io, time, datetime, traceback, threading
import logging, serial
import pandas as pd

from cortix.src.module import Module
#*********************************************************************************

class RS_232(Module):
    r'''
    RS-232 class for Dados. Serial communication with various devices.
    '''

#*********************************************************************************
# Construction 
#*********************************************************************************

    def __init__( self, wrk_dir='/tmp/dados',filename='ir_data',db_dir='IR_7040_db'):
        super().__init__() 
        self.fname = filename
        self.wrk_dir = wrk_dir
        home=os.path.expanduser('~')
        self.db_dir=os.path.join(home,db_dir)
        for d in [self.wrk_dir,self.db_dir]:
            if not os.path.isdir(wrk_dir):
                os.makedirs(wrk_dir)

    def run(self):
        '''
        IR 7040 "intelligent ratemeter from Mirion Tech. Inc.
        '''

        #initialize serial object, parameters hard-coded for now
        port = '/dev/ttyUSB0'
        baud_rate = 9600
        timeout = 5
        home = os.path.expanduser('~')
        directory=home+'/IR7040_database'
        ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=5,
                            stopbits = serial.STOPBITS_ONE,
                            parity = serial.PARITY_NONE,
                            bytesize=serial.EIGHTBITS)
        olddata=''
        tempfile='{}/{}.csv'.format(self.wrk_dir,self.filename)
        rs = self.get_port('rs-plot')
        check=True
        if os.path.exists(tempfile):
            os.remove(tempfile)
        while True:
            #Send request string, specific to IR7040
            ser.write('\r\nP0001 01245689BCDMNVWYZaOdghin 55}'.encode('ascii'))
            original_line=ser.readline()
            line = str(original_line.decode('utf-8', errors='replace').strip())
            if line == olddata:
                time.sleep(.25)
                continue
            self.timestamp=str(datetime.datetime.now())[:-7]
            minutes=self.timestamp[14:19]
            filetime = str(datetime.datetime.now())[:10]
            self.filename = os.path.join(self.db_dir,self.fname+filetime+'.csv')

            #print(line)
            olddata=line
            line = self.timestamp+', '+line
            splitline=line.split()
            for n in range(2,8):
                splitline[n] = splitline[n][0]+'.'+splitline[n][1:3]+'e'+splitline[n][3:]
            line = ', '.join(splitline)+'\n'
            if not os.path.isfile(self.filename):
                with open(self.filename,'w') as f:
                    f.write('Date and Time, Type, Callback, ch1_rate_filtered, ch1_rate_unfiltered, ch1_dose, ch1_alarm_high, ch1_alarm_low\
                            , ch2_rate_filtered, ch2_rate_unfiltered, ch2_dose, ch2_alarm_high, ch2_alarm_low\
                            , Leak Rate: Gallons/Day, Leak Rate: %Power Level\
                            , ch3_rate_filtered, ch3_rate_unfiltered, ch3_dose, ch3_alarm_high, ch3_alarm_low\
                            , ch4_rate_filtered, ch4_rate_unfiltered, ch4_dose, ch4_alarm_high, ch4_alarm_low\
                            , Checksum, Probe Status\n')
            with open(self.filename,'a') as f:
                f.write(line)
            if minutes == '00' and check == True:
                self.df = pd.read_csv(self.filename)
                self.send(self.df,rs)
                check == False
            if minutes != '00' and check==False:
                check = True
                     
    

if __name__=='__main__':
    app = RS_232()
    app.run()
