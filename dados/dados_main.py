#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the DADOS repository; a Cortix module.
# https://cortix.org

import time, os, datetime
import numpy as np

from cortix.src.module import Module
import dados

class Dados(Module):
    '''
    DADOS is a Cortix module for data acquistion.

    Ports
    =====
    rs-232:
    mcc-118:

    '''

    def __init__(self, device=None, timestep=0.1,command_string=None):
        super().__init__()
        print('dados_main init')
        self.device = device
        if isinstance(self.device,str):
            if device.lower() == 'ir_7040':
                self.device = dados.IR_7040()
            if device.lower() == 'mcc_118':
                self.device = dados.MCC_118
        # RS-232 default configuration

        self.number_of_data_lines = 5
        # MCC 118 configuration
        self.time_range = 10
        #self.state = somedata

    def run(self):

        self.endtime = datetime.datetime.now()+datetime.timedelta(seconds=self.time_range)
        # Evolve daq_time    
        while datetime.datetime.now()<=self.endtime:
            
            line = self.device.read_lines(lines=self.number_of_data_lines)
            for port in self.ports:
                self.send(line,port)
        for port in self.ports:
            self.send('Done', port)
        
