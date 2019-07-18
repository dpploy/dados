import serial
import serial.tools.list_ports
import datetime
import time
import os
from send_report import send_report

for chan in list(serial.tools.list_ports.comports()):
        print(chan)


class Comm:
        def __init__(self):
                self.timestamp=str(datetime.datetime.now())
                self.date= self.timestamp.split(" ")[0]
                self.counter=0 # trigger send emails at some value
                self.Time_ID()    # class function helper
                self.start_comm() # class  function helper

        def Time_ID(self):
                self.datetimestamp = datetime.datetime.now()
                self.timestamp=str(datetime.datetime.now()) # not used now
                self.counter+=1
                
              #  if self.date != self.timestamp.split(" ")[0] or self.counter <=10800:
                if self.counter >=5000:
                        self.counter=0
                        olddate=self.date # save current date
                        oldfile='data/data-collected'+olddate+'.txt'
                        app = send_report(oldfile,self.timestamp)
                self.date= self.timestamp.split(" ")[0] # new date


        def start_comm(self):
                # hard-coded port; note timeout 5 seconds
                ser=serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=5,
                                  stopbits = serial.STOPBITS_ONE,
                                  parity = serial.PARITY_NONE,
                                  bytesize=serial.EIGHTBITS)
                #not used timeID=str(datetime.datetime.now())[-6:]
                time.sleep(1)
                                  
                # ADM protocol 
                # 014568 0:unit number; 1: dose rate, etc`
                sentdata='\r\nP0001 014568 58}'
                olddata=''
                print('start')
                while True:
                        # \r is carriage return; \n line feed
                        ser.write('\r\nP0001 014568 58}'.encode('ascii'))

                        line=ser.readline() # time out of 5 s; return byte object
                        line = str(line.decode('utf-8', errors='replace').strip())
                        # strip takes \r\n from line
                        if line == olddata:
                                time.sleep(0.1)
                                continue
                        olddata=line
                        self.Time_ID()
                        print(line)
                        f=open('data/data-collected{}.txt'.format(self.date),'a')
                        f.write('Request: {} Response: {} Timestamp: {}\n'.format(sentdata.strip(),line,self.timestamp))
                        f.close()

if __name__=='__main__':
        for folder in ['data','report_files']:
                if not os.path.exists(folder):
                        os.makedirs(folder)
        app = Comm()

