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
from cortix.src.module import Module
#*********************************************************************************

class MCC_118(Module):
    r'''
    Class for MCC_118 analog voltage data acquisition device
    '''

#*********************************************************************************
# Construction 
#*********************************************************************************

    def __init__( self, wrk_dir='/tmp/dados',db_dir='IR_7040_db'):
        super().__init__()
        print('MCC_118 class start')
        self.wrk_dir = wrk_dir
        home=os.path.expanduser('~')
        self.db_dir=os.path.join(home,db_dir)
        for d in [self.wrk_dir,self.db_dir]:
            if not os.path.isdir(d):
                os.makedirs(d)

    def run(self ,channels=[0,2,4]):
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
        mcc=self.get_port('mcc')
        while True:
            for i in channels:
                if str(i) not in avgs:
                    avgs[str(i)] = []
                value = hat.a_in_read(i,options)
                avgs[str(i)].append(value)
            if len(avgs[str(i)])<200:
                len(avgs[str(i)])
                time.sleep(0.00005)
                continue
            for i in channels:
                i=str(i)
                avgs[i] = sum(avgs[i])/len(avgs[i])
            print(avgs)
            self.send('test message',mcc)
            avgs=dict()

#======================= end class MCC118: =======================================

if __name__=='__main__':
    app = MCC_118()
    app.run()
