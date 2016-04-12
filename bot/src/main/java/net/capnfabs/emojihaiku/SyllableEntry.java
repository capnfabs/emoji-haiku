package net.capnfabs.emojihaiku;

import com.google.gson.annotations.SerializedName;

/**
 * Created by fabian on 12/04/2016.
 */
public class SyllableEntry {
    public String word;
    @SerializedName("syllable_count")
    public int numSyllables;
}
