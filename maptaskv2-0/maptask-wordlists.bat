rem Note that a Java runtime should be on the path.
rem The current directory should be root of the Map Task distribution.
rem (what you get at the top level when you unzip it).
rem You must edit the local variable for the location of NXT
rem to be the path to the top level of the NXT distribution.
rem The preset value assumes you have unzipped NXT in the same location
rem as the Map Task distribution.
rem
rem This assumes that the metadata file for the maptask corpus
rem (a file called maptask.xml) is in the subdirectory called "Data".
rem You can change this assumption by changing the -corpus flag in
rem the Java call below.  The metadata file itself specifies where
rem to find the annotations and signals - search on "path" in it to
rem find the declarations.

@echo off

setlocal
NXT=.
classpath=.;./lib;Data/configuration;%NXT%;%NXT%/lib;%NXT%/lib/nxt.jar;%NXT%/lib/jdom.jar;%NXT%/fobs/jmf.jar;%NXT%/fobs/fobs4jmf.jar;%NXT%/lib/pnuts.jar;%NXT%/lib/resolver.jar;%NXT%/lib/xalan.jar;%NXT%/lib/xercesImpl.jar;%NXT%/lib/xml-apis.jar;%NXT%/lib/jmanual.jar;%NXT%/lib/jh.jar;%NXT%/lib/helpset.jar;%NXT%/lib/poi.jar;%NXT%/lib/eclipseicons.jar;%NXT%/lib/icons.jar;%NXT%/lib/forms-1.0.4.jar;%NXT%/lib/looks-1.2.2.jar;%NXT%/lib/necoderHelp.jar;%NXT%/lib/videolabelerHelp.jar;%NXT%/lib/dacoderHelp.jar;%NXT%/lib/testcoderHelp.jar;%NXT%/lib/parlevink.jar

java -Xms128m -Xmx1024m -cp %classpath$ net.sourceforge.nite.nxt.GUI -corpus Data/maptask-wordlists.xml

