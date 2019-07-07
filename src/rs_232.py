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

from cortix.src.module import Module
#*********************************************************************************

class RS_232(Module):
    r'''
    RS-232 class for Dados. Serial communication with various devices.
    '''

#*********************************************************************************
# Construction 
#*********************************************************************************

    def __init__( self, wrk_dir='/tmp/dados',filename='ir_data'):
        super().__init__() 
        self.filename=filename
        if not os.path.isdir(wrk_dir):
            os.makedirs(wrk_dir)
        self.__wrk_dir = wrk_dir

    def run(self,timeID=''):
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
            print(line)
            olddata=line
            splitline=line.split()
            splitline.append(self.timestamp)
            for n in range(2,8):
                splitline[n] = splitline[n][0]+'.'+splitline[n][1:3]+'e'+splitline[n][3:]




if __name__=='__main__':
    app = RS_232()
    app.run()
