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
RS-232 serials port communication class
'''
#*********************************************************************************
import os, sys, io, time, datetime, traceback
import logging

import serial
#*********************************************************************************

class RS_232():
    r'''
    RS-232 class for Dados
    '''

#*********************************************************************************
# Construction 
#*********************************************************************************

    def __init__( self ):

        port = '/dev/ttyUSB0'
        baud_rate = 9600
        timeout = 5

        serial_rs232 = serial.Serial( port=port, baudrate=baud_rate, \
                timeout=timeout, stopbits=serial.STOPBITS_ONE, \
                parity=serial.PARITY_NONE, \
                bytesize=serial.EIGHTBITS )

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


#======================= end class Dados: ========================================
