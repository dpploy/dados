#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit environment
# https://cortix.org
'''
Cortix run file for DADOS using the IR-7040 gas ratemeter RS-232 interface.

'''

from cortix.src.cortix_main import Cortix
from cortix.src.network import Network

from cortix.examples.dataplot import DataPlot

import dados


class Dados_Run:
    def __init__(self):
        '''
        Example DADOS run file that demonstrates how to build a Cortix
        Application

        '''

        # Parameters
        time_step  = 0.1

        self.cortix = Cortix(splash=True)
        self.cortix.network = Network()

        self.net = self.cortix.network

        # DADOS module
        ir_7040 = dados.IR_7040()
        self.ir_dados = dados.Dados(device=ir_7040)
        self.net.module(self.ir_dados)
##        # DataPlot module
        self.data_plot = DataPlot()
        self.data_plot.title = 'IR-7040 Data Acquisition'
        self.data_plot.dpi = 300
        self.net.add_module(self.data_plot)
        

        
        
    def start(self):
        self.net.connect( [self.ir_dados,'rs-232'], [self.data_plot,'viz-data'] )
        # Run application
        self.cortix.run()
if __name__ == "__main__":
    app = Dados_Run()
    app.start()
