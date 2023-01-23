import clr
from threading import Event
import os


clr.AddReference("PyForm")
clr.AddReference("System.Windows.Forms")


from EulithaAlignment import Form1
from System.Threading import Thread, ThreadStart, ApartmentState, ParameterizedThreadStart
import System.Windows.Forms as WinForms


cognex_ready = Event()


def result_handler(sender, args):
    print("Result handler called")
    res = sender.GetResult()
    print(f"received {res.StatusTxt} X1:{res.X1} Y1:{res.Y1} X2:{res.X2} Y2:{res.Y2}")


def ready_to_work(sender, args):
    print("window ready handler called")
    cognex_ready.set()
    sender.RunCommand()

    
def app_thread(arg):
    print(f"app_thread started with {arg}")
    WinForms.Application.EnableVisualStyles()
    forms_win = Form1()
    forms_win.ResArrived += result_handler
    forms_win.HandleCreated += ready_to_work
    WinForms.Application.Run(forms_win)


def app_main():
    at = Thread(ParameterizedThreadStart(app_thread))
    at.SetApartmentState(ApartmentState.STA)
    at.Start("Text Thread Argument")
    cognex_ready.wait()
    print("wait for Cognex App ready finished")
    at.Join()

if __name__ == "__main__":
    app_main()
