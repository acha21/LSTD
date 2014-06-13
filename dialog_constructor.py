# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 15:21:46 2014
In the MapCorpus, all the words are tagged, and the utternces are splited by tokens(word).
So we need to build dialouge data from the MapCorpus

This program 
@author: yeonchan
"""

import xml.etree.ElementTree as ET
import re
import optparse as OPT
import sys

__DEBUG__ = False

s_pattern_C = re.compile("(id\([a-z]{1}[0-9]{1}[a-z]{2}[0-9]{1}[gf]{1}\.)([0-9])")
move_path = "/home/yeonchan/workspace/LSTD/maptaskv2-0/Data/moves/"
timed_unit_path = "/home/yeonchan/workspace/LSTD/maptaskv2-0/Data/timed-units/"
def reconstructDial(dialogueAct):
    '''
        The moves files contains words split.
        This function makes the words to be merged as sentence.
        finally, it returns utt,label,startOfmove
    '''
    tree_moves = ET.parse(move_path+dialogueAct+".moves.xml")
    root_moves = tree_moves.getroot()
    tag_units = []
    prefix = ""
    for child in root_moves:
        
        if(child.tag == "move"):
            cc = child.find("{http://nite.sourceforge.net/}child")
            ss = cc.get('href').split("#")[1]
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
    timed_tree = ET.parse(timed_unit_path+dialogueAct+".timed-units.xml")
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
                    if(startOfmove < startTime):
                        startOfmove = startTime
                #print (num, word)
            else:
                continue
        if(uttArray!=None):
            utt = " ".join(uttArray)
        utts.append((utt,label,startOfmove))
        utt = ""
       
    return utts

# this functio returns a list of (speaker, label, stn, time)
def getDialogFromMapCorpus(dialName):
    total_utters = []
    g_utters = reconstructDial(dialName+".g")
    for lis in g_utters:
       total_utters.append(("g", lis[0],lis[1],lis[2]))
    
    f_utters = reconstructDial(dialName+".f")
    for lis in f_utters:
       total_utters.append(("f", lis[0],lis[1],lis[2]))
       
    turns = sorted(total_utters, key=lambda (a,b,c,d): d)
    if __DEBUG__:
        for speaker, stn,label,startOfmove in turns:
            print "%s (%s) %s" % (speaker, label, stn)
    
    return turns

def writeDialog(fName, turns):
    with open(fName,"w") as f:
        for turn in turns:
            f.write(turn[0]+","+turn[2]+","+turn[1]+"\n")
        
from os import listdir
from os.path import isfile, join


if __name__=="__main__":
    
    p = OPT.OptionParser(description="This program process mapcourpus and build dialog text",
                         usage=" $python dialog_constructor.py pathName")
                         
    p.add_option("-o","--outpath", action="store", type="string", dest="outpath")
    opt, args = p.parse_args()
    
   
    onlyfiles = [ f for f in listdir(move_path) if isfile(join(move_path, f))]
    dialNames = set([])
    for f in onlyfiles :
        dialNames.add(f.split(".")[0])
    
    
    for name in dialNames :
        print "-------------------", name
        if name!="":
            turns = getDialogFromMapCorpus(name)
            writeDialog("dialog/"+name+".dg", turns)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    