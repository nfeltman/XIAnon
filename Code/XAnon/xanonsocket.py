import os
import xsocket
import ConfigParser
import pickle
import Tkinter
import tkMessageBox
import dagmanip


sock_status = {}   # TODO: Remove me; do this a better way?

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
        config['proxy']['dag'] = 'DAG 0 - \n AD:1000000000000000000000000000000000000002 1 - \n HID:0000000000000000000000000000000000000002 2 - \n SID:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        #config['proxy']['dag'] = 'RE AD:1000000000000000000000000000000000000002 HID:0000000000000000000000000000000000000002 SID:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        config['proxy']['exceptions'] = [] 
        config['temp_ids'] = dict()
        config['temp_ids']['enabled'] = False
        config['temp_ids']['duration'] = 60
        config['principal_filter'] = dict()
        config['principal_filter']['allow_sids'] = True
        config['principal_filter']['allow_cids'] = True
        config['principal_filter']['action'] = 'alert'
        config['statistics'] = dict()
        config['statistics']['system_anonymizer_count'] = 1234
        config['statistics']['no_anonymizer_count'] = 111
        config['statistics']['other_anonymizer_count'] = 257
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

def get_system_anonymizer_count():
    config = get_config()
    return config['statistics']['system_anonymizer_count']

def get_other_anonymizer_count():
    config = get_config()
    return config['statistics']['other_anonymizer_count']

def get_no_anonymizer_count():
    config = get_config()
    return config['statistics']['no_anonymizer_count']

def increment_anonymizer_type_count(anon_type):
    config = get_config()
    config['statistics'][anon_type] +=1
    save_config(config)
    

def should_proceed_check_disallowed_principals(dag):
    print 'checking DAG: %s' % dag
    disallowed_types_string = ''
    disallowed_types_used = False
    if not XGetSIDsEnabled() and 'SID:' in dag:
        print 'content!!!'
        disallowed_types_used = True
        disallowed_types_string += '\nService'
    if not XGetCIDsEnabled() and 'CID:' in dag:
        disallowed_types_used = True
        disallowed_types_string += '\nContent'
    if disallowed_types_used:
        print 'disallowed type!!!'
        action = XGetDisallowedPrincipalAction()
        if action == 'block':
            print 'block'
            return False
        elif action == 'alert':
            print 'alert'
            # TODO: should be less intrusive
            root = Tkinter.Tk()
            root.withdraw()
            tkMessageBox.showwarning("Privacy Settings Alert", "Outbound network traffic using the following disallowed princiapl types was blocked:\n%s" % disallowed_types_string)
            root.destroy()
            return False
        elif action == 'ask':
            print 'ask'
            root = Tkinter.Tk()
            root.withdraw()
            if tkMessageBox.askyesno("Privacy Settings Control", "Outbound network traffic is attempting to use the following disallowed princiapl types. Would you like to allow this?\n%s" % disallowed_types_string):
                root.destroy()
                return True
            else:
                root.destroy()
                return False
        else:
            print 'should_proceed_check_disallowed_principals(): Unrecognized action: %s' % action
    else:
        return True

def ask_user_for_exception(application):
    root = Tkinter.Tk()
    root.withdraw()
    if tkMessageBox.askyesno("Privacy Settings Control", "'%s' has requested to bypass system anonymization settings. Would you like to allow this?" % application):
        XAddAnonymizerException(application)
        root.destroy()
        return True
    else:
        root.destroy()
        return False

            




# Wrappers around Xsocket API functions
def Xconnect(*args):
    if not should_proceed_check_disallowed_principals(args[1]):
        return -2
    if XGetAnonymizerEnabled():
        proxy_dag = XGetAnonymizer()
        sock_status[args[0]] = 'system_anonymizer_count'
        print '***Connecting with anonymizer'
        rv = __XconnectWithAnonymizer(proxy_dag, args[0], args[1])
    else:
        rv = xsocket.Xconnect(args[0], args[1])
        sock_status[args[0]] = 'no_anonymizer_count'
    return rv

def __XconnectWithAnonymizer(proxy_dag, *args):
    print '***About to append dag'
    big_dag = dagmanip.parse_DAG(proxy_dag)
    dagmanip.append_dag(big_dag, dagmanip.parse_DAG(args[1]))
    big_dag_str = dagmanip.DAG_to_string(big_dag)
    print '*** Made DAG: %s' % big_dag_str
    rv = xsocket.Xconnect(args[0], proxy_dag)
    try:
        print 'Sending dag: %s' % big_dag_str
        xsocket.Xsend(args[0], big_dag_str, len(big_dag_str), 0) # send actual dest dag to proxy  TODO: send proxy dag + dest dag
    except:
        print 'sending dag failed'
    return rv
    

def XconnectWithAnonymizer(application, proxy_dag, *args):
    if application in XGetAnonymizerExceptions():
        if not should_proceed_check_disallowed_principals(args[1]):
            return -2
        sock_status[args[0]] = 'other_anonymizer_count'
        return __XconnectWithAnonymizer(proxy_dag, args[0], args[1])
    else:
        if ask_user_for_exception(application):
            return XconnectWithAnonymizer(application, proxy_dag, args[0], args[1])

def XconnectWithoutAnonymizer(application, *args):
    if application in XGetAnonymizerExceptions():
        if not should_proceed_check_disallowed_principals(args[1]):
            return -2
        sock_status[args[0]] = 'no_anonymizer_count'
        return xsocket.Xconnect(args[0], args[1])
    else:
        if ask_user_for_exception(application):
            return XconnectWithoutAnonymizer(application, args[0], args[1])

def Xsendto(*args):        
    if not should_proceed_check_disallowed_principals(args[4]):
        return -2
    increment_anonymizer_type_count(sock_status[args[0]])
    return xsocket.Xsendto(*args)

def Xsend(*args):
    increment_anonymizer_type_count(sock_status[args[0]])
    return xsocket.Xsend(*args)
                           
def XgetCID(*args):
    if not should_proceed_check_disallowed_principals(args[1]):
        return -2
    
    if XGetAnonymizerEnabled():
        proxy_dag = XGetAnonymizer()
        increment_anonymizer_type_count('system_anonymizer_count')
        rv = __XgetCIDWithAnonymizer(proxy_dag, *args)
    else:
        increment_anonymizer_type_count('no_anonymizer_count')
        rv = xsocket.XgetCID(*args)
    return rv

    return xsocket.XgetCID(*args)

def __XgetCIDWithAnonymizer(proxy_dag, *args):
    print '***About to append dag'
    big_dag = dagmanip.parse_DAG(proxy_dag)
    dagmanip.append_dag(big_dag, dagmanip.parse_DAG(args[1]))
    big_dag_str = dagmanip.DAG_to_string(big_dag)
    print '*** Made DAG: %s' % big_dag_str
    rv = xsocket.Xconnect(args[0], proxy_dag)
    try:
        xsocket.Xsend(args[0], big_dag_str, len(big_dag_str), 0) # send actual dest dag to proxy  TODO: send proxy dag + dest dag
        xsocket.Xsend(args[0], big_dag_str, len(big_dag_str), 0) # send actual dest dag to proxy  TODO: send proxy dag + dest dag
    except:
        print 'sending dag failed'
    return rv

def XgetCIDWithAnonymizer(application, proxy_dag, *args):
    if not should_proceed_check_disallowed_principals(args[1]):
        return -2
    
    if application in XGetAnonymizerExceptions():
        return __XgetCIDWithAnonymizer(proxy_dag, *args)
    else:
        if ask_user_for_exception(application):
            return XgetCIDWithAnonymizer(application, proxy_dag, *args)

def XgetCIDWithoutAnonymizer(application, *args):
    if not should_proceed_check_disallowed_principals(args[1]):
        return -2
    
    if application in XGetAnonymizerExceptions():
        increment_anonymizer_type_count('no_anonymizer_count')
        return xsocket.XgetCID(*args)
    else:
        if ask_user_for_exception(application):
            return XgetCIDWithoutAnonymizer(application, *args)

#Xsendto = xsocket.Xsendto
Xrecvfrom = xsocket.Xrecvfrom
Xsocket = xsocket.Xsocket
#Xconnect = xsocket.Xconnect
Xbind = xsocket.Xbind
Xclose = xsocket.Xclose
Xrecv = xsocket.Xrecv
#Xsend = xsocket.Xsend
#XgetCID = xsocket.XgetCID
XputCID = xsocket.XputCID
Xaccept = xsocket.Xaccept
set_conf = xsocket.set_conf
print_conf = xsocket.print_conf
