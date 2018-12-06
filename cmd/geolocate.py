import sys
def geolocate(apikey, useIP=1, getimage=1, imgsize='320x240', zoom=15):
  if sys.platform.startswith('esp'):
    import ujson as json, urequests as requests
    from cmd import wifiscan
    scan = wifiscan(0)
    data = {"considerIp": useIP, "wifiAccessPoints": []}
    for key in scan.keys():
      data['wifiAccessPoints'].append({"macAddress": key,
                                       "signalStrength": scan[key]['rssi'],
                                       "channel": scan[key]['channel']})
  else:
    import json, requests, subprocess
    data = eval(subprocess.check_output(['iwscan','-j']))

  headers = {"Content-Type": "application/json"}
  url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + apikey

  response = requests.post(url, headers=headers, data=json.dumps(data))
  location = json.loads(response.content)["location"]

  if(getimage):
    query = {
        "center": "%.8f,%.8f" % (location["lat"], location["lng"]),
        "markers": "%.8f,%.8f" % (location["lat"], location["lng"]),
        "size": imgsize,
        "zoom": zoom,
        "format": "jpg-baseline"
    }

    query_string = "&".join("%s=%s" % (key, value) for key, value in query.items())

    url = "https://maps.googleapis.com/maps/api/staticmap?key=%s&%s" % (apikey, query_string)

    image = requests.get(url)

    fp = open("map.jpg", "wb")
    fp.write(image.content)
    fp.close()
