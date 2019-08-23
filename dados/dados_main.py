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
        self.initial_time = 0.0
        self.end_time     = np.inf
        self.time_step    = timestep
        self.device = device
        if isinstance(self.device,str):
            if device.lower() == 'ir_7040':
                self.device = dados.IR_7040()
            if device.lower() == 'mcc_118':
                self.device = dados.MCC_118
        # RS-232 default configuration

        self.rs232_dev = '/dev/ttyUSB0'
        self.rs232_baud_rate = 9600
        self.rs232_timeout = 5
        self.rs232_request_string = 'rs232-null-request-string'
        self.rs232_request_string_encoding = 'ascii'
        self.number_of_data_lines = 20
        # MCC 118 configuration

        #self.state = somedata

    def run(self):


        # Evolve daq_time    
        while True:
            
            time.sleep( self.time_step )

            line = self.device.read_lines(lines=self.number_of_data_lines)
            print(line)
            for port in self.ports:
                self.send(line,port)
            

