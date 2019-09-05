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
import os, sys, io, time, datetime, traceback, logging
import pandas as pd
try:
    from daqhats import mcc118, OptionFlags, HatIDs, HatError, hat_list
except ModuleNotFoundError as e:
    pass

from cortix.src.module import Module
#*********************************************************************************

class MCC_118(Module):
    r'''
    Class for MCC_118 analog voltage data acquisition device
    '''

#*********************************************************************************
# Construction 
#*********************************************************************************
    def __init__( self, channels=[]):
        super().__init__()
        try:
            import daqhats
        except:
            print("DAQHats library not installed, download from source at: https://github.com/mccdaq/daqhats")
            return
        self.channels = channels
        if self.channels==[]:
            self.channels=[f for f in range(8)]
        self.running_avg=400
    
    def read_lines(self, lines=2):
        '''
        Run class that will be called by Cortix
        Returns data in predetermined format (format undecided)
        '''
        hatlist = hat_list()
        for i in hatlist:
            ad = i.address
        hat = mcc118(ad)
        options = OptionFlags.DEFAULT
        avgs=dict()
        datadic = {}
        check = True
        counter=0
        while counter<lines:
            for i in self.channels:
                name = 'Channel: '+str(i)
                if name not in avgs:
                    avgs[name] = []
                value = hat.a_in_read(i,options)
                avgs[name].append(value)
            if len(avgs[name])<self.running_avg:
                time.sleep(0.00005)
                continue
            counter +=1
            self.timestamp = str(datetime.datetime.now())[:-7] 
            if 'Timestamp' not in datadic:
                datadic['Timestamp'] = []
            datadic['Timestamp'].append(self.timestamp)
            for i in avgs:
                avgs[i] = sum(avgs[i])/len(avgs[i])
                if i not in datadic:
                    datadic[i] = []
                datadic[i].append(avgs[i])
            avgs=dict()
        return datadic
#======================= end class MCC118: =======================================

if __name__=='__main__':
    app = MCC_118()
    print(app.run())
