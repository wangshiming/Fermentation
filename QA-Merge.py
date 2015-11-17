#!/usr/bin/python
import re,sys

QFile=open(sys.argv[1],'r')
AFile=open(sys.argv[2],'r')

QLine=QFile.readline()
while(not re.search(r'setcounter{questions}{0}',QLine)):
    print QLine
    QLine=QFile.readline()


print r'\setcounter{questions}{0}'
print r'\newcounter{answers}'
print r'\setcounter{answers}{0}'

ALine=AFile.readline()  ## Read to the Biginning frame of Answer file
while(not re.search(r'begin{frame}',ALine)):
    ALine=AFile.readline()

while(QLine):
    while(not re.search(r'end{frame}',QLine) and QLine):
        print QLine.strip()
        if re.search(r'setcounter{questions}{0}',QLine):
            print r'\setcounter{answers}{0}'
        QLine=QFile.readline()
    if not QLine:
        break
    print r'\end{frame}'; 

    while(not re.search(r'end{frame}',ALine) and ALine):
        print ALine.strip()
        ALine=AFile.readline()
    print r'\end{frame}';

    while(not re.search(r'begin{frame}',ALine) and ALine):
        ALine=AFile.readline()
   # print 'test='; print ALine; sys.exit()
    QLine=QFile.readline()


