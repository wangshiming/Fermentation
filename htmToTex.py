#!/usr/bin/python
import sys,re
FirstFrame=1
def PrintFrame():
    global FirstFrame
    if(not FirstFrame):
        print r'\end{frame}'
    FirstFrame=0
    print('\n')
    print(r'\begin{frame}[shrink] {} ')
    print(r'\addtocounter{questions}{1}')
    print(r'\color{blue}')

def ProcessSubPattern(Line):
    Line=re.sub(r'<sub>', '_{', Line)
    Line=re.sub(r'</sub>', '}', Line) 
    Line=re.sub(r'<.*?>','', Line)
    Line=re.sub(r'[\n]', '', Line)
    Line=re.sub(r'^ *', '', Line)
    searchList=re.findall(r'[^$ ]*?{', Line)  #find all word{
    for patternStr in searchList:
        subStr=patternStr
        patternStr=re.sub('\(','\(',patternStr)  ## get rid of ()
        patternStr=re.sub('\)','\)',patternStr)
        Line=re.sub(' '+patternStr, ' $'+subStr, Line) 
        Line=re.sub('^'+patternStr, ' $'+subStr, Line) 
    searchList=re.findall(r'([^{]*?}[^$ ]*)', Line)  #find all word}word
    for patternStr in searchList:
        subStr=patternStr
        patternStr=re.sub('\(','\(',patternStr)  ## get rid of ()
        patternStr=re.sub('\)','\)',patternStr)
        Line=re.sub(patternStr+' ', subStr+'$ ', Line) 
        Line=re.sub(patternStr+'$', subStr+'$ ', Line) 
#        if re.search(patternStr+'$', Line):
#            Line=re.sub(patternStr, subStr+'$', Line) 

        Line=re.sub(patternStr+'\n', subStr+'\n', Line) 
    Line=re.sub(r'\xc2\xb5',r'\mu', Line)
    return Line

def ProcessTable(f):
    List=[]; subList=[];  Length=0; 
    Line=f.readline()
    print r'\color{gray}'
    tableHead=r'\begin{tabular}[ ]{l'
    while(not(re.search(r'</table>',Line))):
        Line=f.readline()
        if(re.search(r'</table>',Line)):
            break
        Obj1=re.search(r'<th>', Line)
        Obj2=re.search(r'<td>', Line)
        if(Obj1 or Obj2):
            Line=ProcessSubPattern(Line)
        else:
            Line=re.sub(r'<.*?>','', Line)
        if(Obj1):
            List.append(Line)
        if(Obj2):
            subList.append(Line)
    Line=List[0]
    for Item in List[1:]:
        Line=Line+r' & '+Item
        tableHead=tableHead+r' l' 
    print tableHead+r'}'
    print Line+r'  \\'
    ColLen=len(List)
    Lines=len(subList)/len(List)
    for i in range(0,Lines): 
        Line=subList[i*len(List)]
        for Item in subList[i*len(List)+1:(i+1)*len(List)]:
            Line=Line+r' & '+Item
        print Line+ r'  \\'
    print r'\end{tabular}  \\'
    print r'\color{blue}'

filename=sys.argv[1]
try: 
    f = open(filename,'r')
except IOError: 
    print(filename, "not exists")

print r'\documentclass[]{beamer}'
print r'\usetheme{Goettingen}'
print r'\usepackage{amsmath,siunitx,comment}'
print r'\begin{document}'
print r'\parskip=1cm plus 1pt'
print r'\newcounter{questions}'

SectionNames=[]
CurrentSectionName=''
SubSectionNames=[]
CurrentSectionPosition=0

Line= f.readline()
while (not re.search(r'<div class="problem">', Line)):
    searchObj=re.search(r'class="group-heading".*?- (.*?)"',Line)
    if searchObj:
        SectionNames.append(searchObj.group(1))
    searchObj=re.search(r'class="group-heading active".*? (\d*) - (.*?) current chapter"',Line)
    if searchObj:
        CurrentSectionPosition=searchObj.group(1);
        CurrentSectionName=searchObj.group(2)
    searchObj=re.search(r'video</span>.*? (.*)$',Line)
    if searchObj:
        SubSectionNames.append(searchObj.group(1));
        #print SubSectionName; sys.exit()

    Line=f.readline()

SectionNames.insert(int(CurrentSectionPosition)-1, CurrentSectionName)
for SectionName in SectionNames:
    print r'\section{'+SectionName+r'}'
print '\n\n'
for Item in SubSectionNames:
    print r'\subsection{'+Item+r'}'
print r'\setcounter{questions}{0}'

while(Line):
    if(('<div class="problem">' in Line)):
        PrintFrame()
        FirstParagraph=1
        FirstInput=1
    PreviouseLine=''

    if(re.search(r'Select the correct answer',Line)):
        Line=f.readline()
    searchObj=re.search(r'<p>Explanation</p>',Line)
    if searchObj:
        Line=f.readline()
        while(not(re.search('</solution>', Line))):
            Line=f.readline()
            if not Line:
                break
  #         print Line
    if(re.search(r'<table>', Line)):
        ProcessTable(f)

    searchObj=re.search(r'<p>', Line)
    if searchObj:
#        Line=searchObj.group(1)
        searchObj_1=re.search(r'type="math/tex">(.*?)<', Line)
        if searchObj_1:
            temStr=searchObj_1.group(1); 
            print '$'+temStr+'$';
        searchObj_2=re.search(r'<sub>.*?</sub>', Line)
        if searchObj_2:
            Line=ProcessSubPattern(Line)
        Line=re.sub(r'<.*?>','', Line)
        
        Line=re.sub(r'\xc2\xb5',r'$\mu$', Line)
        if(FirstParagraph):
            print Line+r' ({\color{red}{Q\arabic{questions} Answers}})\\'
            FirstParagraph=0
        else: 
            print Line+ r'  \\'

    searchObj_3=re.search(r'<input ', Line)
    if searchObj_3:
        if(FirstInput):
            print r'\color{black}'
            print r'\setlength{\parindent}{-0.4cm}'
        FirstInput=0 

        searchObj_1=re.search(r'type="math/tex".*?>(.*?)<', Line)
        if searchObj_1:
            temStr=searchObj_1.group(1); 
            Line= '$'+temStr+'$';    
        searchObj_2=re.search(r'<sub>.*?</sub>', Line)
        if searchObj_2:
            Line=ProcessSubPattern(Line)
#        else:
#            searchObj_1=re.search(r'>(.*?)$', Line)
#            Line=searchObj_1.group(1)
        Line=re.sub(r'<.*?>', '', Line)
        Line=re.sub(r'\n', '', Line)
        Line=re.sub(r'^ *', '', Line)
        Line=re.sub(r'\xc2\xb5',r'\mu', Line)
        if(re.search(r'correct_answer="true"',PreviousLine)):
            print r'{\color{red}$\bullet$} '+ Line+ r'  \\'; 
        elif(Line):
            print r'{\color{red}$\circ$}'+ Line+ r'  \\';
    PreviousLine=Line 
    Line=f.readline()

f.close()
print r'\end{frame}'
print r'\end{document}'

