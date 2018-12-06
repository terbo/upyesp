from cfg import ESPConfig
cfg = ESPConfig()

def add(name, secs, callback, once=1, repeat=0):
  from machine import Timer
  if repeat: mode = Timer.PERIODIC
  else:      mode = Timer.ONE_SHOT
  
  if name in cfg.timers:
    print('Trying to add a duplicate timer: %s' % name)
    return
 
  nexttimer = len(list(cfg.timers.keys()))
  
  try:
    cfg.timers[name] = {'type': mode, 'interval': int(secs),
                        'callback': callback,
                        'timer': Timer(nexttimer) }

    cfg.timers[name]['timer'].init(period=int(secs)*1000, mode=mode, callback=eval(callback))
  except Exception as e:
    print('add %s: %s' % (name, e))

  del Timer

def rm(name):
  try:
    cfg.timers[name]['timer'].deinit()
    if name in cfg.timers: del cfg.timers[name]
  except Exception as e:
    print('Deltimer %s: %s' % (name, e))

def timers(json=0):
  timers = list(cfg.timers.keys())
  if json:
    out = [ cfg.timers[x] for x in timers ]
    return out

  for timer in timers:
    t = cfg.timers[timer]
    print('Timer %-15s: "%-15s" @%-2ds interval, repeats: %s   (%s)' % \
      ( timer, t['callback'], t['interval'], 'True' if t['type'] else 'False', t['timer']))
