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
import os, sys, io, time, datetime, traceback
import logging

import serial
#*********************************************************************************

class RS_232():
    r'''
    RS-232 class for Dados
    '''

#*********************************************************************************
# Construction 
#*********************************************************************************

    def __init__( self ):

        port = '/dev/ttyUSB0'
        baud_rate = 9600
        timeout = 5

        serial_rs232 = serial.Serial( port=port, baudrate=baud_rate, \
                timeout=timeout, stopbits=serial.STOPBITS_ONE, \
                parity=serial.PARITY_NONE, \
                bytesize=serial.EIGHTBITS )

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

    def create_instance(self,*args,**kwargs):
        #Creates a new thread, then kills main thread
        worker = threading.Thread(target=self.__start_com, name='start_com')
        worker.start()
        return
#*********************************************************************************
# Private helper functions (internal use: __)
#*********************************************************************************
    def __start_com(self):
        self.socket_list = []
        self.init_port=60000
        self.port=60001
        self.host=socket.gethostbyname(socket.gethostname())
        print('Host IP-address: {}'.format(self.host()))
        #initialize serial object, parameters hard-coded for now
        ser=serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=5,
                          stopbits = serial.STOPBITS_ONE,
                          parity = serial.PARITY_NONE,
                          bytesize=serial.EIGHTBITS)
        socket_worker=threading.Thread(target=self.__initialize_socket,name='init_worker')
        socket_worker.start()
        print('COMM START')
        olddata=''
        while True:
            #Send request string, specific to IR7040
            ser.write('\r\nP0001 1289Od 7F}'.encode('ascii'))
            original_line=ser.readline()
            line = str(original_line.decode('utf-8', errors='replace').strip())
            if line == olddata:
                time.sleep(.25)
                continue
            self.timestamp=str(datetime.datetime.now())[:-7]
            olddata=line
            splitline=line.split()
            splitline.append(self.timestamp)
            print(line)
            print(splitline)
            for n in range(2,8):
                splitline[n] = splitline[n][0]+'.'+splitline[n][1:3]+'e'+splitline[n][3:]
            filename='data/Stack_monitor_data_{}.csv'.format(str(datetime.datetime.now())[:10])
            if not os.path.isfile(filename):
                with open(filename,'a') as f:
                    f.write('Type, Callback, Ch1_rate_filtered, Ch1_rate_unfiltered, Ch2_rate_filtered, Ch2_rate_unfiltered, Ch4_rate_filtered, Ch4_rate_unfiltered, Checksum, Date and Time\n')
            padding = ', '.join(splitline)
            commaline=padding
            padding += (" " * (100 - len(padding)))
            c=0
            for conn in self.socket_list:
                try:
                    conn.send(padding.encode())
                except Exception as e:
                    print(traceback.print_exc())
                    conn.close()
                    del self.socket_list[c]
                c+=1

            if 'init_woker' not in [f.name for f in threading.enumerate()]:
                socket_worker=threading.Thread(target=self.__initialize_socket,name='init_worker')
                socket_worker.start()
            with open(filename,'a') as f:
                f.write('{}\n'.format(commaline))
        self.conn.close()

    def __initialize_socket(self):
        try:
            print('initial socket')
            #Initial Socket for establishing permanent Port number
            sock=socket.socket()
            sock.settimeout(60)
            sock.bind((self.host,self.init_port))
            sock.listen(5)
            conn,addr=sock.accept()
            self.port+=1
            string='port, {}, host, {}'.format(self.port,self.host)
            string+=' '*(40-len(string))
            conn.send(string.encode())
            time.sleep(0.5)
            print('Socket Initialized!')
            conn.close()
            #Reestablishes connection with new port
            s = socket.socket()
            s.settimeout(60)
            print(self.port)
            s.bind((self.host, self.port))
            s.listen(5)
            conn, addr = s.accept()
            #new socket connections appended to list
            self.socket_list.append(conn)
            print('Connected to:{},{}'.format(conn,addr))
        except Exception as e:
            return        
        return
#======================= end class Dados: ========================================
