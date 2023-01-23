import clr
from threading import Event
import os

import sys
sys.path.append(r"C:\repos\PyForm\bin\Debug")


clr.AddReference("PyForm")
clr.AddReference("System.Windows.Forms")


from PyForm import Form1
from System.Threading import Thread, ThreadStart, ApartmentState, ParameterizedThreadStart
import System.Windows.Forms as WinForms


class FormsApplication:
    
    def __init__(self):
        self.cognex_ready = Event()
        self.at = Thread(ParameterizedThreadStart(self.app_thread))
        self.at.SetApartmentState(ApartmentState.STA)
        self.win_form = None
        self.at.Start(self)

    def result_handler(self, sender, args):
        print("Python result handler called")
        self.cognex_ready.set()

    def ready_to_work(self, sender, args):
        print("window ready handler called")
        self.win_form = sender
        self.cognex_ready.set()
        
    def work(self):
        self.cognex_ready.clear()
        self.win_form.run_cmd()

    def app_thread(self, arg):
        print(f"app_thread started with {arg}")
        WinForms.Application.EnableVisualStyles()
        forms_win = Form1()
        forms_win.Awake += self.result_handler
        forms_win.HandleCreated += self.ready_to_work
        WinForms.Application.Run(forms_win)

    def close(self):
        self.win_form.Close()
        WinForms.Application.ExitThread();  

    def join(self):
        self.at.Join()
    

if __name__ == "__main__":
    app = FormsApplication()
    print("app created")
    while True:
        app.cognex_ready.wait()
        print("app ready to work")
        user_txt = input("Enter text to send to form: ")
        print(f"Sending {user_txt} to form")
        if user_txt == "x":
            break
        else:
            app.work()
    app.close()
    app.join()