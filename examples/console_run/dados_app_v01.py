#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit environment
# https://cortix.org
#
# All rights reserved, see COPYRIGHT for full restrictions.
# https://github.com/dpploy/cortix/blob/master/COPYRIGHT.txt
#
# Licensed under the University of Massachusetts Lowell LICENSE:
# https://github.com/dpploy/cortix/blob/master/LICENSE.txt
'''
Cortix: a program for system-level modules coupling, execution, and analysis.

Cortix is a library and it is used by means of a driver. This file is a simple example
of a driver. Many Cortix objects can be ran simultaneously; a single object
may be sufficient since many simulation/tasks can be ran via one object.

As Cortix evolves additional complexity may be added to this driver and/or other
driver examples can be created.
'''
#*********************************************************************************
import os, sys
from cortix import Cortix

sys.path.append("../..")
import rs_232
#*********************************************************************************

def main():

    pwd = os.path.dirname(__file__)
    full_path_config_file = os.path.join(pwd, '../input/cortix-config-dados.xml')
    print('main')
 # NB: if another instantiation of Cortix occurs, the cortix wrk directory specified
 #     in the cortix configuration file must be different, else the logging facility 
 #     will have log file collision.

#cortix1 = Cortix( 'cortix-dados', full_path_config_file ) # see cortix-config.xml
#
#cortix1.run_simulations( task_name='solo-dados' )
#*********************************************************************************
# Usage: -> python main-dados.py or ./main-dados.py
if __name__ == "__main__":
    main()
