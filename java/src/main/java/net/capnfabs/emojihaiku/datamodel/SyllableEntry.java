package net.capnfabs.emojihaiku.datamodel;

import com.google.gson.annotations.SerializedName;

/** Represents a mapping from a word to a count of syllables for that word. */
public class SyllableEntry {
  public String word;

  @SerializedName("syllable_count")
  public int numSyllables;
}
