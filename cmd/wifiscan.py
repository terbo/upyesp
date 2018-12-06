def wifiscan(pr=True):
  #from json import dumps
  from network import WLAN, STA_IF

  sta = WLAN(STA_IF)
  del WLAN, STA_IF

  wifi_enc = {
          0: 'open',
          1: 'WEP',
          2: 'WPA-PSK',
          3: 'WPA2-PSK',
          4: 'WPA/WPA2-PSK',
  }

  out={}
  for i in sta.scan():
    ssid = str(i[0],'utf8')
    mac = ':'.join(['%02x' % x for x in i[1]])
    channel = i[2]
    rssi = i[3]
    enc = wifi_enc[i[4]]
    hidden = True if i[5] else False

    if pr:
      print('%-24s %-16s %8s dBm    Ch.%s/%s  %s' % ( ssid, mac, rssi, channel, enc, hidden) )
    else:
      pkt = { 'ssid': ssid, 'mac': mac, 'channel': channel, 'rssi': rssi, 'enc': enc, 'hidden': hidden }
      out[mac] = pkt

  if not pr: return out
