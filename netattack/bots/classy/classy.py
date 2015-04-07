import random, sys
f,e,p=[],[],[]
for si,s in enumerate(sys.argv[1].split()):
    if s[0]=='F': f+=[(int(s[1:]),si)]
    else: e+=[(int(s[1:]),si)]
f=sorted(f,key=lambda t:t[0]);r=4
f1,f2,f3=f[:len(f)//r],f[len(f)//r:len(f)//r*2],f[len(f)//r*2:]
for fa in f3:
    ea=[t for t in e if t[0]<fa[0]]
    p+=[(fa[1],random.choice(ea)[1])] if ea else [(fa[1],fa[1])]
for fd,fs in zip(f1,reversed(f2)):
    p+=[(fs[1],fd[1])]
    p+=[(fd[1],fd[1])]
if len(e)==0: p=[(fe[1],0) for fe in f]
for t in p: print(t[0],',',t[1],' ',sep='',end='')
sys.stdout.flush()