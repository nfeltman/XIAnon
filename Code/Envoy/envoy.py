def getPartAfterProxy(dag):
	return ""

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
		
		# get temporary forwarding ID
		temp_forward_id = getrandSID() # TODO implement this function
		print "temporary forwarding sid is: "+temp_forward_id
		forward_dag = "DAG 0 1 - \n %s 2 - \n %s 2 - \n %s 3 - \n %s" % (AD0, IP0, HID0, temp_forward_id) # TODO
		
		# create the forwarding socket
		forward_sock = xsocket.Xsocket()
		if (forward_sock<0):
			print "error initializing forward socket"
			return
		
		# make request to server
		try:
			xsocket.Xbind(forward_sock, forward_dag)
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