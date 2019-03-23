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
RS-232 serials port communication class
'''
#*********************************************************************************
import os, sys, io, time
import logging
#*********************************************************************************

class RS_232():
    r'''
    RS-232 class for Dados
    '''

#*********************************************************************************
# Construction 
#*********************************************************************************

    def __init__( self,
                  slot_id,
                  input_full_path_file_name,
                  work_dir,
                  ports = list(),
                  cortix_start_time = 0.0,
                  cortix_final_time = 0.0,
                  cortix_time_unit  = None 
                ):

        # Sanity test
        assert isinstance(slot_id, int), '-> slot_id type %r is invalid.' % type(slot_id)
        assert isinstance(ports, list), '-> ports type %r is invalid.'  % type(ports)
        assert len(ports) > 0
        assert isinstance(cortix_start_time,float), '-> time type %r is invalid.' % \
                type(cortix_start_time)
        assert isinstance(cortix_final_time, float), '-> time type %r is invalid.' % \
                type(cortix_final_time)
        assert isinstance(cortix_time_unit, str), '-> time type %r is invalid.' % \
                type(cortix_time_unit)

        # Logging
        self.__log = logging.getLogger('launcher-dados_'+str(slot_id)+'.cortix_driver.dados')
        self.__log.info('initializing an object of Dados()')

        # Member data 
        self.__slot_id = slot_id
        self.__ports  = ports

        if work_dir[-1] != '/': work_dir = work_dir + '/'
        self.__wrkDir = work_dir

        # Signal to start operation
        self.__goSignal = True    # start operation immediately
        for port in self.__ports: # if there is a signal port, start operation accordingly
            (portName,portType,thisPortFile) = port
            if portName == 'go-signal' and portType == 'use': self.__goSignal = False

        self.__setup_time = 1.0  # min; a delay time before starting to run

        # Input ports
        # Read input information if any

        #fin = open(input_full_path_file_name,'r')

        return

#*********************************************************************************
# Public member functions
#*********************************************************************************

    def execute( self, cortix_time=0.0, cortix_time_step=0.0 ):
        '''
        Developer must implement this method.
        Evolve system from cortix_time to cortix_time + cortix_time_step
        '''

        s = 'execute('+str(round(cortix_time,2))+'[min]): '
        self.__log.debug(s)

        # Developer implements helper method, for example
        #self.__evolve( self, cortix_time, cortix_time_step ):

        return

#*********************************************************************************
# Private helper functions (internal use: __)
#*********************************************************************************


#======================= end class Dados: ========================================
