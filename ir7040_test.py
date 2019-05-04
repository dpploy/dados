import serial
import time
import datetime

ser=serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=5,
                        stopbits = serial.STOPBITS_ONE,
                        parity = serial.PARITY_NONE,
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
    olddata=line
    print(line)
