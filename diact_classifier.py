"""
Created on Sat Jun 14 13:10:27 2014
    This program classify dialog act(DA) of utterences, and output a file formatted like
    who,label,stn in line of a utterance in the outPathName.
    
    You can see the runnning example in the test function
    
    
@author: yeonchan
"""
from FeatureExtractor import FeatureExtractor, FeatureMap
import collections
from os import listdir, makedirs
from os.path import isfile, join, exists
from maxent import MaxentModel
from operator import itemgetter
from collections import deque
import nltk
import evaluate
import pickle
import sys
import pdb

outPathName="baseline"
#feature option flat, we you set this flag as True, you can use corresponding feature.
use_unigram = True
use_bigram = False
use_trigram = False
use_speaker = True
use_postag = False
use_true_label = 0  # if 1: True label, 2: predicted Label, 0 no use
prev=1

posOf_allFiles = {}


def posTagging(inputfolder):
    """Do POS tagging using nltk and store file pos_map"""
    print "Pos tagging of the utterances..."
    files = [ join(inputfolder, f) for f in listdir(inputfolder) if isfile(join(inputfolder, f))]
    rs = {}
    for f in files:
        lines = open(f, "r").readlines()
        listOf_PL = []
	
        for line in lines:
            sss = line.split(",")[2:]
            stn = "".join(sss)
     #       print stn
            text = nltk.tokenize.word_tokenize(stn)
            posResult = nltk.tag.pos_tag(text)
            posList = [pos for (word, pos) in posResult]
            listOf_PL.append(posList)
        print f 
        rs[f] = listOf_PL
    
    pos_file = open("pos_map","w")
    pickle.dump(rs, pos_file)
    pos_file.close()

def loadposTags():
    """ after performing posTagging, load pos_map file """

    global posOf_allFiles
    pos_file = open("pos_map","r")
    posOf_allFiles = pickle.load(pos_file)
   
def previous_n_uts_maxEnt(trainfiles, testfiles):
    """Using maxEntropy model, and feature such as ngram, postag of previous n utterences, classify DAs
    
    Arguments
    trainfiles -- a list of training files 
    testfiles -- a list of test files 
    """

    # used feature : n-gram, previous ngram, current speaker, previous label
    model = MaxentModel()
    model.begin_add_event();
    g_fm = FeatureMap() 
    
    fe = FeatureExtractor(g_fm)
     
     # trainig phase
    for f in trainfiles:
        # format of line :
        # speaker, label(dialog_act), turn   
        lines  = open(f, "r").readlines()
        # we use a queue structure for storing previous label and features such as bigram, ungram
        # while moving term by term, each of labels and features is enqueued or dequeued.

        prev_label = deque( maxlen=prev ) # the deque stores only #prev words
        prev_context = deque( maxlen=prev )
        features = []
        posListOfList = posOf_allFiles[f]
        
        for line_l , line in enumerate(lines):
            
            speaker = line.split(",")[0]
            label = line.split(",")[1]
            stn = "".join(line.split(",")[2:])
            if(line_l>=prev):
                for i in range(0,len(prev_context)):
                    for m in prev_context[i]:
                        features.append("-"+str(i+1)+m)
                    if(use_true_label>0):
                        for m in prev_label[i]:
                            features.append("-"+str(i+1)+m)
                         
            contexts = fe.toContext(stn,use_unigram,use_bigram,use_trigram)                
            if(use_speaker):
                contexts.append(speaker)
            if(use_postag):
                features+=posListOfList[line_l]
                
            features+=contexts
            model.add_event(features, label)
            features = []
            prev_context.append(contexts)
            if(use_true_label==0):
                pass
            elif(use_true_label==1 or use_true_label==2):
                prev_label.append([label])                        
            
                         
    model.end_add_event()
    model.train(100, "lbfgs");
    
    # test phase
    for testfile in testfiles:
        ls = testfile.split("/")
        outfileName = ls[len(ls)-1]
        posListOfList = posOf_allFiles[testfile]
        
        with open(testfile,"r") as f:
            lines = f.readlines()
            prev_label = deque( maxlen=prev )
            prev_context = deque( maxlen=prev )
            with open(outPathName+"/"+outfileName, "w") as outf:
                 for line_l , line in enumerate(lines):
                     
                    spLines = line.split(",")
                    speaker = spLines[0]
                    label = spLines[1]
                    stn = "".join(line.split(",")[2:])
                    
                    if(line_l>=prev):
                        for i in range(0,len(prev_context)):
                            for m in prev_context[i]:
                                features.append("-"+str(i+1)+m)
                            if(use_true_label>0):
                                for m in prev_label[i]:
                                    features.append("-"+str(i+1)+m)
                    
                    
                    contexts = fe.toContext(stn,use_unigram,use_bigram,use_trigram)                                                
                    if(use_speaker):                
                        contexts.append(speaker)
                        
                    features+=contexts
                    
                    if(use_postag):
                        features+=posListOfList[line_l]

                    result = model.eval_all(features)
                    outcome = max(result,key=itemgetter(1))[0] 
                    outf.write(speaker+","+outcome+","+stn)
                    
                    features = []
                    prev_context.append(contexts)
                    if(use_true_label==0):
                        pass
                    elif(use_true_label==1):
                        prev_label.append([label])                        
                    elif(use_true_label==2): # DA for previous utterance by the classifier is used as feature
                        prev_label.append([outcome])  



def getSpeakerDA_STN(line):
    speaker = line.split(",")[0]
    label = line.split(",")[1]
    stn = "".join(line.split(",")[2:])
    return (speaker, label, stn)

def contextWindow_maxEnt(trainfiles, testfiles):
    
    model = MaxentModel()
    model.begin_add_event();
        
    #fe = FeatureExtractor(g_fm)

     # trainig phase
    for f in trainfiles:
        # format of line :
        # speaker, label(dialog_act), turn   
        lines  = open(f, "r").readlines()
        posListOfList = posOf_allFiles[f]

        for i in range(0, len(lines)):
            pword = []
            nword = []
            (ps, pl, pstn) = (None, None, None)
            (ns, nl, nstn) = (None, None, None)
            feature = []
            if i>0:
                pline = lines[i-1]
                (ps, pl, pstn) = getSpeakerDA_STN(pline)
                pword = ["p"+x for x in pstn.split(" ")]
                pPos = ["p"+x for x in posListOfList[i-1]]
                feature += pPos
            
            if i<len(lines)-1:
                nline = lines[i+1]
                (ns, nl, nstn) = getSpeakerDA_STN(nline)
                nword = ["n"+x for x in nstn.split(" ")]
                nPos = ["n"+x for x in posListOfList[i+1]]
                feature += nPos

            print feature
            line = lines[i]
            (s, l, stn) = getSpeakerDA_STN(line)
            
            word = [x for x in stn.split(" ")]
                    
            feature = word+pword+nword 
            #feature = word
            feature += posListOfList[i]

       
            feature.append("speaker_"+s)

            if(ps!=None):
                     feature.append("pspeaker_"+ps)
            if(ns!=None):
                     feature.append("nspeaker_"+ns)
         
            model.add_event(feature, l)
           
    model.end_add_event()
    model.train(100, "lbfgs");

    # test phase
    
    for testfile in testfiles:
        ls = testfile.split("/")
        outfileName = ls[len(ls)-1]
        lines  = open(testfile, "r").readlines()

        posListOfList = posOf_allFiles[testfile]
        with open(outPathName+"/"+outfileName, "w") as outf:       

            for i in range(0, len(lines)):
                pword = []
                nword = []
                (ps, pl, pstn) = (None, None, None)
                (ns, nl, nstn) = (None, None, None)
                feature = []
                if i>0:
                    pline = lines[i-1]
                    (ps, pl, pstn) = getSpeakerDA_STN(pline)
                    pword = ["p"+x for x in pstn.split(" ")]
                    pPos = ["p"+x for x in posListOfList[i-1]]
                    feature += pPos

                if i<len(lines)-1:
                    nline = lines[i+1]
                    (ns, nl, nstn) = getSpeakerDA_STN(nline)
                    nword = ["n"+x for x in nstn.split(" ")]
                    nPos = ["n"+x for x in posListOfList[i+1]]
                    feature += nPos

                line = lines[i]
                (s, l, stn) = getSpeakerDA_STN(line)
                
                word = [x for x in stn.split(" ")]
                feature = word+pword+nword
                #feature = word
                feature += posListOfList[i]
                
                feature.append("speaker_"+s)
                if(ps!=None):
                     feature.append("pspeaker_"+ps)
                if(ns!=None):
                     feature.append("nspeaker_"+ns)

                result = model.eval_all(feature)
                outcome = max(result,key=itemgetter(1))[0] 
                outf.write(s+","+outcome+","+stn)


def printOutFile(lines):

   for x in range(1, len(lines)-1):
        pline = lines[x-1]
        line = lines[x]
        nline = lines[x+1]
        
        (s, l, stn) = getSpeakerDA_STN(line)
        (s1, l1, stn1) = getSpeakerDA_STN(pline)

        print "%s, %s, %s" % (s, l, stn)



def baseline_mostFreqLabel(trainfiles, testfiles):
    """Output the most frequent label. This is baseline"""

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
                    stn = "".join(spLines[2:])
                    outf.write(spLines[0]+","+mostFreqLabel+","+stn)
        
def makeFolds(inputfolder, numFold = 10):
    """make the folds for cross validation and return a list of the files split"""

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
    """ return list of a folds for test and train

    Arguments
    folds -- output of makeFolds

    Return
    a pair of test folds and train fold

    """
    assert(len(folds)>testfoldNum and testfoldNum>=0)
    trainlist = folds[0:testfoldNum]+folds[(testfoldNum+1):len(folds)]
    train = []
    for t in trainlist:
        for t2 in t:
            train.append(t2)
    return folds[testfoldNum], train

def makeOutDir(out):
    """ Make output dirs """
    global outPathName
    outPathName = out
    if not exists(outPathName):
        makedirs(outPathName)

def setParameter(_outPathName, _use_unigram, _use_bigram, _use_trigram, _use_speaker, _use_postag, _use_true_label, _prev):
    """Set the global variables from the arguments"""

    global outPathName, use_unigram, use_bigram, use_trigram, use_speaker, use_postag, use_true_label, prev
    outPathName="baseline"
    use_unigram = _use_unigram
    use_bigram = _use_bigram
    use_trigram = _use_trigram
    use_speaker = _use_speaker
    use_postag = _use_postag
    use_true_label = _use_true_label
    prev=_prev
    
def test(input_folderName, outPath):
    """ test all of the parameter setting(pSet) using MaxEntropy. """

    folds = makeFolds(input_folderName,10)
    test , train = div_test_train_fold(folds, 0)
    
    files = []    
    files+=test
    files+=train
    loadposTags()  
    # parameter setting
    # In pSet, outPathName and options for whether some of features are used for classifying DA
    # _outPathName, _use_unigram, _use_bigram, _use_trigram, _use_speaker, _use_postag, _use_true_label, _prev
    
    # _outPathName -- output path 
    # _use_unigram  -- whether unigram of utterance is used or not
    # _use_bigram -- whether bigram of utterance is used or not
    # _use_trigram -- whether trigram of utterance is used or not
    # _use_speaker -- whether speaker of utterance is used or not
    # _use_postag -- whether POStag of utterance is used or not
    # _use_true_label -- flag for label as feature if 1: True label, 2: predicted Label, 0 no use
    # _prev # how many previous turns are you going to use 

    
    pSet = [
    (outPath + "unigram_0", True, False, False, False, False, 0, 0),
    (outPath + "unigram_1", True, False, False, False, False, 0, 1),
    (outPath + "unigram_2", True, False, False, False, False, 0, 2),
    
    (outPath + "bigram_0", False, True, False, False, False, 0, 0),
    (outPath + "bigram_1", False, True, False, False, False, 0, 1),
    (outPath + "bigram_2", False, True, False, False, False, 0, 2),
    
    (outPath + "uni_bigram_0", True, True, False, False, False, 0, 0),
    (outPath + "uni_bigram_1", True, True, False, False, False, 0, 1),
    (outPath + "uni_bigram_2", True, True, False, False, False, 0, 2),
    
    (outPath + "unigram_speaker_0", True, False, False, True, False, 0, 0),
    (outPath + "unigram_speaker_1", True, False, False, True, False, 0, 1),
    (outPath + "unigram_speaker_2", True, False, False, True, False, 0, 2),

    (outPath + "uni_bigram_speaker_0", True, True, False, True, False, 0, 0),
    (outPath + "uni_bigram_speaker_1", True, True, False, True, False, 0, 1),
    (outPath + "uni_bigram_speaker_2", True, True, False, True, False, 0, 2),    
        
    (outPath + "unigram_speaker_prev_Label_0", True, False, False, True, False, 2, 0),
    (outPath + "unigram_speaker_prev_Label_1", True, False, False, True, False, 2, 1),

    
    (outPath + "unigram_speaker_prevTrueLabel_0", True, False, False, True, False, 1, 0),
    (outPath + "unigram_speaker_prevTrueLabel_1", True, False, False, True, False, 1, 1),
    
    (outPath + "unigram_posTag_speaker_prev_Label_0", True, False, False, True, True, 2, 0),
    (outPath + "unigram_posTag_speaker_prev_Label_1", True, False, False, True, True, 2, 1),

    (outPath + "unigram_posTag_speaker_prevTrueLabel_0", True, False, False, True, True, 1, 0),
    (outPath + "unigram_posTag_speaker_prevTrueLabel_1", True, False, False, True, True, 1, 1)
    
    ]

   
    for ( _outPathName, _use_unigram, _use_bigram, _use_trigram, _use_speaker, _use_postag, _use_true_label, _prev) in pSet:
        setParameter( _outPathName, _use_unigram, _use_bigram, _use_trigram, _use_speaker, _use_postag, _use_true_label, _prev)
        makeOutDir(_outPathName)
        print "%s : %f" % (_outPathName,evaluate.evaluateCV(previous_n_uts_maxEnt,_outPathName,input_folderName))

def testInformationScienceI(input_folderName, outPath):

    folds = makeFolds(input_folderName,10)
    test , train = div_test_train_fold(folds, 0)
    
    files = []    
    files+=test
    files+=train
    loadposTags()
    pSet = [
        (outPath + "context", True, False, False, True, True, 1, 1)
    
    ]
    for ( _outPathName, _use_unigram, _use_bigram, _use_trigram, _use_speaker, _use_postag, _use_true_label, _prev) in pSet:
        setParameter( _outPathName, _use_unigram, _use_bigram, _use_trigram, _use_speaker, _use_postag, _use_true_label, _prev)
        makeOutDir(_outPathName)
        print "%s : %f" % (_outPathName,evaluate.evaluateCV(contextWindow_maxEnt,_outPathName,input_folderName))

'''

if __name__=="__main__":
    input_folder = ""
    if len(sys.argv)==1:
        print "please enter input path as first argument"
    else:
        input_folder = sys.argv[1]
    
    outPath = "./ss_out3/" 
    #posTagging(input_folder) # if you have posmap file you have to run this function
    test(input_folder, outPath)
    

    ./map_test/map_result_isiunigram_posTag_speaker_prev_Label_0 : 0.652026
    ./map_test/map_result_isiunigram_posTag_speaker_prev_Label_1 : 0.663277
    [Finished in 61.0s]

    
'''

if __name__=="__main__":
    
    input_folder = "./dialog"
    outPath = "./map_test/map_result_isi/"
    testInformationScienceI(input_folder, outPath)

    #0.573752 : previous + current + next
    # : previous + current + next
