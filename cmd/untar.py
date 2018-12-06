def untar(infile=None, fileobj=None, selected='', outdir='.'):
  import utarfile
  from os import mkdir
  totalfiles = totalbytes = 0
  if fileobj: fp = fileobj
  else: fp = open(infile, 'r+')
  tarfp = tarfile.TarFile(fileobj=fp)
  for f in tarfp:
    if f.type == 'file':
      try:
        outfile = '%s/%s' % (outdir, f.name)
        outfp = open(outfile, 'w+')
        print(outfile)
        totalbytes += outfp.write(tarfp.extractfile(f).read())
        totalfiles+=1
        outfp.close()
      except Exception as e:
        print('ERROR "%s": %s' % (outfile, e))
        continue
    elif f.type == 'dir':
      try:
        newdir = '%s/%s' % (outdir, f)
        mkdir(newdir)
        totalfiles+=1
      except Exception as e:
        print('[dir] ERROR "%s": %s' % (newdir, e))
  print('\n%s files, %s bytes extracted' % ( totalfiles, totalbytes))
  del mkdir, tarfile
