#!/usr/bin/python
#-*-coding:utf-8-*-
import sys,re
NewFrame=1
Question=''
def ProcessSpecialChar(Line):
    #Line=re.sub(r'\n', '', Line)
    #Line=re.sub(r'^ *', '', Line)
    Line=Line.strip()
    Line=re.sub('μ',r'$\mu$', Line)
    Line=re.sub('–','-', Line)
    Line=re.sub(r'\xc2\xb5',r'$\mu$', Line)
    Line=re.sub(r'\xce\xbc',r'$\mu$', Line)
    return Line
def PrintFrame():
    global NewFrame
    if(not NewFrame):
        print r'\end{frame}'
    NewFrame=0
    print('\n')
    print(r'\begin{frame}[shrink] {} ')
    print(r'\color{blue}')

def ProcessSubPattern(Line):
    patternStrings=[]
    Line=ProcessSpecialChar(Line)
    Line=re.sub(r'<font.*?>','',Line)
    Line=re.sub(r'</sub>|</sup>', '}$', Line) 
#    print 'Line='
#    print Line; sys.exit()
    patternStrings=re.findall(r'([0-9A-za-z]*<sub)', Line)
    for Str in patternStrings:
        Obj=re.search(r'(.*)<sub',Str)
        if Obj:
            subStr=Obj.group(1)
            Line=re.sub(Str, r'$'+subStr+r'_{<sub',Line)
    patternStrings=re.findall(r'([0-9A-za-z]*<sup)', Line)
#    print Line; print patternStrings;   
    for Str in patternStrings:
        Obj=re.search(r'(.*)<sup',Str)
        if Obj:
            subStr=Obj.group(1)
            Line=re.sub(Str, r'$'+subStr+r'^{<sup',Line)
    Line=re.sub(r'<.*?>','', Line)

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
#print r'\newcounter{questions}'

SectionNames=[]
CurrentSectionName=''
SubSectionNames=[]
CurrentSectionPosition=0

Line= f.readline()
while (not re.search(r'class="problem-header">', Line)):
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

    Line=f.readline()

SectionNames.insert(int(CurrentSectionPosition)-1, CurrentSectionName)
for SectionName in SectionNames:
    print r'\section{'+SectionName+r'}'
print '\n\n'
for Item in SubSectionNames:
    print r'\subsection{'+Item+r'}'
#print r'\setcounter{questions}{0}'
MATHSEP=r'[0.3em]'
MathSep=''
FirstInput=1
while(Line):
    Line=Line.strip()
    if( re.search(r'class="problem-header">', Line)):
        Line=f.readline()
        Question=Line
        PrintFrame()
        FirstParagraph=1
        FirstInput=1
        MathSep=''

    PreviouseLine=''

    if(re.search(r'Select the correct answer',Line)):
        Line=f.readline()
    searchObj=re.search(r'<p>Explanation</p>',Line) #Skipping 
    if searchObj:
        Line=f.readline()
        while(not(re.search('class="problem-header">', Line))):
            Line=f.readline()
            FirstParagraph=1
            FirstInput=1
            if not Line:
                break
        Line=f.readline()
        Question=Line
        
        if(not Line):
            break
        PrintFrame()

    if(re.search(r'<table>', Line)):
        ProcessTable(f)

    searchObj=re.search(r'<p>', Line)
    if searchObj:
        searchObj_1=re.search(r'type="math/tex">(.*?)<', Line)
        if searchObj_1:
            temStr=searchObj_1.group(1); 
            print '$'+temStr+'$';
        searchObj_2=re.search(r'<sub.*?</sub>', Line)
        searchObj_3=re.search(r'<sup.*?</sup>', Line)
        if (searchObj_2 or searchObj_3):
            Line=ProcessSubPattern(Line)
        Line=re.sub(r'<.*?>','', Line)
        
        Line=re.sub(r'%', r'\%',Line)
        Line=re.sub(r'_{3,}', r'\underline{\quad }',Line)
        Line=re.sub(r'\xc2\xb5',r'$\mu$', Line)
        if(Question and Line):
            Obj=re.search(r'(\w*)$', Question)
            print Line+r' ({\color{red}{Q'+Obj.group(1)+r'}})\\'
            Question=''
        elif Line: 
            print Line+ r'\\'

    searchObj_3=re.search(r'<input ', Line)
    if searchObj_3:
        if(FirstInput):
            print r'\color{black}'
            print r'\setlength{\parindent}{-0.4cm}'
        FirstInput=0 

        searchObj_1=re.search(r'type="math/tex".*?>(.*?)<', Line)
        if searchObj_1:
            MathSep=MATHSEP
            temStr=searchObj_1.group(1); 
            Line= '$'+temStr+'$';    
        searchObj_2=re.search(r'<sub.*?</sub>', Line)
        searchObj_3=re.search(r'<sup.*?</sup>', Line)
        if (searchObj_2 or searchObj_2):
            Line=ProcessSubPattern(Line)
        Line=re.sub(r'<.*?>', '', Line)
        Line=ProcessSpecialChar(Line)

        if(re.search(r'correct_answer="true"',PreviousLine)):
            print r'{\color{red}$\bullet$} '+ Line+ r' \\'+MathSep; 
        elif(Line):
            print r'{\color{red}$\circ$} '+ Line+ r' \\'+MathSep;
    PreviousLine=Line 
    Line=f.readline()

f.close()
print r'\end{frame}'
print r'\end{document}'

