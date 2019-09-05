import matplotlib, os, sys, datetime, threading
matplotlib.use('Agg', warn=False)
import matplotlib.pyplot as plt
from cortix.src.module import Module
import pandas as pd

class Dataplot(Module):
    def __init__(self,modules=1):
        super().__init__()
        self.plot_title = 'DADOS Data Plot'
        self.plot_dpi = 300
        self.plot_list = []
        self.experiment_name = 'DADOS'
        self.length = modules
    def run(self):
        self.port_dic = {}
        if not os.path.isdir('output'):
            os.makedirs('output')
        c=0
        threads=[]
        while True:
            for port in self.ports:
                if str(port) not in self.port_dic:
                    self.port_dic[str(port)] = []
                worker = threading.Thread(target=lambda:self.recv_data(port))
                worker.daemon = True
                worker.start()
                threads.append(worker)
            for i in threads:
                i.join()
            break

        self.make_plot()
        return
    def recv_data(self,port):
        while True:
            data = self.recv(port)
            print(data)
            if data == 'Done':
                return
            self.port_dic[str(port)].append(data)

    def make_plot(self):
        print('Creating Plots') 
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
            t=str(datetime.datetime.now())
            filetime= t[:4]+t[5:7]+t[8:10]+'_'+t[11:13]+t[14:16]+t[17:19]
            file_name = 'output/{}_{}_{}'.format(self.experiment_name,port,filetime)
            df.to_csv(file_name+'.csv', sep=',', encoding='utf-8',index=False)
            for i in datadic:
                if i=='Timestamp':continue
                if i in self.plot_list or self.plot_list==[]:
                    plt.plot(datadic[i])
                    title = self.plot_title+' '+port+' '+i
                    plt.title(title)
                    plt.savefig(file_name+'_'+i+'.png')
                    plt.close()    







