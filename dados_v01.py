import serial
import time
import os
import datetime
import socket
import threading

class Comm:
	def __init__(self):
		self.timestamp=str(datetime.datetime.now())
		self.port = 60000                    # Reserve a port for your service.
		self.s = socket.socket()
		self.s.settimeout(60)
		self.host = '10.253.90.164'      # Get local machine name
		self.s.bind((self.host, self.port))            # Bind to the port
		self.s.listen(5)
		while True:
			self.conn, self.addr = self.s.accept()
			if self.conn:
				worker=threading.Thread(target=self.__start_comm)
				worker.start()
	def __start_comm(self):
		ser=serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=5,
                  		stopbits = serial.STOPBITS_ONE,
                  		parity = serial.PARITY_NONE,
                  		bytesize=serial.EIGHTBITS)

		olddata=''
		while True:
			ser.write('\r\nP0001 1289Od 7F}'.encode('ascii'))
			original_line=ser.readline()
			line = str(original_line.decode('utf-8', errors='replace').strip())
			if line == olddata:
				time.sleep(.25)
				continue
			olddata=line
			splitline=line.split()
			print(line)
			for n in range(2,8):
				splitline[n] = splitline[n][0]+'.'+splitline[n][1:3]+'e'+splitline[n][3:]
			filename='data/Stack_monitor_data_{}.csv'.format(str(datetime.datetime.now())[:10])
			if not os.path.isfile(filename):
				with open(filename,'a') as f:
					f.write('Type, Callback, Ch1_rate_filtered, Ch1_rate_unfiltered, Ch2_rate_filtered, Ch2_rate_unfiltered, Ch4_rate_filtered, Ch4_rate_unfiltered, Checksum\n') 
			padding = ', '.join(splitline)
			padding += (" " * (1024 - len(padding)))
			self.conn.send(padding.encode())
			with open(filename,'a') as f:
				f.write('{}\n'.format(', '.join(splitline)))
		self.conn.close()
if __name__=='__main__':
        for folder in ['data','report_files']:
                if not os.path.exists(folder):
                        os.makedirs(folder)
        app = Comm()

