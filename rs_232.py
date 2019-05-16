#!/usr/bin/env python3
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
import os, sys, io, time, datetime, traceback
import argparse, logging

import serial
#*********************************************************************************

class RS_232():
    r'''
    RS-232 class for Dados. Serial communication with various devices.
    '''

#*********************************************************************************
# Construction 
#*********************************************************************************

    def __init__( self, device_name = 'null_device_name', wrk_dir='null-rs_232_wrk_dir' ):

        self.__wrk_dir = wrk_dir

        if device_name == 'ir-7040':
            self.__ir_7040()
        else:
            assert device_name == 'ir-7040','device name: %r'%device_name

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

    def __ir_7040( self ):
        '''
        IR 7040 "intelligent ratemeter from Mirion Tech. Inc.
        '''

        #initialize serial object, parameters hard-coded for now
        port = '/dev/ttyUSB0'
        baud_rate = 9600
        timeout = 5

        ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=5,
                            stopbits = serial.STOPBITS_ONE,
                            parity = serial.PARITY_NONE,
                            bytesize=serial.EIGHTBITS)
        olddata=''
        while True:
            #Send request string, specific to IR7040
            ser.write('\r\nP0001 1289Od 7F}'.encode('ascii'))
            original_line=ser.readline()
            line = str(original_line.decode('utf-8', errors='replace').strip())
            if line == olddata:
                time.sleep(.25)
                continue
            self.timestamp=str(datetime.datetime.now())[:-7]
            olddata=line
            print(line)
            splitline=line.split()
            splitline.append(self.timestamp)
            for n in range(2,8):
                splitline[n] = splitline[n][0]+'.'+splitline[n][1:3]+'e'+splitline[n][3:]
            filename='{}/ir_7040_data_{}.csv'.format(self.__wrk_dir,str(datetime.datetime.now())[:10])
            if not os.path.isfile(filename):
                with open(filename,'a') as f:
                    f.write('Type,Callback,Ch1_rate_filtered,Ch1_rate_unfiltered,Ch2_rate_filtered,Ch2_rate_unfiltered,Ch4_rate_filtered,Ch4_rate_unfiltered,Checksum,Date and Time\n')
            padding = ', '.join(splitline)
            commaline=padding
            padding += (" " * (100 - len(padding)))
            c=0

            with open(filename,'a') as f:
                f.write('{}\n'.format(commaline))

#======================= end class Dados: ========================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Spawn an RS_232 process')
    parser.add_argument('-d', '--device-name', dest="device_name", help='The name of the device', required=True)
    parser.add_argument('-w', '--work-dir', dest="work_dir", help='The path to the work directory', required=True)

    args = parser.parse_args()

    RS_232( device_name = args.device_name, wrk_dir = args.work_dir )
