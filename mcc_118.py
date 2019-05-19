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

class MCC_118():
    r'''
    RS-232 class for Dados. Serial communication with various devices.
    '''

#*********************************************************************************
# Construction 
#*********************************************************************************

    def __init__( self, device_name = 'null_device_name', 
            wrk_dir='/tmp/dados' ):

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
        with open(filename,'w') as f:
            f.write('')
        hatlist = hat_list()
        for i in hatlist:
            ad = i.address
        hat = mcc118(ad)
        options = OptionFlags.DEFAULT
        chan=0
        avg=[]
        home=os.path.expanduser('~')
        directory=home+'/IR7040_database'
        if not os.path.isdir(directory):
            os.makedirs(directory)
        while True:
            value = hat.a_in_read(0,options)
            avg.append(value)
            if len(avg)<100:
                time.sleep(0.005)
                continue
            mean=sum(avg)/len(avg)
            avg=[]
            #print(mean)
            timestamp=str(datetime.datetime.now())[:-7]
            filename2='{}/mcc_118_data_{}'.format(directory,str(datetime.datetime.now())[:10])
            with open(filename,'w') as f:
                f.write(str(mean))
            with open(filename2,'a') as file:
                file.write('{}, {}\n'.format(str(mean),timestamp))

#======================= end class MCC118: =======================================
