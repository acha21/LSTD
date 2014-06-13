'''
Created on 2014. 6. 9.

@author: yeonchan
'''

import collections
import pickle
import os
from maxent import MaxentModel
import xml.etree.ElementTree as ET
import re
import pdb

# Set __DEBUG__ to True to display debugging messages.
__DEBUG__ = False
model = MaxentModel()

class FeatureMap():
    
    def __init__(self):
        
        self.unigrams = collections.defaultdict(int)
        self.bigrams = collections.defaultdict(int)
        self.trigrams = collections.defaultdict(int)

        
g_fm = FeatureMap()      
g_fileName = "FeatureMap" 

class FeatureExtractor(object):
    '''
    classdocs
    '''
    
    def __init__(self, fMap):
        '''
        Constructor
        '''
        self.fMap = fMap
        
    def extractNgrams(self, str):
        wordlist = str.split()
        i = 0
        if(len(wordlist)>2):
            for i in xrange(0,len(wordlist)-2):
                self.fMap.unigrams[wordlist[i]]+=1
                self.fMap.bigrams[(wordlist[i], wordlist[i+1])]+=1
                self.fMap.trigrams[(wordlist[i], wordlist[i+1], wordlist[i+2])] +=1
                i+=1
        elif(len(wordlist)>1):
            for i in xrange(0,len(wordlist)-1):
                self.fMap.unigrams[wordlist[i]]+=1
                self.fMap.bigrams[(wordlist[i], wordlist[i+1])]+=1
                i+=1
        elif(len(wordlist)>0):
            for i in xrange(0,len(wordlist)):
                self.fMap.unigrams[wordlist[i]]+=1
                i+=1
    
    def toContext(self, stn):
        wordlist = stn.lower().split()
        
        context = []
        
        for i in range(0,len(wordlist)):
            context.append("u_"+wordlist[i]) #unigram
            if(i+1 >= len(wordlist)):
                context.append("b_"+wordlist[i]+"_END")
            elif(i+1 < len(wordlist)):
                context.append("b_"+wordlist[i]+"_"+wordlist[i+1])
                           
            if((len(wordlist)-i)==2):
                context.append("t_"+wordlist[i]+"_"+wordlist[i+1]+"_END")
                
            if((len(wordlist)-i)==1):
                context.append("t_"+wordlist[i]+"_END_END")
                
            if((len(wordlist)-i)>=3):
                context.append("t_"+wordlist[i]+"_"+wordlist[i+1]+"_"+wordlist[i+2])
            
        print wordlist, context      
        return context

def loadFeatureMap():
    g_fm = pickle.load(g_fileName)
    
def saveFeatureMap():
     with open(g_fileName,'w') as f:
         pickle.dump(g_fm, f)
            
def processFeatExtract():
    #loadFeatureMap()
    filelist = os.listdir("Transcripts")
    
    for file in filelist:
        with open("Transcripts/"+file,"r") as f:
            lines = f.readlines()
        
        i = 0
        for line in lines:
            if(i>3): # first 2 lines will be ignored.
                fe = FeatureExtractor(g_fm)
                if(len(line.split("\t"))>2):
                    fe.toContext(line.lower().split("\t")[1])
            i+=1

    
    saveFeatureMap()
    
s_pattern_C = re.compile("(id\([a-z]{1}[0-9]{1}[a-z]{2}[0-9]{1}[gf]{1}\.)([0-9])")

def reconstructDial(dialogueAct):
    
    tree_moves = ET.parse("move_test/"+dialogueAct+".moves.xml")
    root_moves = tree_moves.getroot()
    tag_units = []
    prefix = ""
    for child in root_moves:
        
        if(child.tag == "move"):
            cc = child.find("{http://nite.sourceforge.net/}child")
            ss = cc.get('href').split("#")[1]
            #print ss
            str = s_pattern_C.sub(r"\2", ss).replace(")"," ")
            prefix = ss[3:].split(".")[0]
            
            start = 0
            end = 0
           
            pages = [s.strip() for s in str.split("..")]
            
            #print pages
            if(len(pages)==2):
                val0 = float(pages[0]) if pages[0].find(".")!=-1 else int(pages[0])
                val1 = float(pages[1]) if pages[1].find(".")!=-1 else int(pages[1])
                (start, end) = (val0, val1)
                #print (val0, val1)
            elif(len(pages)==1):
                val = float(pages[0]) if pages[0].find(".")!=-1 else int(pages[0])
                (start, end) = (val, val)
            label = child.get('label')
            tag_units.append((start, end, label))
        
    # end for child in root_moves
    
    timed_tree = ET.parse("timed/"+dialogueAct+".timed-units.xml")
    root_timed = timed_tree.getroot()
    
    wordsByNum = []
    for child in root_timed:
        if(child.tag=="sil" or child.tag=="tu"):
            ID = child.attrib["id"]
            prefix = ID.split(".")[0]
            num = ID[len(prefix)+1:]
           
            wordsByNum.append((float(num), child.text, float(child.attrib['start'])))
    
    utts = []
    for (start, end, label) in tag_units:
        uttArray = []
        startOfmove = 0.0
        for (num, word,startTime) in wordsByNum:
           # print "num : %f, start : %d, end : %d" %(num, start, end)
            if(num>=start and num<end+1):
                if(word!=None):
                    uttArray.append(word)
                    if(startOfmove<startTime):
                    
                        startOfmove = startTime
                #print (num, word)
            else:
                continue
        if(uttArray!=None):
            utt = " ".join(uttArray)
        utts.append((utt,label,startOfmove))
        utt = ""
       
    sorted(utts, key=lambda (a,b,c): c)
    for stn,label,startOfmove in utts:
        print dialogueAct[len(dialogueAct)-1], label, startOfmove, stn
      
#def getDialogActsLabel():
#    transPathName = "Tr_test"
#    filelist = os.listdir(transPathName)
#    all_stn = {}
#    for file in filelist:
#        with open(transPathName+"/"+file,"r") as f:
#           
#            lines = f.readlines()
#            linNum = 0
#            cnt = 0
#            for line in lines:
#                cnt+=1
#                if(cnt<4): continue
#                (fileNa, f_or_g) = ( file.split(".")[0], line.split("\t")[0])
#                linNum += 1
#                id = fileNa +"."+f_or_g+".move."+str(linNum)
#                if len(line.split("\t"))>2:
#                    stn = line.split("\t")[1]
#                    all_stn[id] = stn
#                    print id, stn
#         
#    #labelPathName = '/home/yeonchan/workspace/LSTD/maptaskv2-0/Data/moves'
#    labelPathName = '/home/yeonchan/workspace/LSTD/map_test'
#    train_triples = []
#    for fname in os.listdir(labelPathName):
#        tree = ET.parse(labelPathName+"/"+fname)
#        root = tree.getroot()
#        for child in root:
#            #print child.tag, child.attrib
#            if (child.tag=="move"):
#                id = child.attrib['id']
#                label = child.attrib['label']
#                if(id in all_stn.keys()):
#                    print id, label+" : "+all_stn[id]
#                    train_triples.append((id, label, all_stn[id]))
#                else:
#                    print "None exist id in the sentence %s %s" % (id, label)
#    for triple in train_triples:
#        print triple
#         
    
def testGetDA():
    getDialogActsLabel()
    
def testExtractNgram():
    stn = "S\tI am your girl."
    fe = FeatureExtractor(g_fm)
    fe.toContext(stn.lower().split("\t")[1])

    
    
def mappping(grams, itmap, timap):
    for gram in grams.keys():
        idx = len(g_fm.timap)
        g_fm.timap[gram] = idx
        g_fm.itmap[idx] = gram
        
if __name__=="__main__":
    #processFeatExtract()
    #testExtractNgram("S\tMy Name is")
    #testExtractNgram()
    reconstructDial("q1ec1.g")
    reconstructDial("q1ec1.f")