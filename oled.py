from cfg import ESPConfig
cfg = ESPConfig()

import machine, ssd1306, utime
from util import date, uptime

led = None
i2c = ''
addrs = 0

cy = 0   # current line

CW = 8    # character width/height
CH = 9

m_x = 128 # max pixels
m_y = 64

def init(SCREEN=0):
  global i2c, addrs, led, cy
  i2c = machine.I2C(-1, machine.Pin(cfg.SDA_PIN), machine.Pin(cfg.SDL_PIN))

  addrs = i2c.scan()

  if not len(addrs):
    return
    
  led = ssd1306.SSD1306_I2C(m_x, m_y, i2c, addrs[SCREEN])

  clear(1)
  led.invert(1)
  utime.sleep_ms(100)
  clear(0)

  now = date()
  oprint('%s %s' % ( cfg.package, cfg.version ))
  oprint('Host: %s' % ( cfg.hostname ), 0, CH)
  oprint('Date: %s' %  now[:10], 0, CH*2)
  oprint('%s'       % now[12:], 2, CH*3)
  oprint('Uptime: %s' % uptime(), 0, CH*4)

  cy = CH * 5

  led.invert(0)

def clear(clr=0):
  global led, cy
  led.fill(clr)
  cy = 0
  led.show()

def clearline(line, start=0, color=0):
  global m_y, CH
  led.fill_rect(start, line, m_x, CH, color)

def oprint(line, to_x=0, to_y=0):
  global led
  led.text(line, to_x, to_y)
  led.show()

def lprint(text, margin=0):
  global cy, m_x, m_y, CH, CW
  #print('cy: %x' % cy)

  if cy + CH >= m_y - CH:
    led.scroll(0, -(CH))
    cy = m_y - CH - 2
  else:
    cy += CH
  
  #print('cy: %x' % cy)

  oprint(text, 0, cy)

init()
