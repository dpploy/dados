import serial
import time
import datetime


def test_serial(command):
    ser=serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=5,
                            stopbits = serial.STOPBITS_ONE,
                            parity = serial.PARITY_NONE,
                            bytesize=serial.EIGHTBITS)
    print('COMM START')
    olddata=''
    for i in range(10):
        ser.write(command.encode('ascii'))
        original_line=ser.readline()
        line = str(original_line.decode('utf-8', errors='replace').strip())
        if line == olddata:
            time.sleep(.25)
            continue
        olddata=line
        print(line)

def create_command(string):

    CR='\r'
    LF='\n'
    RC='P'
    unit='0001'
    space=' '
    """
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
"""
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
if __name__ == "__main__":
    command = create_command('01245689BCDMNVWYZaOdghin')
    print(command)
    try:
        test_serial(command)
    except:
        print("serial port in use")
