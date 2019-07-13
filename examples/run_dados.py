#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit environment
# https://cortix.org

from cortix.src.module import Module
from cortix.src.port import Port
from cortix.util.dataplot import DataPlot
from cortix.src.cortix_main import Cortix

from ..src.dados import Dados

'''
Cortix run file for DADOS using the IR-7040 gas ratemeter RS-232 interface.
'''

if __name__ == "__main__":

    # Parameters
    time_step  = 0.1

    cortix = Cortix(use_mpi=False)

    # DADOS module.
    dados = Dados()
    # Port def.
    rs232_port = Port('rs-232')
    dados.add_port(rs232_port)
    dados.rs232_filename = 'ir-7040'
    dados.rs232_request_string = '\r\nP0001 01245689BCDMNVWYZaOdghin 55}'

    # DataPlot module.
    data_plot = DataPlot()
    data_plot.title = 'IR-7040 Data Acquisition'
    data_plot.dpi = 300
    # Port def.
    plot_port = Port('viz-data')
    data_plot.add_port(plot_port)

    # Network connectivity
    rs232_port.connect(plot_port)

    # Add modules to Cortix
    cortix.add_module(dados)
    cortix.add_module(data_plot)

    # Run application
    cortix.run()
