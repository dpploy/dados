import matplotlib, os, sys
matplotlib.use('Agg', warn=False)
import matplotlib.pyplot as plt
from cortix.src.module import Module
import pandas as pd

class Dataplot(Module):
    def __init__(self):
        super().__init__()
        self.plot_title = 'DADOS Data Plot'
        self.plot_dpi = 300
        self.plot_list = []
    def run(self):
        self.port_dic = {}
        while True:
            for i in self.ports:
                if str(i) not in self.port_dic:
                    self.port_dic[str(i)] = []
                data = self.recv(i)
            print(data)
            if data == 'Done':
                break
            self.port_dic[str(i)].append(data)

        self.make_plot()
        return
    
    def make_plot(self):
        
        for port in self.port_dic:
            datadic = {}
            for dic in self.port_dic[port]:
                for i in dic:
                    if i not in datadic:
                        datadic[i] = []
                    for line in dic[i]:
                        datadic[i].append(line)
                #fig = plt.figure()
                #ax = fig.add_subplot(111)
                #line, = plt.plot([])
            df = pd.DataFrame.from_dict(datadic)
            file_name = 'tocsvtest.csv'
            df.to_csv(file_name, sep=',', encoding='utf-8',index=False)
            for i in datadic:
                print(i)#,datadic[i])
                if i in self.plot_list or self.plot_list==[]:
                    if i=='Timestamp':continue
                    plt.plot(datadic[i])
                    title = self.plot_title+' '+i
                    plt.title(title)
                    plt.savefig('{}.png'.format(i))
                        







