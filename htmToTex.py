#!/usr/bin/python
#-*-coding:utf-8-*-
import sys,re
NewFrame=1
Question=''
def getStringPattern(Str):
    StrPattern=Str
    StrPattern=re.sub(r'\(',r'\(',Str)
    StrPattern=re.sub(r'\)',r'\)',StrPattern)
    StrPattern=re.sub(r'\[',r'\[',StrPattern)
    StrPattern=re.sub(r'\]',r'\]',StrPattern)
    ##StrPattern=re.sub('\\\\',r'\\\\',StrPattern) ##Hard; Str=\\hello; when print out: \hello
    return StrPattern
def ProcessSpecialChar(Line):
    Line=re.sub('μ',r'$\mu$', Line)
    Line=re.sub('–','-', Line)
    Line=re.sub(r'\xc2\xb5',r'$\mu$', Line)
    Line=re.sub(r'\xce\xbc',r'$\mu$', Line)
    Line=re.sub(r'%', r'\%',Line)
    Line=re.sub(r'&gt;', r' > ', Line)
    Line=re.sub(r'_{3,}', r'\underline{\quad }',Line)
    return Line
def PrintFrame():
    global NewFrame
    if(not NewFrame):
        print r'\end{frame}'
    NewFrame=0
    print('\n')
    print(r'\begin{frame}[shrink] {} ')
    print(r'\color{blue}')
def ProcessMath(Line):
    Line=re.sub(r'<script type="math/tex".*?>',r'$',Line)
    Line=re.sub(r'</script>',r'$',Line)
    Obj=re.search(r'(\$.*?\$)',Line)
    #print Obj.group(1); print 'IN MATH==';sys.exit()
    return Obj.group(1)

def ProcessSubPattern(Line):
    patternStrings=set()
    Line=ProcessSpecialChar(Line)
    Strings=re.findall(r'<.*?>',Line) #get rid of non <sub...> tag
    for Str in Strings:
        if(not(r'sub' in Str)):
            StrPat=getStringPattern(Str)
            Line=re.sub(StrPat,'',Line)

    Line=re.sub(r'</sub>|</sup>', '}$', Line) 
    Strings=re.findall(r'([0-9A-za-z]{1,}<sub)', Line)
    for Str in Strings:
        patternStrings.add(Str)
    for Str in patternStrings: 
        StrPat=getStringPattern(Str)
        Line=re.sub(StrPat, r'$'+Str,Line)
    Line=re.sub(r'<sub',r'_{<sub',Line)
    
    Strings=re.findall(r'([0-9A-za-z]{1,}<sup)', Line)
    for Str in Strings:
        patternStrings.add(Str)
    for Str in patternStrings: 
        StrPat=getStringPattern(Str)
        Line=re.sub(StrPat, r'$'+Str,Line)
    Line=re.sub(r'<sup',r'^{<sup',Line)
    Line=re.sub(r'<.*?>', '', Line)
    Line=ProcessSpecialChar(Line)
    return Line

def ProcessTable(f):
    List=[]; subList=[];  Length=0; 
    Line=f.readline()
    print r'\color{gray}'
    tableHead=r'\begin{tabular}[ ]{l'
    while(not(re.search(r'</table>',Line))):
        Line=f.readline()
        Line=Line.strip()
        if(re.search(r'</table>',Line)):
            break
        temList=re.findall(r'<th>.*?</th>',Line)
        for i in range(0,len(temList)):
            List.append(ProcessSubPattern(temList[i]))

        temList=re.findall(r'<td>.*?</td>',Line)
        for i in range(0,len(temList)):
            subList.append(ProcessSubPattern(temList[i]))

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
            MathSep=''
            if not Line:
                break
        Line=f.readline()
        Question=Line
        
        if(not Line):
            break
        PrintFrame()

    if(re.search(r'<table', Line)):
        ProcessTable(f)

    searchObj=re.search(r'<p', Line)
    if searchObj:
        searchObj_1=re.search(r'type="math/tex"', Line)
        if searchObj_1:
            Line=ProcessMath(Line)

        searchObj_2=re.search(r'<sub.*?</sub>', Line)
        searchObj_3=re.search(r'<sup.*?</sup>', Line)
        if (searchObj_2 or searchObj_3):
            Line=ProcessSubPattern(Line)
        Line=re.sub(r'<.*?>', '', Line)
        Line=ProcessSpecialChar(Line)
        if(Question and Line):
            Obj=re.search(r'(\w*)$', Question)
            print Line+r' ({\color{green}{Q'+Obj.group(1)+r'}})\\'
            Question=''
        elif Line: 
            print Line+ r'\\'

    searchObj_3=re.search(r'<input', Line)
    if searchObj_3:
        if(FirstInput):
            print r'\color{black}'
            print r'\setlength{\parindent}{-0.4cm}'
        FirstInput=0 

        searchObj_1=re.search(r'type="math/tex"', Line)
        if searchObj_1:
            Line=ProcessMath(Line)
            MathSep=MATHSEP
                     
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

