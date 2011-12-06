import os, sys
import time
import fcntl
import xsocket
from xia_address import *


def getPartAfterProxy(dag, proxy_sid):
	sid_index = dag.find(proxy_sid)
	if(sid_index==-1)
		raise Exception('SID for proxy service was not found in address')
	envoy_line_end = find(sid_index,'\n')
	
	return 

def recv_with_timeout(sock, timeout=5):
    # Make socket non-blocking
    try:
        fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)
    except IOError:
        print "ERROR: envoy.py: recv_with_timeout: could not make socket nonblocking"
    
    # Receive data
    start_time = time.time()   # current time in seconds since the epoch
    received_data = False
    reply = '<html><head><title>XIA Error</title></head><body><p>&nbsp;</p><p>&nbsp;</p><p style="text-align: center; font-family: Tahoma, Geneva, sans-serif; font-size: xx-large; color: #666;">Sorry, something went wrong.</p><p>&nbsp;</p><p style="text-align: center; color: #999; font-family: Tahoma, Geneva, sans-serif;"><a href="mailto:xia-dev@cs.cmu.edu">Report a bug</a></p></body></html>'
    try:
        while (time.time() - start_time < timeout and not received_data):
            try:
	    	select.select([sock], [], [], 0.02)
                reply = xanonsocket.Xrecv(sock, 65521, 0)
                received_data = True
            except IOError:
                received_data = False
            except:
                print 'ERROR: xiaproxy.py: recv_with_timeout: error receiving data from socket'
    except (KeyboardInterrupt, SystemExit), e:
        xanonsocket.Xclose(sock)
        sys.exit()

    if (not received_data):
        print "Recieved nothing"
    	raise IOError

    return reply



def main():
	print 'starting proxy'
	# Configure XSocket
	xsocket.set_conf("xsockconf_python.ini", "envoy.py")
	xsocket.print_conf()
	while True:
		# listen for clients
		listen_sock = xsocket.Xsocket()
		if (listen_sock<0):
			print "error initializing listen socket"
			return
		envoy_dag = "RE %s %s %s" % (AD1, HID2, SID_ENVOY)# address of envoy
		xsocket.Xbind(listen_sock, envoy_dag)
		print "Envoy: bound to\n%s" % envoy_dag
		xsocket.Xaccept(listen_sock)
		print "request started"
		
		# read out data 
		full_dst = xsocket.Xrecv(listen_sock, 2000, 0)
		print "full destination is: "+full_dst
		
		end_server_addr = getPartAfterProxy(full_dst)
		request_payload = xsocket.Xrecv(listen_sock, 2000, 0)
		print "full destination is: "+full_dst
		print "end server address is: "+end_server_addr
		
		# I don't think we need this; if we don't call Xbind, an ephemeral
		# SID gets generated for us when we call Xconnect
		# get temporary forwarding ID
		#temp_forward_id = getrandSID() # TODO implement this function
		#print "temporary forwarding sid is: "+temp_forward_id
		#forward_dag = "DAG 0 1 - \n %s 2 - \n %s 2 - \n %s 3 - \n %s" % (AD0, IP0, HID0, temp_forward_id) # TODO
		
		# create the forwarding socket
		forward_sock = xsocket.Xsocket()
		if (forward_sock<0):
			print "error initializing forward socket"
			return
		
		# make request to server
		try:
			if()#content
				# xsocket.Xbind(sock, sdag);
				xsocket.XgetCID(forward_sock, end_server_addr, len(end_server_addr))
			else
				# xsocket.Xbind(forward_sock, forward_dag)
				xsocket.Xconnect(forward_sock, end_server_addr)   # TODO: once dagmanip is done, should just be end_server_addr
				xsocket.Xsend(forward_sock, request_payload, len(request_payload), 0)
		except:
			print 'ERROR: envoy.py:  error forwarding request to final destination'
			
		# wait for reply and close socket
		try:
			reply = xsocket.Xrecv(forward_sock, 2000, 0) #recv_with_timeout(forward_sock) 
			if (reply.find("span")<0):
				print "Potentially non-ASCII payload from SID (len %d) " % len(reply)
		except IOError:
			print "Unexpected error:", sys.exc_info()[0]
			xsocket.Xclose(forward_sock)
			xsocket.Xclose(listen_sock)
			return
		xsocket.Xclose(forward_sock)
		# forward response
		print 'Forwarding response:\n%s' % reply
		xsocket.Xsend(listen_sock,reply,len(reply),0)
		xsocket.Xclose(listen_sock)




if __name__ ==  '__main__':
	main()
