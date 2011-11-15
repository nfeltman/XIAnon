import xanonsocket
from Tkinter import *

def enable_anonymizer_event_handler():
    if anonymizer_enabled.get():
        xanonsocket.XEnableAnonymizer()
    else:
        xanonsocket.XDisableAnonymizer()


root = Tk()

w = Label(root, text="System Anonymization Settings")
w.pack()

anonymizer_enabled = IntVar()
c = Checkbutton(root, text="Enable anonymizer", variable=anonymizer_enabled, command=enable_anonymizer_event_handler)
c.pack()

# Set checkbox state based on ini file
print xanonsocket.XGetAnonymizerEnabled()
if xanonsocket.XGetAnonymizerEnabled() == 'True':
    print 'enabled'
    c.select()
else:
    print 'disabled'
    c.deselect()

root.mainloop()
