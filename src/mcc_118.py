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

    '''

#*********************************************************************************
# Construction 
#*********************************************************************************

    def __init__( self, wrk_dir='/tmp/dados',db_dir='IR_7040_db'):
        print('start')

        self.wrk_dir = wrk_dir
        self.db_dir=db_dir
        if not os.path.isdir(wrk_dir):
            os.makedirs(wrk_dir)

    def run(self ,channels=[0,2,4]):
        '''

        '''
        filename = self.wrk_dir+'/mcc_118_data.csv'
##        with open(filename,'w') as f:
##            f.write('')
        hatlist = hat_list()
        print(hatlist)
        for i in hatlist:
            ad = i.address
        hat = mcc118(ad)
        options = OptionFlags.DEFAULT
        home=os.path.expanduser('~')
        directory=home+os.path.join(home,self.db_dir)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        avgs=dict()
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
            avgs=dict()
            continue
            mean=dict()
            for i in channels:
                mean=sum(avg)/len(avg)
            avg=[]
            print(mean,value2,value4)
            timestamp=str(datetime.datetime.now())[:-7]
            filename2='{}/mcc_118_data_{}'.format(directory,str(datetime.datetime.now())[:10])
##            with open(filename,'w') as f:
##                f.write(str(mean))
            with open(filename2,'a') as file:
                file.write('{}, {}\n'.format(str(mean),timestamp))
##            if self.mccevent.isSet():
##                return

#======================= end class MCC118: =======================================
if __name__=='__main__':
    app = MCC_118()
    app.run()
