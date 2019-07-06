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
import logging

import serial
#*********************************************************************************

class RS_232(threading.Thread):
    r'''
    RS-232 class for Dados. Serial communication with various devices.
    '''

#*********************************************************************************
# Construction 
#*********************************************************************************

    def __init__( self, wrk_dir='/tmp/dados',filename='ir_data',rsevent=None):
        self.rsevent=rsevent
        self.filename=filename
        if not os.path.isdir(wrk_dir):
            os.makedirs(wrk_dir)
        self.__wrk_dir = wrk_dir

#        if device_name == 'ir-7040':
#        else:
#            assert device_name == 'ir-7040','device name: %r'%device_name

        return

#*********************************************************************************
# Public member functions
#*********************************************************************************

    def execute( self, cortix_time=0.0, cortix_time_step=0.0 ):
        '''
        Developer must implement this method.
        Evolve system from cortix_time to cortix_time + cortix_time_step
        '''

        s = 'execute('+str(round(cortix_time,2))+'[min]): '
        self.__log.debug(s)

        # Developer implements helper method, for example
        #self.__evolve( self, cortix_time, cortix_time_step ):

        return

#*********************************************************************************
# Private helper functions (internal use: __)
#*********************************************************************************

    def ir_7040(self,timeID='',event=None):
        '''
        IR 7040 "intelligent ratemeter from Mirion Tech. Inc.
        '''

        #initialize serial object, parameters hard-coded for now
        port = '/dev/ttyUSB0'
        baud_rate = 9600
        timeout = 5
        home = os.path.expanduser('~')
        directory=home+'/IR7040_database'
        if not os.path.exists(directory):
             os.makedirs(directory)
        ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=5,
                            stopbits = serial.STOPBITS_ONE,
                            parity = serial.PARITY_NONE,
                            bytesize=serial.EIGHTBITS)
        olddata=''
        tempfile='{}/{}{}.csv'.format(self.__wrk_dir,self.filename,timeID)
        while True:
            #Send request string, specific to IR7040
            ser.write('\r\nP0001 01245689BCDMNVWYZaOdghin 55}'.encode('ascii'))
            original_line=ser.readline()
            line = str(original_line.decode('utf-8', errors='replace').strip())
            if line == olddata:
                time.sleep(.25)
                continue
            self.timestamp=str(datetime.datetime.now())[:-7]
#            print(line)
            try:
                if self.rsevent.isSet():
#                    print('Thread killed')
                    return
            except AttributeError:
                pass
            olddata=line
            splitline=line.split()
            splitline.append(self.timestamp)
            for n in range(2,8):
                splitline[n] = splitline[n][0]+'.'+splitline[n][1:3]+'e'+splitline[n][3:]
            filename='{}/ir_7040_data_{}.csv'.format(directory,str(datetime.datetime.now())[:10])
            if not os.path.isfile(filename):
                with open(filename,'a') as f:
                    f.write('Type, Callback, ch1_rate_filtered, ch1_rate_unfiltered, ch1_dose, ch1_alarm_high, ch1_alarm_low\
                            , ch2_rate_filtered, ch2_rate_unfiltered, ch2_dose, ch2_alarm_high, ch2_alarm_low\
                            , Leak Rate: Gallons/Day, Leak Rate: %Power Level\
                            , ch3_rate_filtered, ch3_rate_unfiltered, ch3_dose, ch3_alarm_high, ch3_alarm_low\
                            , ch4_rate_filtered, ch4_rate_unfiltered, ch4_dose, ch4_alarm_high, ch4_alarm_low\
                            , Checksum, Probe Status, Date and Time\n')
            padding = ', '.join(splitline)
            commaline=padding
            padding += (" " * (100 - len(padding)))
            c=0
            with open(tempfile,'w') as file:
                file.write(commaline)
            with open(filename,'a') as f:
                f.write('{}\n'.format(commaline))

#======================= end class Dados: ========================================
