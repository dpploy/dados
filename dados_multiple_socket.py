import serial
import time
import os
import datetime
import socket
import threading
import traceback


class Comm:


    def __init__(self):
            self.socket_list = []
            self.init_port=60000
            self.port=60001
            self.host='10.253.90.164'


            worker=threading.Thread(target=self.__start_comm)
            worker.start()
            socket_worker=threading.Thread(target=self.__initial_socket(),name='socket_worker')
            socket_worker.start()




    def __initial_socket(self):
        try:
            print('initial socket')
            sock=socket.socket()
            sock.settimeout(60)
            sock.bind((self.host,self.init_port))
            sock.listen(5)
            conn,addr=sock.accept()
            self.port+=1
            string='port, {}, host, {}'.format(self.port,self.host)
            string+=' '*(40-len(string))
            for n in range(2):
                conn.send(string.encode())
                time.sleep(0.5)
            print('Socket Initialized!')
            conn.close()

            s = socket.socket()
            s.settimeout(60)
            print(self.port)
            s.bind((self.host, self.port))
            s.listen(5)
            conn, addr = s.accept()
            self.socket_list.append(conn)
            print('Connected to:{},{}'.format(conn,addr))
        except Exception as e:
            return


            pass
            #print(e)

        return



    def __start_comm(self):
        ser=serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=5, \
                stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_NONE, \
                bytesize=serial.EIGHTBITS)

        print('COMM START')

        olddata=''

        while True:
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
            for n in range(2,8):
                splitline[n] = splitline[n][0]+'.'+splitline[n][1:3]+'e'+splitline[n][3:]
            filename='data/Stack_monitor_data_{}.csv'.format(str(datetime.datetime.now())[:10])
            if not os.path.isfile(filename):
                with open(filename,'a') as f:
                    f.write('Type, Callback, Ch1_rate_filtered, Ch1_rate_unfiltered, Ch2_rate_filtered, Ch2_rate_unfiltered, Ch4_rate_filtered, Ch4_rate_unfiltered, Checksum, Date and Time\n')
            padding = ', '.join(splitline)
            padding += (" " * (100 - len(padding)))
            c=0
            for conn in self.socket_list:
                try:
                    conn.send(padding.encode())
                
                except socket.BrokenPipeError as e:
                    print(traceback.print_exc())
                    conn.close()
                    del self.socket_list[c]
                c+=1

            if 'init_woker' not in [f.name for f in threading.enumerate()]:
                socket_worker=threading.Thread(target=self.__initial_socket,name='init_worker')
                socket_worker.start()
            with open(filename,'a') as f:
                f.write('{}\n'.format(', '.join(splitline)))
        self.conn.close()




if __name__=='__main__':
    for folder in ['data',]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    app = Comm()

