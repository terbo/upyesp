def env():
  e = sorted(dir())
  global_vars = []
  global_funcs = []

  for v in e:
    if (v in globals()) and type(globals()[v]) == str:
      global_vars.append(('%s','%s') % (v, globals()[v]))
    else:
      l = sorted(dir(eval(v)))
      global_funcs.append(('%s','%d') % (v, len(l)))
   
  print('Classes/Functions:\n')
  
  for v in global_funcs:
    print(v)
  
  print('\nVariables:\n')
  
  for v in global_vars:
    if v in globals():
      print('%-12s: %32s' % (v, globals()[v]))
    else:
      print('%-12s' % (v))
