from cfg import ESPConfig
cfg = ESPConfig()

def update(s='', boot=0):
  errs = 0
  
  if not s:
    files = cfg.files.split(' ')
  else:
    if type(s) == str: files = [s]
    if type(s) == list: files = s
    else: return print("What did you send me?")

  from net import wget
  for f in files:
    try:
      print(f)
      wget(f)
    except Exception as e:
      errs += 1
      print(e)

  del wget

  if boot and not errs:
    print('Restarting...')
    from machine import reset
    reset()

def status(remote=False, evt=0):
  import net
  from esp import freemem
  from machine import freq as cpufreq
  import gc

  s_evts = ['auto','BOOTUP','REQUEST','RESPONSE','reconnect']
  m_reset = ['POWERON','WATCHDOG','CRASH?','BADCRASH?','DEEPSLEEP','DEEPSLEEP_RESET','HARD_RESET']
  m_cust  = ['reconnect'] # -1

  try:
    # but wha if u hav both up..
    if (not type(evt) == int) or (evt <= 0 or evt >= len(s_evts)): evt = 4
  except:
    print("WTF")
  
  ifc = net.sta.ifconfig()
  mem = str(freemem())
  cpufreq = str(cpufreq() / (10**6)) + 'Mhz'
  mac = net.sta.config('mac')

  stats = {'host': cfg.hostname,
           'up': uptime(),
           'cpufreq': cpufreq,
           'mem': mem,
           'mem_alloc': gc.mem_alloc(),
           'mem_free': gc.mem_free(),
           'gc': gc.isenabled(),
           'ip': ifc[0],
           'mac': net.prmac(mac),
           'dns': ifc[3],
           'gw': ifc[2],
           'phy': net.phymode(),
           'essid': net.sta.config('essid'),
           'rssi': net.sta.status('rssi'),
           'event': s_evts[evt],
          }
  
  if evt == 1:
    from machine import reset_cause
    cause = reset_cause()
    
    if cause in m_reset:
      stats['RESET_CAUSE'] = '%d(%s)' % ( cause, m_reset[cause] )
    else:
      stats['RESET_CAUSE'] = cause
    del reset_cause

  if remote: # in [1,2]:
    if remote == 2: print(stats)
    try:
      from mqtt import pub
      pub('/sys/%s' % cfg.hostname, stats) # wow.
    except Exception as e: print('stats/mqtt: %s' % e)
    finally: del pub
    
  else:
    return(stats)

def date(ref=None):
  from utime import localtime, time
  if ref:
    assert type(ref) is tuple
    d = ref
  else:
    d = localtime(time())

  days = 'Sun Mon Tue Wen Thu Fri Sat'.split(' ')
  mos = 'Yo Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(' ')
  now = '%-3s %-3s %02d  %02d:%02d:%02d %4d%s' % \
    ( days[d[6]], mos[d[1]], d[2], d[3], d[4], d[5], d[0], ' ' + \
      str(cfg.timezone) if cfg.timezone else '')
  del time, localtime
  return now

def uptime():
  from utime import time
  up_s = time()
  secs = str(int(up_s % 60))
  mins = str(int(up_s /60 % 60))
  hrs = str(int(up_s / 60 / 60 % 24))
  days = str(int(up_s / 60 /60 / 24))   
  (t_d, t_h, t_m, t_s) = ('d', 'h', 'm', 's')

  if days in [0,'0','']: days = t_d = ''
  if hrs in [0,'0','']: hrs = t_h = ''
  if mins in [0,'0','']: mins = t_m = ''
  if secs in [0,'0','']: secs = t_s = ''
    
  return(days + t_d + hrs + t_h + mins + t_m + secs + t_s)

def pp(obj, depth=1):
  if type(obj) == dict:
    print("%s{" % ' ' * depth)
    for key in sorted(obj):
      if type(obj[key]) in [str,int,bytes]:
        print("%s '%s':  '%s'" % ( "\t" * depth, key, str(obj[key]) ))
      else:
        pp(obj[key], depth+1)
    print("%s}" % ' ' * depth)
