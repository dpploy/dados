import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas.plotting._converter as pandacnv
pandacnv.register()
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import os, datetime
import tkinter as tk
import threading
class App(tk.Frame):
    def __init__(self, parent,*args, **kwargs):
        for f in ['input','output']:
            if not os.path.isdir(f):
                os.makedirs(f)
        self.plot_chan=tk.StringVar()
        self.plot_chan.set('1')
        x,y = self.start()
        frame1=tk.Frame(master=parent)
        frame1.pack()
        frame2=tk.Frame(master=parent)
        frame2.pack()
        frame3=tk.Frame(master=parent)
        frame3.pack()
        self.fig,self.ax = plt.subplots(1,1)
        self.line, = self.ax.plot(x,y)
        self.ax.xaxis_date()
        self.fig.autofmt_xdate(rotation=45)
        plt.gcf().autofmt_xdate()
        myfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
        plt.gca().xaxis.set_major_formatter(myfmt)
        self.ax.autoscale(enable=True)
        self.ax.grid()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame1)
        self.canvas.get_tk_widget().pack()

        self.toolbar = NavigationToolbar2Tk(self.canvas, parent)
        self.toolbar.update()
        self.canvas._tkcanvas.pack()
        self.canvas.mpl_connect("key_press_event", self.on_key_press)
        self.canvas.draw()
        
        lbutton = tk.Button(master=frame2, text="<<", command=lambda: self.update_plot('left'))
        lbutton.grid(column=0,row=0)
        cbutton = tk.Button(master=frame2, text="Refresh", command=lambda: self.update_plot('start'))
        cbutton.grid(column=1,row=0)
        rbutton = tk.Button(master=frame2, text=">>", command=lambda: self.update_plot('right'))
        rbutton.grid(column=2,row=0)

        for n in range(1,13):
            tk.Radiobutton(master=frame3,text=f'{n}',variable=self.plot_chan,value=str(n)).pack(side=tk.LEFT)
        self.update_plot('left')
    def update_plot(self,text):
        if text=='left':
            self.plot_date = self.plot_date - datetime.timedelta(days=1)
        if text=='right':
            self.plot_date = self.plot_date + datetime.timedelta(days=1)
        channum = self.plot_chan.get()
        for chan in self.dic:
            if chan != channum:
                continue
            x,y=[],[]
            for t,z in zip(self.dic[chan][0],self.dic[chan][1]):
                if self.plot_date.date() == t.date():
                    x.append(t)
                    y.append(z)
            if len(x) == 0:
                tk.messagebox.showinfo("Warning", f"No data is found for this day:\n   {self.plot_date.date()}")
                if text=='left':
                    self.plot_date = self.plot_date + datetime.timedelta(days=1)
                if text=='right':
                    self.plot_date = self.plot_date - datetime.timedelta(days=1)
                return
            try:
                
                self.line.set_data(x,y)

                self.ax.set_title(f'Channel: {chan}, {self.plot_date.date()}')
                
                self.ax.relim()
                self.ax.autoscale(enable=True)
                self.canvas.draw()
                self.toolbar.update()
            except Exception as e:
                print(e)
                return

    def on_key_press(self, event):
        key_press_handler(event, self.canvas, self.toolbar)
        self.toolbar.update()
    def start(self):
        c = 0
        self.dic = {}
        with open('RateData_5-7-19.csv') as file:
            for line in file:
                c+=1
                if c==1:
                    continue
                line = line.strip().split(',')
                chan = line[1]
                if chan not in self.dic:
                    self.dic[chan] = ([],[])
                timestamp = datetime.datetime.strptime(line[0], "%m/%d/%Y %I:%M:%S %p")
                self.dic[chan][1].append(float(line[2]))
                self.dic[chan][0].append(timestamp)
            self.plot_date = datetime.datetime.strptime(line[0].split()[0], "%m/%d/%Y")
        x,y=[],[]
        for chan in self.dic:
            if chan != self.plot_chan.get():
                continue
            for t,z in zip(self.dic[chan][0],self.dic[chan][1]):
                if self.plot_date.date() == t.date():
                    x.append(t)
                    y.append(z)
        return x,y

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
