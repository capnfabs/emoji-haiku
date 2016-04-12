package net.capnfabs.emojihaiku;

import com.google.gson.annotations.SerializedName;

/**
 * Created by fabian on 12/04/2016.
 */
public class EmojiEntry {
    @SerializedName("emoji")
    public String emojiChar;
    public String[] descriptions;
    public String[] tags;
    public int year;
    @SerializedName("disp_mode")
    public String displayMode;
}
