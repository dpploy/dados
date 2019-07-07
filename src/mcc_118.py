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

    def __init__( self, wrk_dir='/tmp/dados',filename='mcc_data',db_dir='IR_7040_db'):
        super().__init__()
        self.fname = filename
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
        mcc=self.get_port('mcc-plot')
        tempfile='{}/{}.csv'.format(self.wrk_dir,self.fname)
        if os.path.exists(tempfile):
            os.remove(tempfile)
        check = True
        while True:
            self.timestamp = str(datetime.datetime.now())[:-7]
            minutes=self.timestamp[14:16]
            filetime = str(datetime.datetime.now())[:10]
            self.filename = os.path.join(self.db_dir,self.fname+filetime+'.csv')
            for i in channels:
                if str(i) not in avgs:
                    avgs[str(i)] = []
                value = hat.a_in_read(i,options)
                avgs[str(i)].append(value)
            if len(avgs[str(i)])<400:
                len(avgs[str(i)])
                time.sleep(0.00005)
                continue
            for i in channels:
                i=str(i)
                avgs[i] = sum(avgs[i])/len(avgs[i])
            if not os.path.isfile(self.filename) :
                header='Date and Time, '
                with open(self.filename,'w') as f:
                    for i in channels:
                        header +='Chan {}, '.format(i)
                    header+='\sn'
                    f.write(header)
            dataline = self.timestamp+', '
            with open(self.filename,'a') as f:
                for i in channels:
                    dataline += '{}, '.format(avgs[str(i)])
                dataline+='\n'
                f.write(dataline)
            c=0
            with open(self.filename) as f:
                for line in f:
                    c+=1
            if minutes == '00' and check == True:              
                self.df = pd.read_csv(self.filename)
                self.send(self.df, mcc)
                check == False
            if minutes != '00':
                check = True
            avgs=dict()

#======================= end class MCC118: =======================================

if __name__=='__main__':
    app = MCC_118()
    app.run()
