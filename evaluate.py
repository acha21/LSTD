# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 15:24:59 2014
This module is made in the purpose of a evaluating dialact_callfier 

@author: yeonchan
"""
from os import listdir
from os.path import isfile, join
import diact_classifier
import sys

def evaluate(resultFolder, goldenFolderName):
    ''' calculate precision of resultFolder
    
    Arguments
    resultFolder : The output of classifier should be in this folder in the same form of goldenStandard
    goldenFolder : The golden standard of classifier should be here 
    '''

    rsFiles = [f for f in listdir(resultFolder) if isfile(join(resultFolder,f))]
    goldFiles = [f for f in listdir(goldenFolderName) if isfile(join(goldenFolderName,f))]
    
    rsFileMap = {}
    for rsFile in rsFiles:    
        rsFileMap[rsFile]=0
        
    totalCNT = 0
    rsCNT = 0
    goldenAnswers = []
    rsAnswers = []
    
    for rs in rsFiles:
        with open(resultFolder+"/"+rs, "r") as f:
            lines = f.readlines()
            for line in lines:
                rsAnswers.append(line.split(",")[1])
            rsCNT += len(lines)
                
    #for gf in goldFiles:
    #   if(rsFileMap.has_key(gf)):
        with open(goldenFolderName+"/"+rs, "r") as f:
            lines = f.readlines()
            for line in lines:
                goldenAnswers.append(line.split(",")[1])
            totalCNT += len(lines)
        
        #print "classifier CNT %d, golden CNT %d" %(rsCNT, totalCNT)
        assert rsCNT == totalCNT
         
    index =0
    corrects =0
    for ga in goldenAnswers:        
        if(ga==rsAnswers[index]):
            corrects+=1
        index+=1   
   
    return float(corrects)/float(len(goldenAnswers))

def evaluateCV(classifer, resultFolder, goldenFolderName, fold=10):
    diact_classifier.makeOutDir(resultFolder)
    folds = diact_classifier.makeFolds(goldenFolderName,fold)
    avg_acc = 0.0
    for i in xrange(0,1):
        test , train = diact_classifier.div_test_train_fold(folds, i)
        classifer(train, test)
        acc = evaluate(resultFolder, goldenFolderName)
        avg_acc += acc
        #print "%f %d 'th fold is finished" % (acc, i)
    return avg_acc/1
    
if __name__=="__main__":
    print sys.argv[1] 
    print evaluate(sys.argv[1],sys.argv[2])
    print "ok"
