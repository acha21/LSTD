# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 15:24:59 2014

@author: yeonchan
"""
from os import listdir
from os.path import isfile, join

def evaluate(resultFolder, goldenFolderName):
    rsFiles = [f for f in listdir(resultFolder) if isfile(join(resultFolder,f))]
    goldFiles = [f for f in listdir(goldenFolderName) if isfile(join(goldenFolderName,f))]
    
    rsFileMap = {}
    for rsFile in rsFiles:    
        rsFileMap[rsFile]=0
        
    totalCNT = 0
    
    goldenAnswers = []
    rsAnswers = []
    
    for rs in rsFiles:
        with open(resultFolder+"/"+rs, "r") as f:
            lines = f.readlines()
            for line in lines:
                rsAnswers.append(line.split(",")[1])
                rsCNT = len(lines)
                
    for gf in goldFiles:
        if(rsFileMap.has_key(gf)):
            with open(goldenFolderName+"/"+gf, "r") as f:
                lines = f.readlines()
                for line in lines:
                    goldenAnswers.append(line.split(",")[1])
                    totalCNT = len(lines)
    index =0
    corrects =0
    for ga in goldenAnswers:        
        if(ga==rsAnswers[index]):
            corrects+=1
        index+=1   
    print rsCNT, totalCNT
    assert rsCNT == totalCNT
    
    print float(corrects)/float(len(goldenAnswers))
    
if __name__=="__main__":
    evaluate("bigram_current","dialog")