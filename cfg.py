__version__ = (0,2,5)
__package__ = 'upyesp'

from machine import unique_id
from sys import print_exception as prexc

class ESPConfig():
  def __init__(self, filename='/etc/esp.json'):
    self.version    = __version__
    self.package    = __package__
    self.filename   = filename
    self.module     = self.__class__.__name__
    self.boottime   = 0
    self.espmodel   = ''
    self.uid        = ':'.join(['%02x' % x for x in unique_id()]).split(':')
    self.uid        = ''.join([self.uid[1],self.uid[0]])
    self.hostname   = 'esp%s-%s' % (self.espmodel, self.uid)
    self.domainname = ''
    self.json = {}
    self.keepbackups = 3
    self.load()
  def load_defaults(self):
    self.json = {
      'caps': {'wifi_ap': 0, 'wifi_sta': 1, 'wlan_mon': 0, # wireless
               'mqtt': 0, 'telnet': 1, 'webrepl': 1,       # services
               'led': 0, 'lcd': 0, 'gsm': 0, 'bt': 0,      # periphials
               'eth': 0, 'uart': 1, 'sd': 0,
               'autostart': 1, },                          # autoload?
      'files': 'boot cfg fs mqtt oled net util timer telnet lib/gsm/__init__ lib/gsm/commands lib/cmd/process lib/cmd/untar lib/cmd/env lib/cmd/lsr lib/cmd/wifiscan',
      'timezone': '-0800',
      'wifi_ap': 'default',
      'wifi_psk': 'password',
      'status_delay': 300,
      'telnetport': 2323,
      'webroot': '',
      'ntpdelta': 3155673600,
      'ntphost': 'tick.ucla.edu',
      'timelords': ['ntp','time'],
      
      'mqtt_root': 'esp',
      'mqtt_topics': ['/FIXME'],
      'mqttport': 1883,
      'mqtthost': '0.0.0.0',
      'mqtt_keepalive': 10,
      'mqtt_start_delay': 7,
      'mqtt_check_delay': 10,

      'timers': {},
      'peers': {},

      'DEBUG': 1,
      'RECV_SIZE': 256,
      'MAX_TS_DRIFT': 60,
      'SDL_PIN': 0,
      'SDL_PIN': 2,
    }
  def __del__(self):
    self.save()
  def __dir__(self):
    return dir(ESPConfig)
  def keys(self):
    return sorted(self.json.keys())
  def values(self):
    return self.json.values()
  def __str__(self):
    return '%s/%s v.%s' % (self.package, self.module, '.'.join([str(x) for x in map(int,self.version)]))
  def __getitem__(self,key):
    return self.json[key]
  def __setitem__(self,key, val):
    self.json[key] = val
  def __getattr__(self,key):
    return self.json[key]
  def __setattr__(self, key, val):
    self.json[key] = val
  def load(self):
    try:
      from ujson import loads
      from uos import stat, mkdir
      try: stat('/etc')
      except Exception as e:
        if e.args[0] == 2:
          mkdir('/etc')
        else: raise
      finally:
        try: del stat, mkdir
        except: pass
      with open(self.filename) as fp:
        self.json = loads(''.join(fp.readlines()))
    except Exception as e:
      prexc(e)
      self.load_defaults()
    finally:
      try: del loads
      except: pass
  def save(self):
    from ujson import dumps
    try:
      self.backup()
      with open(self.filename,'w+') as fp:
        ret = fp.write(dumps(self.json))
    except Exception as e:
      prexc(e)
    finally:
      try: del dumps
      except: pass
  def backup(self):
    pass
