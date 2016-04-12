package net.capnfabs.emojihaiku;

import net.capnfabs.emojihaiku.datamodel.EmojiDescriptionSyllableCount;
import net.capnfabs.emojihaiku.datamodel.EmojiEntry;
import net.capnfabs.emojihaiku.datamodel.SyllableEntry;

import java.io.IOException;
import java.util.List;
import java.util.Random;

public class Util {
  public static Generator createGenerator() throws IOException {
    EmojiEntry[] emojiEntries =
        DataProducer.loadJson("emoji.json", EmojiEntry[].class);
    SyllableEntry[] syllableEntries =
        DataProducer.loadJson("syllablecount.json", SyllableEntry[].class);
    List<List<EmojiDescriptionSyllableCount>> table =
        DataProducer.buildCumulativeSyllableTable(
            DataProducer.buildEmojiBySyllableCountTable(emojiEntries, syllableEntries));
    return new Generator(new Random(), table);
  }
}
