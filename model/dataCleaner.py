"""
The goal of this program is to use regex to clean the data
"""
import re
def cleantext(filepath):
    with open(filepath,"r", encoding = "utf8") as corpus:
        allLines = corpus.read()
        
        allLines= re.sub(r"(\bHEADER: \b)[A-Z, a-z,0-9,\/,\.,\-,\:]*\n\n(\bCONTENT: \b)","",allLines)
        
        allLines=re.sub(r'\b([A-Z](?:\.[A-Z]?:)*)\.?', lambda m: ''.join(m.group(0).split('.')), allLines)
        allLines=re.sub(':', ' ', allLines)
        allLines = re.sub(r'\b(\w+)\.(\w+)\b', r'\1. \2', allLines)
        return allLines
        
def splitLines(str):
    allLinesArray = re.split(r"\.|\n",str)
    return allLinesArray



arr = cleantext('../corpuses/test.txt')
