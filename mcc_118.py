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
MCC 118 DAQ GitHub repository.
'''
#*********************************************************************************
import os, sys, io, time, datetime, traceback
import logging

from daqhats import mcc118, OptionFlags, HatIDs, HatError, hat_list
#*********************************************************************************

class MCC118():
    r'''
    RS-232 class for Dados. Serial communication with various devices.
    '''

#*********************************************************************************
# Construction 
#*********************************************************************************

    def __init__( self, device_name = 'null_device_name', 
            wrk_dir='null-mcc_118_wrk_dir' ):

        self.__wrk_dir = wrk_dir

        if device_name == 'analog-input':
            self.__mcc_118()
        else:
            assert device_name == 'analog-input','device name: %r'%device_name

        return

#*********************************************************************************
# Private helper functions (internal use: __)
#*********************************************************************************

    def __mcc_118( self ):
        '''
        IR 7040 "intelligent ratemeter from Mirion Tech. Inc.
        '''

        filename = self.__wrk_dir+'/mcc_118_data.csv'
        fout = open(filename,'w')
        fout.write('This is the header\n')

        hatlist = hat_list()
        for i in hatlist:
            ad = i.address
        hat = mcc118(ad)
        options = OptionFlags.DEFAULT
        chan=0
        while True:
            value = hat.a_in_read(0,options)
            fout.write(str(value)+'\n')
            time.sleep(0.1)
         
#======================= end class MCC118: =======================================
