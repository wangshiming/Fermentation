#!/usr/bin/python
import sys,re
f=open(sys.argv[1],'r')
StrLists=[]
Str=f.readline()
i=1
while(Str): ## Add 0.5em before the choice
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
#    print Str##
    Str=re.sub(r'\\\\.*','',Str)
 #   print Str; sys.exit()##
    print Str+r'\\[0.5em]'
    print r'\color{black}'
    StrLists=[]
    Str=f.readline()

Obj=re.search(r'(.*)_)',sys.argv[1])
w=open(Obj.group(1),'w')
f.position(0)

f.close()
w.close()

