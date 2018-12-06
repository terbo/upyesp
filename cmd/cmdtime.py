def cmdtime(topic, msg):
  from cfg import ESPConfig
  cfg = ESPConfig()

  from util import date
  from utime import mktime
  from ure import compile,  match
  src = topic[1]
  try:
    newdate = msg[0:-6]
    assert compile(r"^[0-9,'() ]+$").match(newdate)
    
    newdate = eval(newdate)
    tz = msg[-5:]
    newdate = mktime(newdate)
  except Exception as e:
    print('Incorrect time msg from %s: "%s" -- %s' % (src, msg, e))
    return
      
  print("Net date: %s Our date: %s" % (date(newdate), date()))

  if src in cfg.timelords:
    # check timezones...
    if (newdate < time()) and (time() - newdate > cfg.MAX_TS_DRIFT):
      print('%s has incorrect time by %s seconds!' % (time() - newdate))
      return
    elif time() < newdate and (newdate - time() > cfg.MAX_TS_DRIFT):
      print('Clock is off by more than a minute, updating time') 
      
      cfg.timezone = tz
      from machine import RTC
      print('OLD: %s' % date())
      RTC.datetime((now))
      print('NEW: %s' % date())
      del RTC
  else:
    print("Net date: %s Our date: %s" % (date(newdate), date()))

  del mktime, compile, match
