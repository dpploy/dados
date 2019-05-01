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
Dados module in Cortix
'''
#*********************************************************************************
import os, sys, io, time
import logging

from cortix.src.utils.xmltree import XMLTree
from .rs_232 import RS_232

from .dados_simulator import simulator

#*********************************************************************************

class Dados():
    r'''
    Dados module for Cortix
    '''

#*********************************************************************************
# Construction 
#*********************************************************************************

    def __init__( self,
                  slot_id,
                  input_full_path_file_name,
                  manifesto_full_path_file_name,
                  work_dir,
                  ports = list(),
                  cortix_start_time = 0.0,
                  cortix_final_time = 0.0,
                  cortix_time_step = 0.0,
                  cortix_time_unit = None 
                ):

        # Sanity test
        assert isinstance(slot_id, int), '-> slot_id type %r is invalid.' % type(slot_id)
        assert isinstance(ports, list), '-> ports type %r is invalid.'  % type(ports)
        assert len(ports) > 0
        assert isinstance(cortix_start_time,float), '-> time type %r is invalid.' % \
                type(cortix_start_time)
        assert isinstance(cortix_final_time, float), '-> time type %r is invalid.' % \
                type(cortix_final_time)
        assert isinstance(cortix_time_step, float), '-> time step type %r is invalid.' % \
                type(cortix_time_step)
        assert isinstance(cortix_time_unit, str), '-> time type %r is invalid.' % \
                type(cortix_time_unit)

        # Logging
        self.__log = logging.getLogger('launcher-dados_'+str(slot_id)+'.cortix_driver.dados')
        self.__log.info('initializing an object of Dados()')

        # Read the manisfesto
        self.__read_manifesto( manifesto_full_path_file_name )
        self.__log.info(self.__port_diagram)

        # Member data 
        self.__slot_id = slot_id
        self.__ports  = ports

        if work_dir[-1] != '/': work_dir = work_dir + '/'
        self.__wrkDir = work_dir

        # Start external devices 
        for port in self.__ports: # if there is a connected device, start its port
            (portName,portType,thisPortHardware) = port
            if portName == 'rs-232' and portType == 'use':
                device_name = thisPortHardware.split('/')[-1]
                self.__rs_232 = RS_232( device_name = device_name )

        self.__setup_time = 1.0  # min; a delay time before starting to run

        # Input ports
        # Read input information if any

        #fin = open(input_full_path_file_name,'r')

        # if a serial port is wanted create this variable
        # add conditional to create this or not

        #self.__serial_232_port = RS_232()

        return

#*********************************************************************************
# Public member functions
#*********************************************************************************

    def call_ports( self, cortix_time=0.0 ):
        '''
        Developer must implement this method.
        Transfer data at cortix_time
        '''

        # provide data using the 'provide-port-name' of the module
        #self.__provide_data( provide_port_name='provide-port-name', at_time=cortix_time )

        # use data using the 'use-port-name' of the module
        #self.__use_data( use_port_name='use-port-name', at_time=cortix_time )

        return

    def execute( self, cortix_time=0.0, cortix_time_step=0.0 ):
        '''
        Developer must implement this method.
        Evolve system from cortix_time to cortix_time + cortix_time_step
        '''

        s = 'execute('+str(round(cortix_time,2))+'[min]): '
        self.__log.debug(s)


        #simulator()

        return

#*********************************************************************************
# Private helper functions (internal use: __)
#*********************************************************************************

    def __provide_data( self, provide_port_name=None, at_time=0.0 ):

        # Access the port file
        port_file = self.__get_port_file( provide_port_name = provide_port_name )

        # Provide data to port files
        #if provide_port_name == 'provide-port-name' and port_file is not None: 
        #   self.__provide_mymodule_method( port_file, at_time )

        return

    def __use_data( self, use_port_name=None, at_time=0.0 ):

        # Access the port file
        port_file = self.__get_port_file( use_port_name = use_port_name )

        # Use data from port file
        #if use_port_name == 'use-port-name' and port_file is not None:  
        #   self.__use_mymodule_method( port_file, at_time )

        return

    def __get_port_file( self, use_port_name=None, provide_port_name=None ):
        '''
        This may return a None port_file
        '''

        port_file = None

        #..........
        # Use ports
        #..........
        if use_port_name is not None:

            assert provide_port_name is None

            for port in self.__ports:
               (portName,portType,thisPortFile) = port
               if portName == use_port_name and portType == 'use':
                   port_file = thisPortFile

            if port_file is None: return None

            max_n_trials = 50
            n_trials     = 0
            while os.path.isfile(port_file) is False and n_trials <= max_n_trials:
                n_trials += 1
                time.sleep(0.1)

            if n_trials > max_n_trials:
                s = '__get_port_file(): waited ' + str(n_trials) + ' trials for port: '\
                        + port_file
                self.__log.warn(s)

            assert os.path.isfile(port_file) is True, \
                    'port_file %r not available; stop.' % port_file

        #..............
        # Provide ports
        #..............
        if provide_port_name is not None:

            assert use_port_name is None

            for port in self.__ports:
                (portName,portType,thisPortFile) = port
            if portName == provide_port_name and portType == 'provide':
                port_file = thisPortFile

        return port_file

    def __read_manifesto( self, xml_tree_file ):
        '''
        Parse the manifesto
        '''

        assert isinstance(xml_tree_file, str)

        # Read the manifesto
        xml_tree = XMLTree( xml_tree_file=xml_tree_file )

        assert xml_tree.get_node_tag() == 'module_manifesto'

        assert xml_tree.get_node_attribute('name') == 'dados'

        # List of (port_name, port_type, port_mode, port_multiplicity)
        __ports = list()

        self.__port_diagram = 'null-module-port-diagram'

        # Get manifesto data  
        for child in xml_tree.get_node_children():
            (elem, tag, attributes, text) = child

            if tag == 'port':

                text = text.strip()

                assert len(attributes) == 3, "only <= 3 attributes allowed."

                tmp = dict()  # store port name and three attributes

                for attribute in attributes:
                    key = attribute[0].strip()
                    val = attribute[1].strip()

                    if key == 'type':
                        assert val == 'use' or val == 'provide' or val == 'input' or\
                            val == 'output', 'port attribute value invalid.'
                        tmp['port_name'] = text  # port_name
                        tmp['port_type'] = val   # port_type
                    elif key == 'mode':
                        file_value = val.split('.')[0]
                        assert file_value == 'file' or file_value == 'directory' or\
                               file_value == 'hardware','port attribute value invalid.'
                        tmp['port_mode'] = val
                    elif key == 'multiplicity':
                        tmp['port_multiplicity'] = int(val)  # port_multiplicity
                    else:
                        assert False, 'invalid port attribute: %r=%r. fatal.'%\
                                (key,val)

                assert len(tmp) == 4
                store = (tmp['port_name'], tmp['port_type'], tmp['port_mode'],
                         tmp['port_multiplicity'])

                # (port_name, port_type, port_mode, port_multiplicity)
                __ports.append(store)

                # clear
                tmp   = None
                store = None

            if tag == 'diagram':

                self.__port_diagram = text

            if tag == 'ascii_art':

                self.__ascii_art = text

        return

#======================= end class Dados: ========================================
