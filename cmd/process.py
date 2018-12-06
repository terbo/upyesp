def process(buf):
  from cfg import ESPConfig
  cfg = ESPConfig()

  (src,dst,cmd,args,msg,atexit) = ('','','','','','')
  
  try:
    topic = str(buf[0],'utf8').split('/')[1:]
    msg = str(buf[1],'utf8')
  except Exception as e:
    print('Error processing cmd from "%s": %s' % (buf, e))
    return

  # we can get the time and keep it accurate
  #   (and see how it drifts)
  # and we can also notice others clocks innacuracies

  if topic[0] == 'time':
    try:
      from cmd.cmdtime import cmdtime
      cmdtime(topic, msg)
    except Exception as e:
      from sys import print_exception as prexc
      prexc(e)
      del prexc
    finally:
      del cmdtime
  elif topic[0] == cfg.mqtt_root:
    if topic[1].upper() == 'ALL':
      dst = 'all'
      #print('/%s/ALL: %s - %s' % (cfg.mqtt_root, topic[2:], msg))
    elif topic[1] == cfg.uid:
      dst = 'direct'
      #print('/%s/%s: %s - %s' % (cfg.mqtt_root, cfg.uid, topic[2:], msg))
    else:
      return
    cmd = topic[2].lower()
    
    if len(topic) > 3:
      args = topic[3:]

    if cmd == 'status':
      from util import status
      status(2)
      del status
    elif cmd == 'peers':
      print('Asked for a peerlist')
      from mqtt import pub
      pub('/sys/%s/peers' % cfg.uid, cfg.peers)
      del pub
    elif cmd == 'ping':
      print('Got PING')
      if src == cfg.hostname:return
      from mqtt import peerpong
      peerpong()
      del peerpong
    elif cmd == 'pong':
      from json import loads
      from utime import localtime
      rep = loads(msg)
      if rep['hostname'] in list(cfg.peers.keys()):
        print('Got PONG')
        cfg.peers[rep['hostname']]['lastseen'] = localtime()
        cfg.peers[rep['hostname']]['rssi'].append(rep['rssi'])
      elif rep['hostname'] != cfg.hostname:
        print('Adding new peer: %s' % rep['hostname'])
        from mqtt import pub
        pub('/sys/%s/peer/%s' % ( cfg.uid, rep['uid']), [rep['hostname'], rep['version']])
        rssi = rep['rssi']
        del rep['rssi']
        rep.update({'rssi': [rssi], 'firstseen': localtime(), 'lastseen': localtime()})
        cfg.peers[rep['hostname']] =  rep
      del loads
    elif cmd == 'update':
      print('Updating: ', end='')
      try:
        if not msg and args != 'all':
          print('derp, bad args')
          return

        if(msg == 'all' or args == 'all'):
          args = cfg.__all__
          atexit = 'reset'
        elif args == 'reset':
          atexit = 'reset'
        else:
          args = msg.split(' ')

        print(' %s\n' % args)
        
        from net import wget
        for f in args:
          try:
            print('%-6s>>  %10s\r' % ('.....', f), end='')
            wget(f)
          except Exception as e: print('WGET %s: %s' % (f, e))
          finally: del wget
      except Exception as e:
        print('UPDATE: %s' % e)
    elif cmd == 'reset':
      print('Got RESET')
      atexit = 'reset'
    elif cmd == 'cfg':
      print('Asked for config')
      from mqtt import pub
      pub('/sys/%s/config' % cfg.uid, {x:eval('cfg.%s'%x)} for x in dir(cfg))

    elif cmd == 'wifiscan':
      print('Performing Wireless Scan')
      from mqtt import pub
      from cmd.wifiscan import wifiscan
      pub('/sys/%s/wifiscan' % cfg.uid, wifiscan(0))
      del wifiscan, pub

  if atexit == 'reset':
    print('Resetting per MQTT request')
    from utime import sleep
    from machine import reset
    sleep(1)
    machine.reset()
