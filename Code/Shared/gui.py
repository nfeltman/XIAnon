#! /usr/bin/python

import xanonsocket
from Tkinter import *
from tkFont import *


# ***** GLOBAL STUFF ***** #
change_service_window = None
change_service_name = None
change_service_address = None
add_exception_window = None
add_exception_name = None



# ***** EVENT HANDLERS ***** #

def enable_anonymizer_event_handler():
    if anonymizer_enabled.get():
        xanonsocket.XEnableAnonymizer()
    else:
        xanonsocket.XDisableAnonymizer()

def btn_change_service_click():
    global change_service_window, change_service_name, change_service_address
    change_service_window = Toplevel()
    change_service_window.title("Change Anonymization Service")
    Label(change_service_window, text="Specify the name and address of an anonymization service\nbelow, or choose 'Default' to use the default anonymizer.", justify=LEFT).grid(row=0, padx=10, pady=10, sticky=W)
    
    frame_info = Frame(change_service_window)
    frame_info.grid(row=1, padx=10, pady=(0,10), sticky=W+E)
    Label(frame_info, text="Name: ").grid(row=1, column=0, sticky=E)
    change_service_name = StringVar()
    change_service_name.set("Envoy")
    Entry(frame_info, width=10, textvariable=change_service_name).grid(row=1, column=1, sticky=W)
    Label(frame_info, text="Address: ").grid(row=2, column=0, sticky=E)
    change_service_address = StringVar()
    change_service_address.set(xanonsocket.XGetAnonymizer())
    Entry(frame_info, width=40, textvariable=change_service_address).grid(row=2, column=1, sticky=W)

    frame_buttons = Frame(change_service_window)
    frame_buttons.grid(row=2, padx=10, pady=(20,10), sticky=W+E)
    frame_buttons.columnconfigure(0, weight=1)
    Button(frame_buttons, text="Default", command=btn_default_click).grid(row=0, column=0, sticky=W)
    Button(frame_buttons, text="Save", command=btn_save_click).grid(row=0, column=1, sticky=E)

def btn_default_click():
    global change_service_window, change_service_name, change_service_address
    change_service_name.set("Envoy")
    change_service_address.set("RE AD:1000000000000000000000000000000000000001 HID:0000000000000000000000000000000000000002 SID:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

def btn_save_click():
    global change_service_window, change_service_name, change_service_address
    xanonsocket.XSetAnonymizer(change_service_address.get())
    change_service_window.destroy()

def cbx_use_temp_sids_changed():
    if use_temp_sids.get():
        xanonsocket.XEnableTempSIDs()
    else:
        xanonsocket.XDisableTempSIDs()

def load_app_exceptions_listbox():
    lbx_exceptions.delete(0, END)
    for app in xanonsocket.XGetAnonymizerExceptions():
        lbx_exceptions.insert(END, app)

def btn_remove_exception_click():
    indices = lbx_exceptions.curselection()
    try:
        indices = map(int, indices)
    except:
        pass
    for index in indices:
        xanonsocket.XRemoveAnonymizerException(index)
    load_app_exceptions_listbox()

def btn_add_exception_click():
    global add_exception_window, add_exception_name
    add_exception_window = Toplevel()
    add_exception_window.title("Add Exception")
    Label(add_exception_window, text="To allow an application to bypass this anonymizer, enter \nits name and click 'Add'.", justify=LEFT).grid(row=0, padx=10, pady=10, sticky=W)

    add_exception_name = StringVar()
    Entry(add_exception_window, textvariable = add_exception_name).grid(row=1, padx=10, sticky=W+E)

    frame_buttons = Frame(add_exception_window)
    frame_buttons.grid(row=2, padx=10, pady=10, sticky=E)
    Button(frame_buttons, text="Cancel", command=add_exception_window.destroy).grid(row=0, column=0, sticky=E)
    Button(frame_buttons, text="Add", command=btn_add_click).grid(row=0, column=1, sticky=E)

def btn_add_click():
    global add_exception_window, add_exception_name
    xanonsocket.XAddAnonymizerException(add_exception_name.get())
    load_app_exceptions_listbox()
    add_exception_window.destroy()

def duration_validate_and_save():
    try:
        seconds = int(duration.get())
    except ValueError:
        return False
    xanonsocket.XSetTempSIDDuration(seconds)
    return True

def cbx_allow_SIDs_changed():
    if allow_SIDs.get():
        xanonsocket.XEnableSIDs()
    else:
        xanonsocket.XDisableSIDs()

def cbx_allow_CIDs_changed():
    if allow_CIDs.get():
        xanonsocket.XEnableCIDs()
    else:
        xanonsocket.XDisableCIDs()

def rbtn_action_changed():
    xanonsocket.XSetDisallowedPrincipalAction(action.get())



# ***** Tk SETUP STUFF ***** #

root = Tk()
root.title("System Privacy Settings")
root.columnconfigure(0, weight=1)



# ***** ANONYMIZATION SERVICE SETTINGS ***** #

frame_anon_service = Frame(root)
frame_anon_service.grid(row=0, padx=10, pady=10, sticky=W+E)
#frame_anon_service.columnconfigure(0, weight=1)

lbl_anon_service = Label(frame_anon_service, text="Anonymization Service", font='TkHeadingFont')
lbl_anon_service.grid(row=0, sticky=W)

anonymizer_enabled = IntVar()
cbx_anonymizer_enabled = Checkbutton(frame_anon_service, text="Send outbound traffic through an anonymization service", variable=anonymizer_enabled, command=enable_anonymizer_event_handler)
cbx_anonymizer_enabled.grid(row=1, padx=(10,0), sticky=W)

frame_pick_service = Frame(frame_anon_service)
frame_pick_service.grid(row=2, padx=(33,0), sticky=W+E)
lbl_service_title = Label(frame_pick_service, text="Service: ")
lbl_service_title.grid(row=0, column=0, sticky=W)
lbl_service_name = Label(frame_pick_service, text="Envoy") #TODO: don't hardcode
lbl_service_name.grid(row=0, column=1, sticky=W)
btn_change_service = Button(frame_pick_service, text="Change Service...", command=btn_change_service_click) 
btn_change_service.grid(row=0, column=2)
frame_pick_service.columnconfigure(1, weight=1) # column 1 should absorb extra space

frame_exceptions = Frame(frame_anon_service)
frame_exceptions.grid(row=3, padx=(33,0), pady=(10,0), sticky=W+E)
lbl_exceptions_title = Label(frame_exceptions, text="Allow these applications to bypass the anonymization service:")
lbl_exceptions_title.grid(row=0, column=0, sticky=W)
scrollbar = Scrollbar(frame_exceptions, orient=VERTICAL)
lbx_exceptions = Listbox(frame_exceptions, yscrollcommand=scrollbar.set)
scrollbar.config(command=lbx_exceptions.yview)
lbx_exceptions.grid(row=1, column=0, sticky=W+E+N+S)
scrollbar.grid(row=1, column=1, sticky=N+S)
frame_exceptions.columnconfigure(0, weight=1)
frame_add_remove_exception = Frame(frame_exceptions)
frame_add_remove_exception.grid(row=2, columnspan=2, sticky=E)
btn_remove_exception = Button(frame_add_remove_exception, text="Remove", command=btn_remove_exception_click)
btn_remove_exception.grid(row=0, column=0, sticky=E)
btn_add_exception = Button(frame_add_remove_exception, text="Add", command=btn_add_exception_click)
btn_add_exception.grid(row=0, column=1, sticky=E)




# ***** TEMPORARY ID SETTINGS ***** #

frame_temp_ids = Frame(root)
frame_temp_ids.grid(row=1, padx=10, pady=10, sticky=W+E)
frame_temp_ids.columnconfigure(0, weight=1)

lbl_temp_ids = Label(frame_temp_ids, text="Temporary IDs", font='TkHeadingFont')
lbl_temp_ids.grid(row=0, sticky=W)

use_temp_sids = IntVar()
cbx_use_temp_sids = Checkbutton(frame_temp_ids, text="Use temporary service IDs instead of my HID", variable=use_temp_sids, command=cbx_use_temp_sids_changed)
cbx_use_temp_sids.grid(row=1, padx=(10,0), sticky=W)

frame_duration = Frame(frame_temp_ids)
frame_duration.grid(row=2, padx=(33,0), sticky=W+E)
lbl_duration1 = Label(frame_duration, text="Temporary IDs expire every ")
lbl_duration1.grid(row=0, column=0, sticky=W)
duration = StringVar()
tbx_duration = Entry(frame_duration, width=5, textvariable=duration, validate="focusout", validatecommand=duration_validate_and_save)
tbx_duration.grid(row=0, column=1, sticky=W)
lbl_duration2 = Label(frame_duration, text=" seconds")
lbl_duration2.grid(row=0, column=2, sticky=W)
btn_change_now = Button(frame_temp_ids, text="Change Now")
btn_change_now.grid(row=3, sticky=E)




# ***** PRINCIPAL TYPE FILTER SETTINGS ***** #

frame_principal_filter = Frame(root)
frame_principal_filter.grid(row=2, padx=10, pady=10, sticky=W+E)

lbl_filter_title = Label(frame_principal_filter, text="Traffic Type Filter", font='TkHeadingFont')
lbl_filter_title.grid(row=0, sticky=W)

lbl_allowed_types = Label(frame_principal_filter, text="Allow traffic using the following principal types:")
lbl_allowed_types.grid(row=1, padx=(10,0), sticky=W)

frame_types = Frame(frame_principal_filter)
frame_types.grid(row=2, padx=(33,0), sticky=W+E)
allow_SIDs = IntVar()
cbx_allow_sids = Checkbutton(frame_types, text="Services", variable=allow_SIDs, command=cbx_allow_SIDs_changed)
cbx_allow_sids.grid(row=0, column=0, sticky=W)
allow_CIDs = IntVar()
cbx_allow_cids = Checkbutton(frame_types, text="Content", variable=allow_CIDs, command=cbx_allow_CIDs_changed)
cbx_allow_cids.grid(row=0, column=1, sticky=W)

lbl_action = Label(frame_principal_filter, text="When an application attempts to use a disallowed principal\n type, take the following action:", justify=LEFT, anchor=W)
lbl_action.grid(row=3, padx=(10,0), pady=(10,0), sticky=W)

frame_actions = Frame(frame_principal_filter)
frame_actions.grid(row=4, padx=(33,0), sticky=W+E)
action = StringVar()
Radiobutton(frame_actions, text="Block the packet", variable=action, value="block", command=rbtn_action_changed).pack(anchor=W)
Radiobutton(frame_actions, text="Block the packet and alert me", variable=action, value="alert", command=rbtn_action_changed).pack(anchor=W)
Radiobutton(frame_actions, text="Ask me what to do", variable=action, value="ask", command=rbtn_action_changed).pack(anchor=W)




# Set GUI state based on config file
if xanonsocket.XGetAnonymizerEnabled():
    cbx_anonymizer_enabled.select()
else:
    cbx_anonymizer_enabled.deselect()

load_app_exceptions_listbox()

if xanonsocket.XGetTempSIDsEnabled():
    cbx_use_temp_sids.select()
else:
    cbx_use_temp_sids.deselect()

duration.set(xanonsocket.XGetTempSIDDuration())

if xanonsocket.XGetSIDsEnabled():
    cbx_allow_sids.select()
else:
    cbx_allow_sids.deselect()
if xanonsocket.XGetCIDsEnabled():
    cbx_allow_cids.select()
else:
    cbx_allow_cids.deselect()

action.set(xanonsocket.XGetDisallowedPrincipalAction())

root.mainloop()
