import socket
from collections import deque
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import traceback
import time

s = socket.socket()             # Create a socket object
host = 'xx.xxx.xx.xx'              # Get local machine name
port = 60000                    # Reserve a port for your service.

s.connect((host, port))
data = s.recv(40).decode().split(', ')
port=int(data[1])
host=data[3]
s.close()

print('port name = {}, host name= {}'.format(port,host))
time.sleep(1.5)
s = socket.socket()
s.connect((host, port))
a1=[deque(),deque()]
b1=[deque(),deque()]
c1=[deque(),deque()]

fig,(ax,ax2,ax3) =plt.subplots(3,1)
plt.ion()
ax.xaxis_date()
fig.autofmt_xdate(rotation=45)
plt.gcf().autofmt_xdate()
myfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
plt.gca().xaxis.set_major_formatter(myfmt)
ax.set_ylabel('Rate')
ax2.set_ylabel('Rate')
ax3.set_ylabel('Rate')
fig.suptitle('Intelligent Ratemeter 7040 Data')
ax.set_title('Channel 1')
ax2.set_title('Channel 2')
ax3.set_title('Channel 4')
ax.relim()
ax.grid()
ax2.grid()
ax3.grid()
while True:
    data = s.recv(100)
    line = data.decode().strip()
    spline = line.split(', ')
    if len(spline)<10:
        continue
    try:
        ch1=float(spline[2])
        ch2=float(spline[4])
        ch4=float(spline[6])
        timestamp=spline[-1]
        dtime = datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S')
    except:
        plt.pause(0.1)
        continue

    a1[1].appendleft(ch1)
    b1[1].appendleft(ch2)
    a1[0].appendleft(dtime)
    b1[0].appendleft(dtime)
    c1[1].appendleft(ch4)
    c1[0].appendleft(dtime)
    ax.plot(a1[0],a1[1],'r', label='channel 1')
    ax2.plot(b1[0],b1[1],'b',label='Channel 2')
    ax3.plot(c1[0],c1[1],'g',label='Channel 4')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.draw()
    plt.pause(0.1)
    del ax.lines[:10]

