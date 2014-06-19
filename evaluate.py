# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 15:24:59 2014

@author: yeonchan
"""
from os import listdir
from os.path import isfile, join
import diact_classifier

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
   
    assert rsCNT == totalCNT
    
    return float(corrects)/float(len(goldenAnswers))

def evaluateCV(classifer, resultFolder, goldenFolderName, fold=10):
    diact_classifier.makeOutDir(resultFolder)
    folds = diact_classifier.makeFolds("./dialog",fold)
    avg_acc = 0.0
    for i in xrange(0,fold):
        test , train = diact_classifier.div_test_train_fold(folds, i)
        classifer(train, test)
        avg_acc += evaluate(resultFolder, goldenFolderName)
        print "%d 'th fold is finished" % i
    return avg_acc/fold
    
if __name__=="__main__":
    #print evaluateCV(diact_classifier.only_presentSTN_maxEnt,"bigram_current","dialog")
    #print evaluateCV(diact_classifier.previous_n_stn_maxEnt,"previous","dialog")
    #print evaluate("bigram_current","dialog")
    #print evaluate("previous_1_current","dialog")
    print evaluate("baseline","dialog")