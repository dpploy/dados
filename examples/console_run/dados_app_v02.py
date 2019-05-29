import threading, os, sys, time
import urwid
sys.path.append('../..')
from rs_232 import RS_232
from mcc_118 import MCC_118

class SwitchingPadding(urwid.Padding):
    def padding_values(self, size, focus):
        maxcol = size[0]
        width, ignore = self.original_widget.pack(size, focus=focus)
        if maxcol > width:
            self.align = "left"
        else:
            self.align = "right"
        return urwid.Padding.padding_values(self, size, focus)


class MainDisplay:
    def __init__(self):
        self.palette = [
                    ('body',         'black',      'light gray', 'standout'),
                    ('header',       'white',      'dark red',   'bold'),
                    ('button normal','light gray', 'dark blue', 'standout'),
                    ('button select','white',      'dark green'),
                    ('button disabled','dark gray','dark blue'),
                    ('edit',         'light gray', 'dark blue'),
                    ('bigtext',      'white',      'black'),
                    ('chars',        'light gray', 'black'),
                    ('exit',         'white',      'dark cyan'),
                        ]
    def main(self):
        self.view, self.exit_view = self.setup_view()
        self.loop = urwid.MainLoop(self.view, self.palette, unhandled_input=self.unhandled_input)
        threading.Thread(target=self.update_display,daemon=True).start()
        self.loop.run()
    def update_display(self):
        while True:
            line = 1
            urwid.connect_signal(self.edit,'change',str(line))
            time.sleep(1)
            line+=1
    def start_rs232(self):
##Add rs_232 module using threads. needs to communicate with this class
        return
    def setup_view(self):

        self.edit = urwid.Edit('')
        self.dataline = urwid.AttrWrap(urwid.Text('DADOS\nHere'),'body')
        text2 = urwid.AttrWrap(urwid.Text('Second Text\nHere'),'body')

        l = [self.dataline, urwid.Divider()]
        urwid.connect_signal(self.edit, 'change', self.update_text)
        l = urwid.SimpleListWalker([self.dataline,urwid.Divider(),text2])
        box=urwid.ListBox(l)
        box=urwid.AttrWrap(box,'body')
#        box=urwid.BoxAdapter(box,7)
        header=urwid.Text('DADOS. Press F8 to exit')
#        w=urwid.AttrWrap(bt,'body')
        self.frame = urwid.Frame(header=header, body=box)

        exit = urwid.BigText(('exit','Quit?'), urwid.Thin6x6Font)
        exit = urwid.Overlay('exit',self.frame,'center',None,'middle',None)
        return self.frame, exit

    def update_text(self,widget,line):
        self.dataline.set_text(line)

    def unhandled_input(self, key):
        if key == 'f8':
            self.loop.widget = self.exit_view
            return True
        if self.loop.widget != self.exit_view:
            return
        if key in ('y', 'Y'):
            raise urwid.ExitMainLoop()
        if key in ('n', 'N'):
            self.loop.widget = self.view
            return True
def main():
    MainDisplay().main()

if '__main__'==__name__:
    main()

#Source: https://github.com/urwid/urwid/blob/master/examples/bigtext.py
