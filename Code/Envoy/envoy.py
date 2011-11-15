import xsocket


def getPartAfterProxy(dag):
	return ""



def recv_with_timeout(sock, timeout=5):
    # Make socket non-blocking
    try:
        fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)
    except IOError:
        print "ERROR: xiaproxy.py: recv_with_timeout: could not make socket nonblocking"
    
    # Receive data
    start_time = time.time()   # current time in seconds since the epoch
    received_data = False
    reply = '<html><head><title>XIA Error</title></head><body><p>&nbsp;</p><p>&nbsp;</p><p style="text-align: center; font-family: Tahoma, Geneva, sans-serif; font-size: xx-large; color: #666;">Sorry, something went wrong.</p><p>&nbsp;</p><p style="text-align: center; color: #999; font-family: Tahoma, Geneva, sans-serif;"><a href="mailto:xia-dev@cs.cmu.edu">Report a bug</a></p></body></html>'
    try:
        while (time.time() - start_time < timeout and not received_data):
            try:
	    	select.select([sock], [], [], 0.02)
                reply = xsocket.Xrecv(sock, 65521, 0)
                received_data = True
            except IOError:
                received_data = False
            except:
                print 'ERROR: xiaproxy.py: recv_with_timeout: error receiving data from socket'
    except (KeyboardInterrupt, SystemExit), e:
        xsocket.Xclose(sock)
        sys.exit()

    if (not received_data):
        print "Recieved nothing"
    	raise IOError

    return reply


def main():
	print 'starting proxy'
	while True:
		# listen for clients
		listen_sock = xsocket.Xsocket()
		if (listen_sock<0):
			print "error initializing listen socket"
			return
		proxy_service_dag = "RE %s %s %s" # address of proxy service TODO 
		xsocket.Xbind(listen_sock, proxy_service_dag)
		print "bound connection"
		xsocket.Xaccept(listen_sock)
		print "request started"
		
		# read out data 
		full_dst = xsocket.Xrecv(listen_sock, 2000, 0)
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
			# xsocket.Xbind(forward_sock, forward_dag)
			xsocket.Xconnect(forward_sock, end_server_addr)
			xsocket.Xsend(forward_sock, request_payload, len(request_payload), 0)
		except:
			print 'ERROR: xiaproxy.py: sendSIDRequest: error binding to sdag, connecting to ddag, or sending SID request:\n%s' % request_payload
			
		# wait for reply and close socket
		try:
			reply = recv_with_timeout(forward_sock) # TODO
			if (reply.find("span")<0):
				print "Potentially non-ASCII payload from SID (len %d) " % len(reply)
		except IOError:
			print "Unexpected error:", sys.exc_info()[0]
			xsocket.Xclose(forward_sock)
			xsocket.Xclose(listen_sock)
			return
		xsocket.Xclose(forward_sock)
		# forward response
		xsocket.Xsend(listen_sock,reply,len(reply),0)
		xsocket.Xclose(listen_sock)




if __name__ ==  '__main__':
    main()
