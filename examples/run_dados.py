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

from ..dados import Dados

def main():
    '''
    Description of the run file.

    '''

    # Parameters
    time_step  = 0.1

    ir_7040 = Cortix(splash=True)
    ir_7040.network = Network()

    ir_7040_net = ir_7040.network

    # DADOS module.
    dados = Dados()
    ir_7040_net.module(dados)
    dados.rs232_filename = 'ir-7040'
    dados.rs232_request_string = '\r\nP0001 01245689BCDMNVWYZaOdghin 55}'

    # DataPlot module.
    data_plot = DataPlot()
    data_plot.title = 'IR-7040 Data Acquisition'
    data_plot.dpi = 300

    # Network connectivity

    ir_7040_net.connect( [dados,'rs-232'], [data_plot,'viz-data'] )
    rs232_port.connect(plot_port)

    ir_7040_net.draw()

    # Run application
    ir_7040.run()

if __name__ == "__main__":
    main()
