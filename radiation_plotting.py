import socket
from collections import deque
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import traceback
s = socket.socket()             # Create a socket object
host = '10.253.90.164'          # Get local machine name
port = 60000                    # Reserve a port for your service.

s.connect((host, port))
a1=[deque(),deque()]
b1=[deque(),deque()]

fig,ax=plt.subplots(1,1)
plt.ion()
#plt.show()
ax.xaxis_date()
fig.autofmt_xdate(rotation=45)
plt.gcf().autofmt_xdate()
myfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
plt.gca().xaxis.set_major_formatter(myfmt)
ax.relim()
ax.grid()
while True:
        data = s.recv(100)
        line = data.decode().strip()
        spline = line.split(', ')
        print(line)
        ch1=float(spline[2])
        ch2=float(spline[4])
        timestamp=spline[-1]
        dtime = datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S')
        print(ch1,ch2)
        a1[1].appendleft(ch1)
        b1[1].appendleft(ch2)
        a1[0].appendleft(dtime)
        b1[0].appendleft(dtime)
        ax.plot(a1[0],a1[1],'r', label='channel 1')
        ax.plot(b1[0],b1[1],'b',label='Channel 2')
        ax.legend()
        plt.draw()
        plt.pause(0.1)
        del ax.lines[:10]
