package net.capnfabs.emojihaiku.datamodel;

import com.google.gson.annotations.SerializedName;

public class EmojiEntry {
  @SerializedName("emoji")
  public String emojiChar;
  public String[] descriptions;
  public String[] tags;
  public int year;
  @SerializedName("disp_mode")
  public String displayMode;
}
