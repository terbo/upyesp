def ls(d=False,r=False,o=True):
  from os import getcwd, ilistdir
  (total, files, dirs, perms, dirarr) = (0,0,0,'rwx------+',[])
  
  if not d: d = getcwd()

  if o: print('\n\t%s:' % d)
  else: out = []

  if d.startswith('//'): d = d[1:]
  
  for f in sorted(ilistdir(d)):
    ft = '-'
    size = f[3]
    total += size
  
    if is_dir(f[1]):
      ft = 'd'
      dirs += 1
      if r:
        dirarr.append(f[0])
      if o:
        print('%s%8s  %-8s %32s' % (ft, perms, size, f[0]))
      
    elif is_file(f[1]):
      ft = '-'
      files += 1
      if d.endswith('/'): d = d[0:-2]
      if d.startswith('/'): d = d[1:]
      if f[0].startswith('/'): f[0] = f[0][1:]
      if f[0].endswith('/'): f[0] = f[0][0:-2]
      
      if o:
        print('%s%8s  %-8s %32s' % (ft, perms, size, f[0]))
      else:
        out.append('/%s/%s' % (d, f[0]))
      
    if len(dirarr):
      ft == 'd'
    
      ret = ls('%s/%s' % (d,f[0]), r, o) # wrd
      
      if ret:
        if not o:
          out.append('%s/%s' % (d, f[0]))
          for f2 in ret['out']:
            out.append('%s' % f2 )

        files += ret['files']
        dirs  += ret['dirs']
        total += ret['total']
      dirarr = []

  if o:
    print('\n%8s total bytes in %d files and %d directories' % (total, files, dirs))
  else:
    return { 'directory': d, 'files': files, 'dirs': dirs, 'total': total, 'out': out }
