from cfg import ESPConfig
cfg = ESPConfig()

from network import WLAN, STA_IF
sta = WLAN(STA_IF)

del WLAN, STA_IF

from socket import socket, getaddrinfo

'''
if not sta.isconnected():
  print('Guess I\'ll try to connect again...')
  print(sta.ifconfig())
  sta.config(essid=cfg.wifi_ap, password=cfg.wifi_psk, dhcp_hostname=cfg.hostname)
  sta.connect()
'''

def prmac(mac): return ':'.join(['%02x' % x for x in mac])
def phymode():
  from network import phy_mode
  return [0,'11B','11G','11N'][ phy_mode() ]

def wget(f, out=None, host=None, port=None):
  import os

  if not host: host = '1.0.0.1'
  if not port: port = 80
  if not out: out = '%s/%s.py-tmp' % (os.getcwd(), f.rsplit('/',1)[-1])
  tmpfile = '/%s.tmp' % f.rsplit('/',1)[-1]
  (totalbytes, readbytes) = (0,0)

  try:
    sock = socket()
    addr = getaddrinfo(host, port)[0][-1]
    sock.connect(addr) # todo, add webroot
    sock.write('GET %s/%s.py HTTP/1.0\r\n\r\n' % ( cfg.webroot, f) )
    res = str(sock.readline(), 'utf8').split(' ')[1]
    if res.startswith('40'): raise OSError(-1)
  except Exception as e:
    print('CONNECT http://%s:%s%s/%s.py -- %s' % (host, cfg.webroot, port, f, e))
    return -1

  with open(tmpfile,'w+') as fp:
    while 1:
      try:
        s = sock.recv(cfg.RECV_SIZE)
        if not s: break
        readbytes += fp.write(s)
        print('%04d <\r' % readbytes, end='')
      except Exception as e:
        print('OPEN %s: %s' % (tmpfile, e))
        continue
  sock.close()
  print('')
  h=0
  
  with open(out,'w+') as nfp, open(tmpfile, 'r+') as fp:
    try:
      hs = 0
      while 1:
        if h: line = fp.read(cfg.RECV_SIZE)
        else: line = fp.readline()
        
        hs += len(line)
        if not line: break
        if h:
          print('%04d >\r' % totalbytes, end='')
          nfp.write(line) 
      
        if line == '\r\n': h=1
    except Exception as e: print(e)
  print('%04d >\n' % hs)
  
  try:
    os.rename(out,out.replace('-tmp',''))
  except Exception as e:
    print('Renaming "%s": %s' % (out, e))
  
  try: os.remove(tmpfile)
  except: pass


def ifconfig():
  netmasks = {
    '255.255.255.224': 27,
    '255.255.255.192': 26,
    '255.255.255.128': 25,
    '255.255.255.0': 24,
  }

  (ifcfg, essid, rssi, mac) = (sta.ifconfig(), sta.config('essid'),
                               sta.status('rssi'), sta.config('mac'))
  print("%s: " % cfg.hostname)
  if sta.active() and sta.isconnected(): print('\t802.%s  BSSID: "%s"  RSSI: %s dBm' % ( phymode(), essid, rssi))
  try:print('\tIP: %s/%d  MAC: %s  DNS: %s  GW: %s\n' % (ifcfg[0], netmasks[ifcfg[1]], prmac(mac), ifcfg[3], ifcfg[2]))
  except:pass
def startweb(*args, **kwargs):
  try:
    from webrepl import start
    start() #password='none'
  except Exception as e:
    print(e)
    print('WHY WONT WEBREPL START')
  finally:
    try:
      cfg.timers['webrepl']['timer'].deinit()
      del cfg.timers['webrepl'], start
    except: pass

def stop():
  from timer import rm
  for timer in cfg.timers:
    rm(timer)
  from mqtt import disconnect
  disconnect()

  print("Stopped all timers and network connections.")
