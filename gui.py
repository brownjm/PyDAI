#    PyDAI - Python Data Acquisition and Instrumentation
#
#    Copyright (C) 2011 Jeffrey M Brown, Greg A Cohoon, Kyle T Taylor
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from Tkinter import *
import traceback
from executable import Executable
from constants import EXIT, STATUS

class Launcher(object):
    def run(self):
        self.root = Tk()
        self.app = PyDAI_GUI(self.root)
        self.app.pack(expand='yes', fill='both')

        self.root.title("PyDAI - Python Data Acquisition and Instrumentation")
        self.root.protocol("WM_DELETE_WINDOW", closeCallback)
        self.root.mainloop()

class PyDAI_GUI(Frame, Executable):
    """Graphics interface to the PyDAI program"""
    def __init__(self, root):
        Frame.__init__(self)

        # menu
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=closeCallback)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)

        # frame
        self.textbox = Text(self, state="disabled")
        scrollbar = Scrollbar(self)
        self.entry = Entry(self)

        # packing
        self.entry.pack(side=BOTTOM, fill=X)
        self.textbox.pack(side=LEFT, fill=Y)
        scrollbar.pack(side=RIGHT, fill=Y)

        scrollbar["command"] = self.textbox.yview
        self.textbox["yscrollcommand"] = scrollbar.set
        self.entry.bind("<Up>", self.upkey)
        self.entry.bind("<Down>", self.downkey)
        self.entry.bind("<Return>", self.enterkey)
        self.entry.focus_set()
        
        # setting up control
        self.opWrap = OutputWrapper(self)
        sys.stdout = self.opWrap # redirect printing
        Executable.__init__(self)
        self.prompt = ">>> "
        self.writeCallback(self.getWelcome()+"\n")
    
    def upkey(self, Event=None):
        self.entry.delete(0, END)
        self.entry.insert(INSERT, self.env.prev())

    def downkey(self, Event=None):
        self.entry.delete(0, END)
        self.entry.insert(INSERT, self.env.next())

    def enterkey(self, Event=None):
        line = self.entry.get()
        self.entry.delete(0, END)
        print self.prompt + line
        try:
            if len(line) > 0:
                self.env.addToHistory(line)
                self.execute(line)
            if line == EXIT:
                closeCallback()

        except Exception as ex:
            print "Error Occured:"
            print traceback.format_exc()
        finally:
            self.histindex = -1
    
    def writeCallback(self, string):
        self.textbox.config(state=NORMAL)
        self.textbox.mark_set(INSERT, END)
        self.textbox.insert(INSERT, string)
        self.textbox.config(state=DISABLED)
        self.textbox.see(END)

    def send(self, packet):
        print packet[STATUS]

    def writePrompt(self):
        print self.prompt,

class OutputWrapper(object):
    def __init__(self, parent):
        self.parent = parent

    def write(self, string):
        self.parent.writeCallback(string)

if __name__ == "__main__":
    def closeCallback():
        sys.stdout = origstdobj
        launcher.root.destroy()

    origstdobj = sys.stdout

    launcher = Launcher()
    launcher.run()
