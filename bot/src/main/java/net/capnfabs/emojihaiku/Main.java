package net.capnfabs.emojihaiku;

import org.apache.commons.lang3.tuple.Pair;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Entry point for command-line utility.
 */
public class Main {
  public static void main(String[] args) {
    try {
      EmojiEntry[] emojiEntries =
          DataProducer.loadJson(new File("../datasources/emoji.json"), EmojiEntry[].class);
      SyllableEntry[] syllableEntries = DataProducer.loadJson(
              new File("../datasources/syllablecount.json"), SyllableEntry[].class);
      List<List<EmojiDescriptionSyllableCount>> table =
          DataProducer.buildCumulativeSyllableTable(
              DataProducer.buildEmojiBySyllableCountTable(emojiEntries, syllableEntries));
      Generator generator = new Generator(new Random(), table);
      Pair<String, String> poem = generator.generatePoem(new int[]{5, 7, 5});
      System.out.println( poem.getLeft() + "\n" + poem.getRight());
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}
