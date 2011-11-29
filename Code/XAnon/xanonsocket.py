import os
import xsocket
import ConfigParser
import pickle
import tkMessageBox

conf_path = 'anonymization_configuration.dat'
#conf_path = 'anonymization_configuration.ini'

#def check_config():
#    if not os.path.isfile(conf_path):
#        with open(conf_path, 'w') as conf_file:
#            conf_file.write('[Proxy]\nEnabled: False\nDAG:\nExceptions:\n\n[TempServiceID]\nEnabled: False\nDuration: 60')
#        conf_file.closed
#
#def get_config():
#    check_config()
#    config = ConfigParser.ConfigParser()
#    config.read(conf_path)
#    return config
#
#def save_config(config):
#    with open(conf_path, 'w') as conf_file:
#        config.write(conf_file)
#    conf_file.closed

def get_config():
    if os.path.isfile(conf_path):
        with open(conf_path, 'r') as conf_file:
            config = pickle.load(conf_file)
        conf_file.closed
    else:
        config = dict()
        # Add defaults
        config['proxy'] = dict()
        config['proxy']['enabled'] = False
        config['proxy']['dag'] = 'RE AD:1000000000000000000000000000000000000001 HID:0000000000000000000000000000000000000002 SID:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        config['proxy']['exceptions'] = ['Test app 1', 'Test app 2']  # TODO: remove test apps
        config['temp_ids'] = dict()
        config['temp_ids']['enabled'] = False
        config['temp_ids']['duration'] = 60
        config['principal_filter'] = dict()
        config['principal_filter']['allow_sids'] = True
        config['principal_filter']['allow_cids'] = True
        config['principal_filter']['action'] = 'alert'
    return config

def save_config(config):
    with open(conf_path, 'w') as conf_file:
        pickle.dump(config, conf_file)
    conf_file.closed



# Anonymization settings getters and setters
def XSetAnonymizer(dag):
    config = get_config()
    config['proxy']['dag'] = dag
    save_config(config)

def XGetAnonymizer():
    config = get_config()
    return config['proxy']['dag']

def XEnableAnonymizer():
    config = get_config()
    config['proxy']['enabled'] = True
    save_config(config)

def XDisableAnonymizer():
    config = get_config()
    config['proxy']['enabled'] = False
    save_config(config)

def XGetAnonymizerEnabled():
    config = get_config()
    return config['proxy']['enabled']

def XGetAnonymizerExceptions():
    config = get_config()
    return config['proxy']['exceptions']

def XAddAnonymizerException(application):
    config = get_config()
    config['proxy']['exceptions'].append(application)
    save_config(config)

def XRemoveAnonymizerException(application):
    config = get_config()
    if type(application) is int:
        application = config['proxy']['exceptions'][application]
    config['proxy']['exceptions'].remove(application)
    save_config(config)

def XEnableTempSIDs():
    config = get_config()
    config['temp_ids']['enabled'] = True
    save_config(config)

def XDisableTempSIDs():
    config = get_config()
    config['temp_ids']['enabled'] = False
    save_config(config)

def XGetTempSIDsEnabled():
    config = get_config()
    return config['temp_ids']['enabled']

def XSetTempSIDDuration(duration):
    config = get_config()
    config['temp_ids']['duration'] = duration
    save_config(config)

def XGetTempSIDDuration():
    config = get_config()
    return config['temp_ids']['duration']

def XEnableSIDs():
    config = get_config()
    config['principal_filter']['allow_sids'] = True
    save_config(config)

def XDisableSIDs():
    config = get_config()
    config['principal_filter']['allow_sids'] = False
    save_config(config)

def XGetSIDsEnabled():
    config = get_config()
    return config['principal_filter']['allow_sids']

def XEnableCIDs():
    config = get_config()
    config['principal_filter']['allow_cids'] = True
    save_config(config)

def XDisableCIDs():
    config = get_config()
    config['principal_filter']['allow_cids'] = False
    save_config(config)

def XGetCIDsEnabled():
    config = get_config()
    return config['principal_filter']['allow_cids']

def XSetDisallowedPrincipalAction(action):
    config = get_config()
    config['principal_filter']['action'] = action
    save_config(config)

def XGetDisallowedPrincipalAction():
    config = get_config()
    return config['principal_filter']['action']



# Wrappers around Xsocket API functions
def Xconnect(*args):
    if XGetAnonymizerEnabled():
        print 'Connecting via an anonymizer'
        proxy_dag = XGetAnonymizer()
        rv = xsocket.Xconnect(args[0], proxy_dag)
        try:
            print 'about to send real dag'
            xsocket.Xsend(args[0], args[1], len(args[1]), 0) # send actual dest dag to proxy  TODO: send proxy dag + dest dag
            print 'sent %s' % args[1]
        except:
            print 'sending dag failed'
    else:
        print 'Not connecting with anonymizer'
        rv = xsocket.Xconnect(args[0], args[1])
    return rv

def XconnectNoAnonymizer(application, *args):
    print 'checking if %s is an exception' % application
    if application in XGetAnonymizerExceptions():
        return xsocket.Xconnect(args[0], args[1])
    else:
        print '%s not in exceptions' % application
        if tkMessageBox.askyesno("Privacy Settings Control", "'%s' has requested to bypass system anonymization settings. Would you like to allow this?" % application):
            XAddAnonymizerException(application)
            XconnectNoAnonymizer(application, args[0], args[1])
        

Xsendto = xsocket.Xsendto
Xrecvfrom = xsocket.Xrecvfrom
Xsocket = xsocket.Xsocket
#Xconnect = xsocket.Xconnect
Xbind = xsocket.Xbind
Xclose = xsocket.Xclose
Xrecv = xsocket.Xrecv
Xsend = xsocket.Xsend
XgetCID = xsocket.XgetCID
XputCID = xsocket.XputCID
Xaccept = xsocket.Xaccept
set_conf = xsocket.set_conf
print_conf = xsocket.print_conf
