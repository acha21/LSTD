This directory contains syntax files that have not been added
to the formal NXT data set. 

The annnotations are early-1990's automatic syntax, and so we
have judged that making the transform to NXT format is not 
worthwhile.

If we were to do the transform, it would need to be defined as
an agent-coding in maptask.xml.  In addition:

(1) We need to check whether the starts and durations are the same
as what one would get by inheritance, and remove if they are, or
push them aside into unofficial attributes (not the NXT start and
end times) if not.  The way to do this is to push and use NXT to
test.

(2) The summaries don't belong in the main
syntax files because they aren't time-aligned, and they probably
serve no purpose. (If we can't figure out what something means,
no point in working on it so we can distribute it even if we
distribute the syntax).  
