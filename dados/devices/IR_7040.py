import os, sys, time, datetime, traceback, threading
import serial
import pandas as pd


class IR_7040(threading.Thread):
    def __init__(self,port='/dev/ttyUSB0',baudrate=9600,timeout=5,command_string='12489BOdg'):
        self.command_string = command_string
        self.request_string = self.create_command(command_string)
        print(self.request_string)
##        self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=5,
##                            stopbits = serial.STOPBITS_ONE,
##                            parity =IR_ serial.PARITY_NONE,
##                            bytesize=serial.EIGHTBITS)
        self.df = dict()
        self.make_header()
        
    def read_line(self):
        #self.timestamp=str(datetime.datetime.now())[:-7]
        #line = ser.readline.decode()
        line = 'Hello'
        return line
    def create_command(self,string):

        CR='\r'
        LF='\n'
        RC='P'
        unit='0001'
        space=' '
        
        command=CR+LF+RC+unit+space+string+space
        
            # Convert the string to ASCII
        ascii_vals = [ord(i) for i in command]

        # XOR each ascii value
        checksum = ascii_vals[0]
        for i in range(1, len(ascii_vals)):
            checksum ^= ascii_vals[i]

        # Convert the checksum to hex and print it
        checksum = hex(checksum).upper()[2:]
        complete_command=command+checksum+'}'
        return complete_command
    def make_header(self):
        dic = {}
        dic['P'] ='Send requested values'
        dic['0']='Status group'
        dic['1']='Rate Filtered (Chan 1)'
        dic['2']='Rate Unfiltered (Chan 1)'
        dic['4']='Dose (Chan 1)'
        dic['5']='Rate Alarm: High (Chan 1)'
        dic['6']='Rate Alarm: Warning (Chan 1)'
        
        dic['8']='Rate Filtered (Chan 2)'
        dic['9']='Rate Unfiltered (Chan 2)'
        dic['B']='Dose (Chan 2)'
        dic['C']='Rate Alarm: High (Chan 2)'
        dic['D']='Rate Alarm: Warning (Chan 2)'

        dic['K']='Clear New Data flag'
        dic['L']='Clear Modified Alarm Setpoint'

        dic['M']='Leak Rate: Gallons/Day'
        dic['N']='Leak Rate: %Power Level'

        dic['V']='Rate Filtered (Chan 3)'
        dic['W']='Rate Unfiltered (Chan 3)'
        dic['Y']='Dose (Chan 3)'
        dic['Z']='Rate Alarm: High (Chan 3)'
        dic['a']='Rate Alarm: Warning (Chan 3)'
        
        dic['O'] = 'Rate Filtered (Chan 4)'
        dic['d'] = 'Rate Unfiltered (Chan 4)'
        dic['g'] = 'Dose (Chan 4)'
        dic['h'] = 'Rate Alarm: High'
        dic['i'] = 'Rate Alarm: Warning (chan 4)'
        dic['n'] = 'Probe Status'
        header = ''
        for s in self.command_string:
            assert s in dic, "Error, {} not a recognized command string".format(s)
            self.df[dic[s]] = []
        print(self.df)
    def help(self):
        print("""
Many commands are not implemented in the IR-7040
The default command is: '12489BOdg'

Full command list and descriptions:
    'P'='Send requested values'
    '0'='Status group'
    '1'='Rate Filtered (Chan 1)'
    '2'='Rate Unfiltered (Chan 1)'
    '4'='Dose (Chan 1)'
    '5'='Rate Alarm: High (Chan 1)'
    '6'='Rate Alarm: Warning (Chan 1)'
    
    '8'='Rate Filtered (Chan 2)'
    '9'='Rate Unfiltered (Chan 2)'
    'B'='Dose (Chan 2)'
    'C'='Rate Alarm: High (Chan 2)'
    'D'='Rate Alarm: Warning (Chan 2)'

    'K'='Clear New Data flag'
    'L'='Clear Modified Alarm Setpoint'

    'M'='Leak Rate: Gallons/Day'
    'N'='Leak Rate: %Power Level'

    'V'='Rate Filtered (Chan 3)'
    'W'='Rate Unfiltered (Chan 3)'
    'Y'='Dose (Chan 3)'
    'Z'='Rate Alarm: High (Chan 3)'
    'a'='Rate Alarm: Warning (Chan 3)'
    
    'O = Rate Filtered (Chan 4)'
    'd = Rate Unfiltered (Chan 4)'
    'g = Dose (Chan 4)'
    'h = Rate Alarm: High'
    'i = Rate Alarm: Warning (chan 4)'
    'n'='Probe Status'
""")
    def __del__(self):
        return
        try:
            self.ser.close()
        except Exception as e:
            print(traceback.print_exc())
