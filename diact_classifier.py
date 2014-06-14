# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 13:10:27 2014
    This program classify the dial_act, and output a file formatted like
    who,label,stn in line of a utterance
    in the 
    
@author: yeonchan
"""
from FeatureExtractor import FeatureExtractor, FeatureMap
import collections
from os import listdir, makedirs
from os.path import isfile, join, exists
from maxent import MaxentModel
from operator import itemgetter

outPathName="baseline"


def only_presentSTN_maxEnt(trainfiles, testfiles):
    model = MaxentModel()
   
    model.begin_add_event();
    g_fm = FeatureMap() 
    for f in trainfiles:
        #print f
        lines  = open(f, "r").readlines()
        for line in lines:
            speaker = line.split(",")[0]
            label = line.split(",")[1]
            stn = line.split(",")[2]
            #print speaker, label, stn
            fe = FeatureExtractor(g_fm)
            contexts = fe.toContext(stn,True,True,True)                
            model.add_event(contexts, label)
            
                
    model.end_add_event()
    model.train(100, "lbfgs");
    
    for testfile in testfiles:
        ls = testfile.split("/")
        outfileName = ls[len(ls)-1]
        with open(testfile,"r") as f:
            lines = f.readlines()
            with open(outPathName+"/"+outfileName, "w") as outf:
                for line in lines:
                    spLines = line.split(",")
                    stn = spLines[2]
                    fe = FeatureExtractor(g_fm)
                    #print stn                 
                    result = model.eval_all(fe.toContext(stn,True,True,True))
                    outcome = max(result,key=itemgetter(1))[0] 
                    #print result
                    print spLines[0]+","+outcome+","+spLines[2]
                    outf.write(spLines[0]+","+outcome+","+spLines[2])
                    
                   

    
def baseline_mostFreqLabel(trainfiles, testfiles):
    '''
        Here we find the most frequent label
    '''            
    labelCNT = collections.defaultdict(int)   
    
    for f in trainfiles:
        lines  = open(f, "r").readlines()
        for line in lines:
            labelCNT[line.split(",")[1]]+=1
    maxCNT =0
    for key in labelCNT.keys():
        cnt = labelCNT[key]
        if(cnt>maxCNT):
            maxCNT = cnt
            mostFreqLabel = key
            
    
    
    for testfile in testfiles:
        ls = testfile.split("/")
        outfileName = ls[len(ls)-1]
        with open(testfile,"r") as f:
            lines = f.readlines()
            
            with open(outPathName+"/"+outfileName, "w") as outf:
                for line in lines:
                    spLines = line.split(",")
                    outf.write(spLines[0]+","+mostFreqLabel+","+spLines[2])
        

def makeFolds(inputfolder, numFold = 10):
    onlyfiles = [ f for f in listdir(inputfolder) if isfile(join(inputfolder, f))]
    fold = []
    folds = []
    leng = len(onlyfiles)
    size= round(leng / numFold +0.5)
    cnt =0    
    for f in onlyfiles :
        cnt+=1
        if(cnt<size):
            fold.append(join(inputfolder, f))
        elif(size==cnt):
            fold.append(join(inputfolder, f))
            folds.append(fold)
            cnt =0
            fold = []

        if(numFold==(len(folds)+1)):
            folds.append(fold)
   
    return folds

def div_test_train_fold(folds, testfoldNum):
    assert(len(folds)>testfoldNum and testfoldNum>=0)
    trainlist = folds[0:testfoldNum]+folds[(testfoldNum+1):len(folds)]
    train = []
    for t in trainlist:
        for t2 in t:
            train.append(t2)
    return folds[testfoldNum], train

def makeOutDir(out):
    global outPathName
    outPathName = out
    if not exists(outPathName):
        makedirs(outPathName)
if __name__=="__main__":
    makeOutDir("bigram_current")
    folds = makeFolds("./dialog",10)
    test , train = div_test_train_fold(folds, 2)
    only_presentSTN_maxEnt(train, test)