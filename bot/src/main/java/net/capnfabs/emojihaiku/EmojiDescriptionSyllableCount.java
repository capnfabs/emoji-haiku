package net.capnfabs.emojihaiku;

/**
 * Created by fabian on 12/04/2016.
 */
public class EmojiDescriptionSyllableCount {
    public final EmojiEntry emoji;
    public final String description;
    public final int syllableCount;

    public EmojiDescriptionSyllableCount(EmojiEntry emoji, String description, int syllableCount) {
        this.emoji = emoji;
        this.description = description;
        this.syllableCount = syllableCount;
    }
}
