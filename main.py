import esp, uos, machine
import sys, gc, network
import utime

os = uos
time = utime
fn = sys.modules
reset = machine.reset
prexc = sys.print_exception

try: del bdev, fn['flashbdev']
except: pass

from cfg import ESPConfig
cfg = ESPConfig()

if cfg.caps['uart']:
  uos.dupterm(machine.UART(0, 115200), 1)
else:
  uos.dupterm(None,0)
  uos.dupterm(None,1)

ap = network.WLAN(network.AP_IF)
if cfg.caps['wifi_ap']:
  ap.active(1)
else:
  ap.active(0)
  del ap

sta = network.WLAN(network.STA_IF)
if cfg.caps['wifi_sta']:
  sta.active(1)
else:
  sta.active(0)

if cfg.caps['webrepl']:
  import webrepl
  webrepl.start()

try:
  from net import ifconfig
  from fs import ls, cat, head #, read, write
  from util import uptime, date, pp, status #  pp, update, status
  #from wget import wget
  #import mon
except Exception as e:
  prexc(e)

if cfg.caps['mqtt']:
  import mqtt
  try: timer.add('mqtt_init', cfg.mqtt_start_delay, 'mqtt.init')
  except Exception as e: prexec(e)
  try: timer.add('status',cfg.status_delay, 'status', repeat=1)
  except Exception as e: prexec(e)

def welcome():
  pre = '|\t  '
  print('\n'*2)
  print(' ',end='')
  print('.-v-' * 19)
  print('/'+pre)
  print('\\'+pre,end='')
  print('Welcome to %s %s @ %s.%s' % (cfg.package, cfg.version, cfg.hostname, cfg.domainname))
  print('/'+pre)
  print('\\'+pre)
  print('{'+pre,end='')
  print('MicroPython %s (Python %s) on the %s platform' % \
    ('.'.join(map(str,sys.implementation.version)), sys.version, sys.platform))
  print('/'+pre,end='')
  print('    (%s)' % uos.uname().version)
  print('\\'+pre)
  print('/'+pre,end='')
  try: print('Local time is %s, enjoy.' % date())
  except: pass
  print('\\'+pre)
  print('/'+pre,end='')
  print(' ' * 53, '~~`')
  print('\\'+pre)
  print('/'+pre,end='')
  print('   ... there is but only one way to death - through life.')
  print('\\'+pre)
  print('+',',..,,' * 15)
  print('')
  print('')
  print('Loaded modules: %s' % ', '.join(sorted(list(sys.modules.keys()))))

if cfg.caps['telnet']:
  import telnet
  telnet.start(cfg.telnetport)

try: import boot_local
except: pass

gc.collect()
