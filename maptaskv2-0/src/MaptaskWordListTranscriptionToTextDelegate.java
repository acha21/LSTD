/**
 * Natural Interactivity Tools Engineering
 * Copyright (c) 2004, Jean Carletta, Jonathan Kilgour, Natasa Jovanovic, Dennis Reidsma
 * See the README file in this distribution for licence.
 */

import net.sourceforge.nite.gui.transcriptionviewer.*;
import net.sourceforge.nite.nom.nomwrite.*;

import java.util.Iterator;
import java.util.List;


/**
 * A very simple delegate made especially for the Maptask corpus. See interface documentation for moreinfo.
 * <p>
 * @author Dennis Reidsma, UTwente  Jean Carletta, University of Edinburgh
 */
public class MaptaskWordListTranscriptionToTextDelegate implements TranscriptionToTextDelegate {
    private final String WORD="wl-tu";

    /**
     * Return a string representation for the given element from a transcription layer.
     */
    public String getTextForTranscriptionElement(NOMElement nme) {
	String name = nme.getName();
        // This code should just take the text content - there are no children.
	if (name.equalsIgnoreCase(WORD)) {
	    List kids=nme.getChildren();
	    String content="";
	    if (kids==null) {
		content = nme.getText();
		if (content==null) { return ""; }
		return content.trim();
	    } else {
 		return "";
	    }
        }
	/* 
	  return "[" + (String)nme.getAttributeComparableValue('type') + "]";
	*/
	else { 
	    return "[" + name + "]";
	}
    }
}
