import os
import matplotlib.pyplot as plt
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class send_report:
    def __init__(self,filename,timestamp):
        self.filename= filename
        self.timestamp=timestamp
        print(self.filename)

        self.parse_file()

    def parse_file(self):
        ch1,ch2=[],[]
        c=0
        with open(self.filename) as file:
            for line in file:
                c+=1
                line=line.strip().split()
                ch1rate = line[8]
                scinum = ch1rate[0]+'.'+ch1rate[1:3]+'E'+ch1rate[3:]
                ch1value = float(scinum)
                ch1.append(ch1value)
                
                ch2rate = line[12]
                scinum2 = ch2rate[0]+'.'+ch2rate[1:3]+'E'+ch2rate[3:]
                ch2value = float(scinum2)
                ch2.append(ch2value)
            file.close()

        fig,ax=plt.subplots(1,1)
        ax.plot(ch1,label='Chan#1')
        ax.plot(ch2,label='Chan#2')
        ax.set_title('Ratemeter data collect 1/25/19-1/28/19')
        ax.set_ylabel('Dose Rate mR/hr')
        self.fig_file=os.path.join('report_files','Report_figure_{}.png'.format(self.timestamp))
        print(self.fig_file)
        plt.savefig(self.fig_file)
        
        self.send_email()
        
    def send_email(self):
        SUBJECT = "Email Data"

        img_data = open(self.fig_file, 'rb').read()
        
        msg = MIMEMultipart()
        msg['Subject'] = SUBJECT 
        msg['From'] = 'seamus_gallagher@student.uml.edu'
        msg['To'] = ', '.join(['seamusdgallagher@gmail.com','Valmor_deAlmeida@uml.edu'])

        text = MIMEText("Automatically Generated Data Report")
        msg.attach(text)
        image=MIMEImage(img_data, name=os.path.basename(self.fig_file))
        msg.attach(image)

        s = smtplib.SMTP('smtp-mail.outlook.com','587')
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login('seamus_gallagher@student.uml.edu', 'Seaseasea23!')
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()

        print('sent email?')




if __name__=='__main__':
    for folder in ['data','report_files']:
        if not os.path.exists(folder):
            os.makedirs(folder)
    filename='data-collected2019-01-25.txt'
    app = send_report(filename)
