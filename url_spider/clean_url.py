f=open('url_dic_clean','w')
for l in open('url_dic').readlines():
  if len(l)-len(l.replace(' ','')) >1:
    continue;
  else:
    f.writelines(l);
f.close();