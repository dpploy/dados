#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit environment
# https://cortix.org
'''
Cortix run file for DADOS using the IR-7040 gas ratemeter RS-232 interface.

'''

from cortix.src.cortix_main import Cortix
from cortix.src.network import Network


import dados


class Dados_Run:
    def __init__(self):
        '''
        Example DADOS run file that demonstrates how to build a Cortix
        Application

        '''

        # Parameters
        time_step  = 0.1
        print('-----\nWhat is the experiment name?')
               self.experiment_name = input('>>')    
        while True:
            try:
                print('-----\nHow many seconds would you like to capture?')
                self.time_range = int(input('>>'))
                break
            except:
                print('Invalid Input. Please Try Again')

        self.cortix = Cortix(splash=True)
        self.cortix.network = Network()
        self.net = self.cortix.network

        # DADOS module
        ir_7040 = dados.IR_7040()
        self.ir_dados = dados.Dados(device=ir_7040)
        self.ir_dados.time_range = self.time_range
        self.ir_dados.number_of_data_lines = 6
        self.net.module(self.ir_dados)

        mcc = dados.MCC_118(channels=[2,])
        self.mcc_dados = dados.Dados(device=mcc)
        self.mcc_dados.number_of_data_lines = 7
        self.mcc_dados.time_range = self.time_range
        self.net.add_module(self.mcc_dados)

        # DataPlot module
        self.plot = dados.Dataplot()
        self.plot.plot_list = ['Rate Filtered (Chan 1)','Rate Filtered (Chan 2)',
                                'Rate Filtered (Chan 4)','Channel: 2']
        self.plot.experiment_name = self.experiment_name
        self.net.add_module(self.plot)
        
        
    def start(self):
        self.net.connect( [self.ir_dados,'rs-232'], [self.plot,'RS232-viz'] )
        self.net.connect( [self.mcc_dados,'mcc-118'], [self.plot,'MCC118-viz'] )
        # Run application
        self.cortix.run()

        self.cortix.close()


if __name__ == "__main__":
    app = Dados_Run()
    app.start()
