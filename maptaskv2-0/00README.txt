This is a public release of the HCRC Map Task Corpus Annotations,
version 2.0.  The web page for the corpus is at
http://www.hcrc.ed.ac.uk/maptask.  This release was prepared
by Jean Carletta, Amy Isard, and Colin Matheson at the University
of Edinburgh.

This version of the corpus is in the correct format for use with
the NITE XML Toolkit (http://www.ltg.ed.ac.uk/NITE), version 1.3.6
or higher.  NXT relies on Java 1.4 or higher.

The release contains a translation of the XML annotations from
an earlier version of the corpus in a pre-NXT stand-off XML format,
plus some GUI tools and documentation for how to use the data in
this format. You must go to the documentation of the earlier format
for information about what the annotations themselves mean.

This material is released under the Creative Commons
Attribution-NonCommercial-ShareAlike License version 2.5.  See
00LICENSE.html.

The public release is built from a CVS repository to which improvements
can be contributed.  Contact maptask@cogsci.ed.ac.uk for access.

------------------------------------------------
MAP TASK HISTORY
------------------------------------------------

The HCRC Map Task audio and transcriptions were released on
CD in 1992.  The CDs are available from the Linguistic Data Consortium.

Over the years, various Edinburgh projects have created annotations
for a range of linguistic phenomena for the corpus.  These were used
to create an on-line demo at
http://www.hcrc.ed.ac.uk/maptask/interface/ that still exists.  The
demo web pages are a good place to find information about the
annotations.

In 2001, the annotations were released publicly on the web at
http://www.hcrc.ed.ac.uk/maptask/ in a stand-off XML format as "The
HCRC Map Task Corpus Annotations Version 1.0".  The NXT format data
is a translation of these annotations and should be considered a
replacement for this format.  NXT allows better access to the data
because the release includes GUIs for viewing the data on a local
machine, whereas before the only way to use a GUI on the data was
via the web demo.  The NXT format data omits the automatic syntax
from the original.

-------------------------------------------------
TWO CORPORA IN ONE ARCHIVE
-------------------------------------------------

This data set is actually two NXT-format corpora in one archive.

The primary corpus is the set of Map Task dialogues - that is,
recordings of the dialogues along with transcription and a great deal
of annotation for many different linguistic phenomena (dialogue
structure, disfluency, references to landmarks, and so on).  The NXT
metadata for this is in Data/maptask.xml.  Most users want this corpus.

Each Map Task participant read out a list of landmark names to create
"citation" forms against which landmark references in the running
speech of the dialogues could be compared.  The secondary corpus is
the set of word lists that the participants read out.  The NXT
metadata for this corpus is in Data/maptask-wordlists.xml.

The two corpora are disjoint apart from two files - both of them
make use of Data/corpus-resources/maptask-landmarks.xml and
Data/corpus-resources/maptask-participants.xml.

------------------------------
INSTRUCTIONS FOR RUNNING NXT GUIS
------------------------------

NXT does not come with this data distribution - get it from
http://www.ltg.ed.ac.uk/NITE.

To run, you must edit the shell scripts (*.sh/*.bat) to set $NXT to 
the root directory of your NXT installation, or else unzip the NXT 
distribution and this one to the same location.  We recommend the former.

If you wish to listen to the dialogues or citation lists, you must
download the signals.  The NXT metadata file for the dialogues ,
Data/maptask.xml, declares that both kinds of signals (dialogues and
citation lists) should be found at the path ./signals, that is, in a
subdirectory called "signals" of the Data directory.  To change this,
edit the path attribute of the <signals> tag.  You can keep the
signals in separate subdirectories if you wish; read the NXT metadata
format documentation to see how.

-------------------------------------------------------------
WHAT'S IN THE ARCHIVE
-------------------------------------------------------------

TODO.txt, in CVS but not in the built public release,
contains the list of things that could be done to improve the
data set.

BUILD-INSTRUCTIONS.txt, in CVS but not in the built public release,
contains instructions about how the public release is built.

CVS-INSTRUCTIONS.txt, in CVS but not in the built public release,
contains some instructions about the CVS repository including where
the root of the CVS is.

EXAMPLE-QUERIES.txt contains a set of NXT queries that work on the
dialogue corpus plus their English glosses.  It is by no means
comprehensive, but is intended to give the new user some help starting
out.

maptask.sh is a shell script that can be run (on Linux or Mac OSX)
to get access to GUIS on the dialogue corpus (in the first instance, 
just the standardized GUIS configured for a few things). Use this 
shell script as an example of the classpath you need for other NXT 
uses to work.  Do not attempt to search the entire corpus using the 
GUI provided, because it is too large; use the search menu on any 
GUI for an individual dialogue, such as the named entity GUI, or 
use the command line.

maptask.bat is the same thing, but for Windows.

maptask-wordlists.sh is a shell script (on Linux or Mac OSX) that can 
be run to get access to a GUI on the wordlist corpus.  You can either 
use the generic GUI or the named entity coder configured to code for 
whether citations are first/second/third mentions.

maptask-wordlists.bat is the same thing, but for Windows.

Data and its subdirectories contains the data plus the configuration
file and code for rendering textual transcription for NXT's
configurable GUIs (in the configuration subdirectory).

src contains the source code for two java files that are required to
run the graphical user interfaces in NXT for this corpus.   

lib, which is in the built public release but not in the CVS, contains 
compiled versions of the two java files from the src directory.  They
can be recreated using the commands

java -d ./lib ./src/MaptaskTranscriptionToTextDelegate.java
java -d ./lib ./src/MaptaskWordListTranscriptionToTextDelegate.java

from the top level directory.

transforms, which is in the CVS but not in the built public release, 
contains  some scripts that were used to create this version
of the data.  This is not a fully documented process,
but the scripts are here as examples of processing for other needs
we might have later.

------------------------------------------------------
USING THE TWO CORPORA TOGETHER
-----------------------------------------------------

If you treat the data as plain old XML, it is possible to link up the
two corpora, finding landmark references and citation forms that refer
to the same landmark.  If you are interested in the relationship
between running speech and citation forms, you can also consider
creating your own version of the metadata that for each type of
information contains the union of what is in the two metadata files,
since then if you load the "observations" corresponding to a dialogue
and the word lists for the two participants in it, you can use NXT
itself to look at the relationships between them.  However, in this
case, some observations will have dialogue data and some will have
wordlist data, which means running the same queries over all
observations will be inefficient, and you could get confused by zero
counts for queries for the wrong kind of observation. You can at
least find out which observations are which by using regular expressions
on the observation name, which is available to the query language
as the "obs" attribute on all tags.  We do not ship
the corpus this way because it's quite a specialist concern and
because it would be more confusing for most users.

-----------------------------
SOUND FILES 
------------------------------

NXT can't work with the original sound files as on the Map Task Corpus
CDs. 

Assuming a particular mount point for the CDs, you can make the
sound files NXT requires for the main, dialogue corpus as follows:

cat /group/corpora/public/maptask/original/maptask_1_of_8/q1/e/c1/q1ec1.nst 
/group/corpora/public/maptask/original/maptask_1_of_8/q1/e/c1/q1ec1.ses > q1ec1.sph

sox q1ec1.sph q1ec1.wav
mv q1ec1.wav q1ec1.mix.wav

To create one citation sound file, 

cat /group/corpora/public/maptask/original/maptask_1_of_8/q1/e/wordlist/q1eta1w.nst /group/corpora/public/maptask/original/maptask_1_of_8/q1/e/wordlist/q1eta1w.ses > q1eta1w.sph

sox q1eta1w.sph q1eta1w.wav
mv q1eta1w.wav q1eta1.wordlist.wav

You can either use these commands to create sound files for use
in the interface using the CDs, or download the sound files in this
format from http://www.hcrc.ed.ac.uk/maptask.

If you have trouble playing the sound from within NXT, 
your metadata files probably aren't finding the files correctly.
The <signal> declarations give the path to sound files and specifies
the expected filenames (observation name + "." + specified signal name + "."
+ specified file extension).  

------------------------------
CAVEAT ABOUT MAIN CORPUS STRUCTURE
-----------------------------

In this version of the corpus, our arrangement for tokens, timed
units, and pos tags (tw) violate the NXT data model.  

In many corpora, there is a problem about what to do with words
like "there's", where the timings go with the entire unit, but
it needs further splitting (e.g. into "there" and "+s") for 
some operations, like part-of-speech tagging.

In this corpus, <tu> is a timed unit like "there's", and <token> 
is for the "there" and "+s".  The current version keeps timed
units in one file.  The tokens are represented in a separate
file that mixes <tuseq> and <token> elements - the <tuseq> elements
draw <tu>s as children, using them as they occur in the tu files.
This means that either the tu or the token
file can be used to get a complete version of the words in the data.
<tw> tags contain part-of-speech tags, which use tokens (from the
tokens files) as children where they exist, and tu's (from the
tu files) where they do not.  This is illegal, since in NXT
a tag (plus any other tags in its layer) must draw children from
exactly one other layer, not a choice of two. This can confuse
the lazy loading, because the metadata declares that the children
are in the layer holding the tus - which means that the lazy loading
need not bother to load the tokens files to find the children.

A more correct representation would be to define <token> and <tu> as
occuring in the same recursive layer, and change the file structure so
that the tus contain their corresponding tokens as children. This
doesn't make clear that tu's contain tokens rather than the other way
around, but it does mean that the part of speech tags can use either
as children.  However, even this has its problems.  At present, both
tus and tokens have textual content.  In NXT's data model, no element
can have both children and textual content.  (Strictly speaking,
elements of a given type should be defined as having either children
or textual content, not both, and every element of that type should
conform to the definition, but we aren't sure violating this has any
ill effects.)  We could erase the textual content on tus that contain
tokens, or we could move the textual content into attributes, which
have no restrictions, but either choice requires more care to make the
interfaces behave, since then we would have to specify how to display
these elements in GUIs. NXT doesn't implement content inheritance by
concatenating the content of children in order, although some
developers and users think it should.  Getting to a representation
that has tokens as within-file children of tus isn't hard, but it is
non-trivial because there can be two tokenized tus in a row, and
nothing but the textual content gives us any hint as to where to split
the sequence of tokens to match the sequence of tus.  If we do make
this change, then some queries about these tags will also change.

------------------------------
CAVEAT ABOUT GAZE CODING
-----------------------------

The gaze coding as present in the public release clearly does not 
conform to NXT's data model.  NXT assumes that tags of the same
type for the same speaker do not overlap, but it's clear that they do
- to see this, run the command line call

java CountQueryResults -c maptask.xml -q '($l look)($m look):($l@who == $m@who)&& ($l@who="f") && (END($l) > START($m)) && (START($l) < START($m))' 

Correspondence with Ellen Bard suggests that the overlap in the gaze
coding is deliberate, and that the meaning is explained in a paper that 
she wrote jointly with Anne H. Anderson that is on the topic of second 
mentions.  We have not had time to consider what the coding is meant
to mean and what effect the data model violation might have on use
of this part of the data.  We still consider this data worth releasing
(especially for users with access to the videos) because we think cleaning
it up is a relatively minor effort.


---------------------
VIDEOS
---------------------

There are videos for the corpus, as explained on the website at
http://www.hcrc.ed.ac.uk/maptask.  They can be made available for
research use as long as any screenshots in papers or video clips shown
obscure the subjects' faces.  We have a DVD that contains quads 3 and
4, eye contact only, in MPEG format; we have clipped two of the dialogues
to the correct length just to see how that can be done.  TODO.txt (in 
the CVS repository) explains how that works.  Clipping takes around
20 minutes per dialogue the way we've been doing it; we intend to leave
this work for the first person who needs them, and to ask them to contribute
the clipped videos back.  There are recordings for other quads on VHS tape;
they would need converted to a digital format before use.


