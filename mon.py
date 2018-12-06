import os, network, machine, time

ap_if = network.WLAN(network.AP_IF)
sta_if = network.WLAN(network.STA_IF)

sta_if.promiscuous_disable()
try:
  if sta_if.isconnected():
    sta_if.disconnect()
except:
  print("Unable to disconnect from sta")

ap_if.active(False)
del ap_if
sta_if.active(1)

out = None
channel = 1
timer = None
pkt = None
packets = 0

def disable():
  if timer:
   timer.deinit()
  sta_if.promiscuous_disable()
  global out
  ret = False
  if out is not None:
     #out.write("{},end\n".format(get_time()))
     out.close()
     out = None
     ret = True

  print("Promiscuous mode disabled")
  
  sta_if.active(1)
  sta_if.connect()

def prmac(mac):
  return ':'.join(['%02x' % x for x in mac])

def monitor_cb_one(buf):
  global sta_if, pkt, packets
  packets += 1
  sta_if.promiscuous_disable()
  pkt = {
    'fc': buf[0:1],
    'di': buf[2:3],
    'subtype': buf[0] & 0x000C,
    'ra': prmac(buf[4:10]),
    'ta': prmac(buf[16:22]),
    'dst': prmac(buf[23:29]),
    'src': prmac(buf[-6:]),
    'channel': channel,
#    'time': time.time() + 946733000,
    'seq': buf[30:31],
    'ssid': buf[50:50+int(buf[49])],
    'pkt': buf,
  } 

def monitor_cb(buf):
  global pkt, packets
  packets += 1
  pkt = {
    'fc': buf[0:1],
    'di': buf[2:3],
    'subtype': buf[0] & 0x000C,
    'ra': prmac(buf[4:10]),
    'ta': prmac(buf[16:22]),
    'dst': prmac(buf[23:29]),
    'src': prmac(buf[-6:]),
    'channel': channel,
    'time': time.time() + 946733000,
    'seq': buf[30:31],
    'ssid': buf[50:50+int(buf[49])],
    'pkt': buf,
  } 

def enable(output='log.txt', hop=True, hoptime=1000):
  global timer, out, sta_if
  #out = open('/log.pcap', 'a+')
  #out.write("{},begin\n".format(get_time()))
  sta_if.set_channel(1)
  sta_if.promiscuous_enable(monitor_cb)
  if hop:
    timer = machine.Timer(1)
    timer.init(period=hoptime, mode=machine.Timer.PERIODIC, callback=chanhop)

def one():
  sta_if.promiscuous_enable(monitor_cb_one)

def chanhop(*args, **kwargs):
  global channel, sta_if
  try:
    newchan = sta_if.set_channel(channel)
    if channel >= 11: channel = 0
    channel+=1
    #if not channel % 3:
    #  print('%s\r' % newchan, end='')
  except:
    pass

print("Monitor mode scripts loaded")
