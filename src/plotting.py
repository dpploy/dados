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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import pandas as pd

from cortix.src.module import Module
#*********************************************************************************

class Plot(Module):
    def __init__( self, wrk_dir='/tmp/dados',db_dir='IR_7040_database/graphs'):
        super().__init__()
        self.wrk_dir = wrk_dir
        home=os.path.expanduser('~')
        self.db_dir=os.path.join(home,db_dir)
        for d in [self.wrk_dir,self.db_dir]:
            if not os.path.isdir(d):
                os.makedirs(d)
        self.fig,self.ax = plt.subplots()

    def run(self ,channels=[0,2,4]):
        '''


        '''
        mcc = self.get_port('mcc-plot')
        rs = self.get_port('rs-plot')
        while True:
            mccdf = self.recv(mcc)
            rsdf = self.recv(rs)
            
            plotlist = ['ch1_rate_filtered','ch2_rate_filtered','ch3_rate_filtered','ch4_rate_filtered']
            for name in plotlist:
                filetime = str(datetime.datetime.now())[:10]
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.xaxis_date()
                fig.autofmt_xdate(rotation=45)
                plt.gcf().autofmt_xdate()
                myfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
                plt.gca().xaxis.set_major_formatter(myfmt)
                rsdf['Date and Time'] = pd.to_datetime(rsdf['Date and Time'])
                ax.plot(rsdf['Date and Time'],rsdf[name])
                ax.set_title("Serial Communication: {}".format(name))
                ax.set_xlabel('Rate of Activity')
                plt.autoscale()
                ax.relim()
                fig.savefig(os.path.join(self.db_dir,name+'_'+filetime+'.png'))

            plotlist2 = ['Chan 0','Chan 2','Chan 4']
            for name in plotlist2:
                filetime = str(datetime.datetime.now())[:10]
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.xaxis_date()
                fig.autofmt_xdate(rotation=45)
                plt.gcf().autofmt_xdate()
                myfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
                plt.gca().xaxis.set_major_formatter(myfmt)
                mccdf['Date and Time'] = pd.to_datetime(mccdf['Date and Time'])
                ax.plot(mccdf['Date and Time'],mccdf[name])
                ax.set_title("Analog Output: {}".format(name))
                ax.set_xlabel('Voltage')
                plt.autoscale()
                ax.relim()
                fig.savefig(os.path.join(self.db_dir,name+'_'+filetime+'.png'))
            print('graph saved!',str(datetime.datetime.now()))
            break
            time.sleep(0.01)
            

if __name__=='__main__':
    app = Plotting()
    app.run()
