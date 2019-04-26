from daqhats import mcc118, OptionFlags, HatIDs, HatError
import time
import daqhats
class app:
    def __init__(self):
        
        self.main()
    def main(self):

        lis=daqhats.hat_list()
        for i in lis:
            print(i)
            ad=i.address
        hat=mcc118(ad)
        options = OptionFlags.DEFAULT
        chan=0
        lis=[]
        while True:
            value = hat.a_in_read(0, options)
            print(value)
            time.sleep(0.1)
if __name__ == '__main__':
    run=app()


