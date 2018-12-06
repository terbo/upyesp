__version__ = (0,1,9)
__package__ = 'upygsm'

from machine import Pin, UART
from utime import sleep_ms
from .commands import *
uart = None

def open_uart(ipin=0, opin=1, baud=57600):
  global uart
  try:
    Pin(ipin, Pin.IN)
    Pin(opin, Pin.OUT)
    uart = UART(ipin, baudrate=baud, timeout=5, timeout_char=5)
    setup()
    sleep_ms(100)
    null = uart.read(256)
    del null
  except Exception as e:
    from sys import print_exception
    print_exception(e)
  finally: return uart
def setup():
  global uart
  uart.write('ATE0\n')
  cmd('ringer',99)
  cmd('micgain',10)
  cmd('callerid',1)
  cmd('ringtone','3,0')
  cmd('smstype',1)
  cmd('localts',1)
  cmd('sleep',0)
def read(): return uart.read()
def write(s): return uart.write(s)
def cmd(action, wait=500, args=None):
  global uart
  if uart == None: open_uart()
  if action not in commands.keys():
    from util import pp
    print('Invalid command.')
    pp(commands)
    del pp
    return
  command = commands[action]
  #print("Executing %s [%s]" % ( command, action ) )
  # flush input
  while uart.any(): uart.read(1)
  uart.write('AT+%s%s\n' % (command, '=%s' % args if args else ''))
  sleep_ms(wait)
  uart.readline()
  buf = uart.readline()

  if not buf: return None
  return to_string(buf)
  
  '''
  while True:
    more = uart.any()
    if more:
      rep += uart.read(more)
      sleep_ms(100)
    else:
      break
  '''
def to_string(buf):
  try:
    tt =  buf.decode('utf-8').strip()
    return tt
  except UnicodeError:
    tmp = bytearray(buf)
    for i in range(len(tmp)):
      if tmp[i]>127:
        tmp[i] = ord('#')
    return bytes(tmp).decode('utf-8').strip()
def close(ipin=0, opin=1, baud=9600):
  global uart
  try:
    uart.deinit()
  except Exception as e:
    from sys import print_exception
    print_exception(e)
  finally:
    uart = None
