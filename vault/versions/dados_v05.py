import os, datetime
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import matplotlib.dates as mdates
import tkinter as tk
from cortix.src.port import Port
from cortix.src.cortix_main import Cortix
from cortix.src.peon import Peon
from stack_receiver import Receiver

class App:
    def __init__(self,parent):
        self.parent = parent
        self.frame1=tk.Frame(master=self.parent)
        self.frame1.grid(column=0,row=0)
        self.frame2=tk.Frame(master=self.parent)
        self.frame2.grid(column=0,row=1)

        self.fig,(self.ax,self.ax2,self.ax3) = plt.subplots(3,1)
        self.a1 = deque([0]*100)
        self.line, = self.ax.plot(self.a1)
        self.line2, = self.ax2.plot([])
        self.line3, = self.ax3.plot([])
        
        self.ax.set_title('DADOS')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
##        self.ax.xaxis_date()
##        self.fig.autofmt_xdate(rotation=45)
##        plt.gcf().autofmt_xdate()
##        myfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
##        plt.gca().xaxis.set_major_formatter(myfmt)
        self.ax.set_ylabel('Rate')
        self.ax2.set_ylabel('Rate')
        self.ax3.set_ylabel('Rate')
        self.fig.suptitle('Intelligent Ratemeter 7040 Data')
        self.ax.set_title('Channel 1')
        self.ax2.set_title('Channel 2')
        self.ax3.set_title('Channel 4')
        self.ax.relim()
        self.ax.grid()
        self.ax2.grid()
        self.ax3.grid()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame1)
        self.canvas.get_tk_widget().pack()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame1)
        self.toolbar.update()
        self.canvas._tkcanvas.pack()
        self.canvas.mpl_connect("key_press_event", self.on_key_press)
        self.canvas.draw()
        self.start_cortix()
        self.parent.after(0, self.update_plot)

    def update_plot(self):

        line = self.receiver.recv()
        spline = line.split(', ')
        if len(spline)<10:
            self.parent.after(40, self.update_plot)
        print(line)
        try:
            ch1=float(spline[2])
            ch2=float(spline[7])
            ch4=float(spline[14])
            timestamp=spline[-1]
            dtime = datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(e)
            self.parent.after(40, self.update_plot)
        self.a1.appendleft(ch1)
        self.a1.pop()
        self.line.set_ydata(self.a1)
        self.ax.autoscale()
        self.ax.relim()
        self.canvas.draw()
        self.parent.after(40, self.update_plot)
    def start_cortix(self):
        app = Receiver()
        self.receiver = Peon(app.run)
        #self.cortix = Cortix()
        #self.cortix.add_module(self.receiver)
        #c.run()
    def on_key_press(self, event):
        key_press_handler(event, self.canvas, self.toolbar)
        self.toolbar.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
