import os
import xsocket
import ConfigParser

conf_path = 'anonymization_configuration.ini'

def check_config():
    if not os.path.isfile(conf_path):
        with open(conf_path, 'w') as conf_file:
            conf_file.write('[Proxy]\nEnabled: False\nDAG:\n\n[TempServiceID]\nEnabled: False\nDuration: 60')
        conf_file.closed

def get_config():
    check_config()
    config = ConfigParser.ConfigParser()
    config.read(conf_path)
    return config

def save_config(config):
    with open(conf_path, 'w') as conf_file:
        config.write(conf_file)
    conf_file.closed




# Sets the dag for an anonymization service all outbound
# system traffic should use
def XSetAnonymizer(dag):
    config = get_config()
    config.set('Proxy', 'DAG', dag)
    save_config(config)

def XEnableAnonymizer():
    config = get_config()
    config.set('Proxy', 'Enabled', True)
    save_config(config)



# Wrappers around Xsocket API functions
def Xconnect(*args):
    config = get_config()
    if config.get('Proxy', 'Enabled'):
        proxy_dag = config.get('Proxy', 'DAG')
        sock = xsocket.Xconnect(args[0], proxy_dag)
        xsocket.Xsend(sock, args[1], len(args[1]), 0) # send actual dest dag to proxy
    else:
        sock = xsocket.Xconnect(args)
    return sock

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
