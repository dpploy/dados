import os,sys,time,datetime,threading
from rs_232 import RS_232

class Neuron:
    def __init__(self, task=None,*args,**kwargs):
        print(kwargs)
        self.task=task
        self.wrk_dir=kwargs['wrk_dir']
        self.name=kwargs['name']
        self.event=threading.Event()
        timestamp=str(datetime.datetime.now())
        self.timeID=timeID=timestamp[:4]+timestamp[5:7]+timestamp[8:10]+timestamp[11:13]+timestamp[14:16]+timestamp[17:19]+timestamp[20:]
        self.tempfile = os.path.join(self.wrk_dir,self.name)+self.timeID+'.csv'
        with open(self.tempfile,'w') as file:
            file.write('')
        self.worker = threading.Thread(target=task,args=(self.timeID,self.event))
        self.worker.daemon=True
        self.worker.start()

    def read_line(self):
        line = 'no data'
        try:
            with open(self.tempfile) as file:
                line = file.readline()
                #print(line)
        except Exception as e:
            pass
            #print(e)
        return line

def test_fun():
    print('test func')
    time.sleep(1)
    print('goodbye')

if __name__=='__main__':
    Neuron(task=test_fun)
