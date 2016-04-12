package net.capnfabs.emojihaiku.datamodel;

/**
 * A triple of emoji database item, a specific description from that item, and the syllable count of
 * that description.
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
