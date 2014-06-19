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
from collections import deque
import evaluate

outPathName="baseline"

def previous_n_uts_maxEnt(trainfiles, testfiles):
    # used feature : n-gram, previous ngram, current speaker, previous label
    model = MaxentModel()
    prev = 1
    model.begin_add_event();
    g_fm = FeatureMap() 
    ext_unigram = True
    ext_bigram = False
    ext_trigram = False
    
    fe = FeatureExtractor(g_fm)
     
    for f in trainfiles:
        #print f
        lines  = open(f, "r").readlines()

        prev_label = deque( maxlen=prev )
        prev_context = deque( maxlen=prev )
        features = []
        for line_l , line in enumerate(lines):
            speaker = line.split(",")[0]
            label = line.split(",")[1]
            stn = line.split(",")[2]
            
            if(line_l>=prev):
                for i in range(0,len(prev_context)):
                    for m in prev_context[i]:
                        features.append("-"+str(i+1)+m)
                    for m in prev_label[i]:
                        features.append("-"+str(i+1)+m)
                         
            #print speaker, label, stn
           
            contexts = fe.toContext(stn,ext_unigram,ext_bigram,ext_trigram)                
            
            features+=(contexts+[speaker])
            model.add_event(features, label)
            features = []
            prev_context.append(contexts)
            prev_label.append([label])
            
                
    model.end_add_event()
    model.train(100, "lbfgs");
    
    for testfile in testfiles:
        ls = testfile.split("/")
        outfileName = ls[len(ls)-1]
        with open(testfile,"r") as f:
            lines = f.readlines()
            prev_label = deque( maxlen=prev )
            prev_context = deque( maxlen=prev )
            with open(outPathName+"/"+outfileName, "w") as outf:
                 for line_l , line in enumerate(lines):
                     
                    spLines = line.split(",")
                    stn = spLines[2]
                    speaker = spLines[0]
                    
                    if(line_l>=prev):
                        for i in range(0,len(prev_context)):
                            for m in prev_context[i]:
                                features.append("-"+str(i+1)+m)
                            for m in prev_label[i]:
                                features.append("-"+str(i+1)+m)
                    
                    contexts = fe.toContext(stn,ext_unigram,ext_bigram,ext_trigram)                                                
                    features+=(contexts+[speaker])
                    
                    #print stn                 
                    result = model.eval_all(features)
                    outcome = max(result,key=itemgetter(1))[0] 
                    #print result
                    #print spLines[0]+","+outcome+","+spLines[2]
                    outf.write(spLines[0]+","+outcome+","+spLines[2])
                    
                    features = []
                    prev_context.append(contexts)
                    prev_label.append([outcome])
                    

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
                    #print spLines[0]+","+outcome+","+spLines[2]
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

def testCurrentBigram():
    out = "bigram_current"
    makeOutDir(out)
    folds = makeFolds("./dialog",10)
    test , train = div_test_train_fold(folds, 2)
    #only_presentSTN_maxEnt(train, test)
    #previous_n_uts_maxEnt(train, test)
    print evaluate.evaluateCV(previous_n_uts_maxEnt,"bigram_current","dialog")
    #evaluateCV(diact_classifier.previous_n_stn_maxEnt,"previous","dialog")
    #print evaluate.evaluate(out,"dialog")
    #evaluate("previous_1_current","dialog")
    
if __name__=="__main__":
    testCurrentBigram()