package net.capnfabs.emojihaiku;

import net.capnfabs.emojihaiku.datamodel.EmojiDescriptionSyllableCount;
import org.apache.commons.lang3.tuple.Pair;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Generates patterns of random emojis based on syllable counts.
 */
public class Generator {

  private final Random random;
  private final List<List<EmojiDescriptionSyllableCount>> table;

  public Generator(Random random, List<List<EmojiDescriptionSyllableCount>> table) {
    this.random = random;
    this.table = table;
  }

  /**
   * Returns a pair, where the left element is the set of emoji comprising this line, and the right
   * element is the descriptions corresponding to these emoji.
   */
  public Pair<String, String> generateLine(int syllableCount) {
    List<String> emojis = new ArrayList<>();
    List<String> descriptions = new ArrayList<>();
    for (int budget = syllableCount; budget > 0; ) {
      // Selection Space is all emoji with a syllable count equal to or less than the remaining
      // budget.
      List<EmojiDescriptionSyllableCount> selectionSpace = table.get(budget);
      // Choose an emoji at random
      EmojiDescriptionSyllableCount emoji = selectionSpace.get(random.nextInt(selectionSpace.size()));
      emojis.add(emoji.emoji.emojiChar);
      descriptions.add(emoji.description.toUpperCase());
      budget -= emoji.syllableCount;
    }
    return Pair.of(String.join(" ", emojis), String.join(" ", descriptions));
  }

  public Pair<List<String>, List<String>> generateLines(int[] syllableCount) {
    ArrayList<String> emojis = new ArrayList<>();
    ArrayList<String> descriptions = new ArrayList<>();
    for (int syllables : syllableCount) {
      Pair<String, String> p = generateLine(syllables);
      emojis.add(p.getLeft());
      descriptions.add(p.getRight());
    }
    return Pair.of(emojis, descriptions);
  }

  public Pair<String, String> generatePoem(int[] syllableCount) {
    Pair<List<String>, List<String>> poem = generateLines(syllableCount);
    return Pair.of(String.join("\n", poem.getLeft()), String.join("\n", poem.getRight()));

  }
}
