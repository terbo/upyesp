import socket, network, uos, errno, io
LOGFILE=''
last_client_socket=None
server_socket=None
class TelnetWrapper(io.IOBase):
 def __init__(self,socket):
  self.socket=socket
  self.discard_count=0
 def readinto(self,b):
  readbytes=0
  for i in range(len(b)):
   try:
    byte=0
    while(byte==0):
     byte=self.socket.recv(1)[0]
     if byte==0xFF:
      self.discard_count=2
      byte=0
     elif self.discard_count>0:
      self.discard_count-=1
      byte=0
    b[i]=byte
    readbytes+=1
   except(IndexError,OSError)as e:
    if type(e)==IndexError or len(e.args)>0 and e.args[0]==errno.EAGAIN:
     if readbytes==0:
      return None
     else:
      return readbytes
    else:
     raise
  return readbytes
 def write(self,data):
  while len(data)>0:
   try:
    written_bytes=self.socket.write(data)
    data=data[written_bytes:]
   except OSError as e:
    if len(e.args)>0 and e.args[0]==errno.EAGAIN:
     pass
    else:
     raise
 def close(self):
  self.socket.close()
  try:log_connection(action=1)
  except:pass
def log_connection(remoteaddr='0.0.0.0', action=0):
  if not LOGFILE: return
  from time import localtime
  if action: action = 'logout'
  else: action = 'login'
  try:
    with open(LOGFILE,'a') as logfile:
      logfile.write('%s  %s  %s\n' % ( localtime(), action, remoteaddr ))
  except:pass
  del localtime
def accept_telnet_connect(telnet_server):
 global last_client_socket
 if last_client_socket:
  uos.dupterm(None)
  last_client_socket.close()
 last_client_socket,remote_addr=telnet_server.accept()
 #print("Telnet connection from:",remote_addr)
 log_connection(remote_addr)
 last_client_socket.setblocking(False)
 last_client_socket.setsockopt(socket.SOL_SOCKET,20,uos.dupterm_notify)
 last_client_socket.sendall(bytes([255,252,34]))
 last_client_socket.sendall(bytes([255,251,1]))
 uos.dupterm(TelnetWrapper(last_client_socket))
 from main import welcome
 welcome()
 del welcome
def stop():
 global server_socket,last_client_socket
 uos.dupterm(None)
 if server_socket:
  server_socket.close()
 if last_client_socket:
  last_client_socket.close()
def start(port=23, logfile='/etc/logfile'):
 global server_socket, LOGFILE
 LOGFILE=logfile
 stop()
 server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
 ai=socket.getaddrinfo("0.0.0.0",port)
 addr=ai[0][4]
 server_socket.bind(addr)
 server_socket.listen(1)
 server_socket.setsockopt(socket.SOL_SOCKET,20,accept_telnet_connect)
 for i in(network.AP_IF,network.STA_IF):
  wlan=network.WLAN(i)
  if wlan.active():
   print("Telnet server started on {}:{}".format(wlan.ifconfig()[0],port))
