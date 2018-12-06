from sys import print_exception as prexc
def is_dir(f): return f & 0o170000 == 0o040000
def is_file(f): return f & 0o170000 == 0o100000
def head(f,num=5):
  try:
    fp = open(f)
    while 1:
      line = fp.readline()
      if not line or num <= 0: break
      print(line, end='')
      num -= 1
  except Exception as e:
    prexec(e)
  finally:
    fp.close()
  print('')
def cat(f):
  try:
    i = 0
    for line in open(f).readlines():
      print('%2d\t%s' % (i, line), end='')
      i+=1
  except Exception as e:
    prexc(e)
def write(f, txt, append=1):
  try:
    if append: mode = 'a+'
    else: mode = 'w+'
    fp = open(f,mode)
    print('%d of %d bytes written to %s' % (len(txt), fp.write(txt), f))
    fp.close()
  except Exception as e:
    prexc(e)
def read(f):
  try:
    with open(f,'r+') as fp:
      while 1:
        line = fp.read(256)
        if not line:
          break
        yield(line)
  except Exception as e:
    prexc(e)
def basename(f):
  return f.rsplit('/',1)[-1]
def ls(d=False):
  from uos import getcwd, ilistdir
  perms = 'rwx------+'
  if not d: d = getcwd()
  print('\n\t%s:' % d)
  if d.startswith('//'): d = d[1:]
  for f in sorted(ilistdir(d)):
    ft = '-'
    size = f[3]
    if is_dir(f[1]): print('%s%8s  %-8s %32s' % ('d', perms, size, f[0]))
    elif is_file(f[1]):
      if d.endswith('/'): d = d[0:-2]
      if d.startswith('/'): d = d[1:]
      if f[0].startswith('/'): f[0] = f[0][1:]
      if f[0].endswith('/'): f[0] = f[0][0:-2]
      print('%s%8s  %-8s %32s' % ('-', perms, size, f[0]))
  del getcwd, ilistdir
