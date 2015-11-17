#!/usr/bin/python
import sys,re
f=open(sys.argv[1],'r')
StrLists=[]
Str=f.readline()
i=1
while(Str):
    Str=Str.strip()
    while(not ('color{black}' in Str) and Str):
        if(not(r'\\' == Str.strip())):
            StrLists.append(Str)
        Str=f.readline()
        #print i;sys.exit()
    Len=len(StrLists)
    for Str in StrLists[0:Len-1]:
        Str=Str.strip()
        if Str:
            print Str.strip()
        if Str==r'\end{frame}':
            print ''
    Str=StrLists[Len-1]
    Str=Str.strip()
    if (r'\end{document}' in Str):
        print Str
        break
    Str=re.sub(r'\[.*\]|\\','',Str)
    print Str+r'\\[0.5em]'
    print r'\color{black}'
    StrLists=[]
    Str=f.readline()
f.close()
