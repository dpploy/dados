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

from cortix.src.module import Module
#*********************************************************************************

class Plot(Module):
    def __init__( self, wrk_dir='/tmp/dados',db_dir='IR_7040_db'):
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
        #mcc = self.get_port('mcc')
        rs = self.get_port('rs')
        while True:
            #line = self.recv(mcc)
            line2 = self.recv(rs)
            print(line2)
            time.sleep(0.01)
            

if __name__=='__main__':
    app = Plotting()
    app.run()
