package net.capnfabs.emojihaiku;

import com.google.gson.Gson;
import com.google.gson.stream.JsonReader;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Functionality for processing input data.
 */
public class DataProducer {

  /**
   * Used to split words in unicode descriptions.
   * <p>
   * Everything except for letters gets in the way of our syllable dictionary, so we split based
   * on that.
   */
  private static final String NOT_LETTERS_REGEX = "[^A-Za-z]";

  public static <T> T loadJson(File json, Class<T> clazz)
      throws FileNotFoundException, IOException {
    try (FileInputStream inputStream = new FileInputStream(json)) {
      Gson gson = new Gson();
      JsonReader jsonReader = gson.newJsonReader(new InputStreamReader(inputStream));
      return gson.fromJson(jsonReader, clazz);
    }
  }


  /**
   * Builds a map of syllable count / emoji description.
   * <p>
   * Note that there are multiple possible descriptions per emoji, so we return a {@link
   * EmojiDescriptionSyllableCount}s instead of {@link EmojiEntry EmojiEntries}.
   */
  public static Map<Integer, List<EmojiDescriptionSyllableCount>> buildEmojiBySyllableCountTable(
      EmojiEntry[] emojiEntries, SyllableEntry[] syllableEntries) {
    Map<String, Integer> syllablesByWord = Arrays.stream(syllableEntries).collect(
        Collectors.toMap(
            s -> s.word,
            s -> s.numSyllables));
    Map<Integer, List<EmojiDescriptionSyllableCount>> table = new HashMap<>();
    for (EmojiEntry emoji : emojiEntries) {
      for (String description : emoji.descriptions) {
        int syllables;
        try {
          syllables = countSyllables(syllablesByWord, description);
        } catch (NotFoundException e) {
          continue;
        }
        List<EmojiDescriptionSyllableCount> list = table.get(syllables);
        if (list == null) {
          list = new ArrayList<>();
          table.put(syllables, list);
        }
        list.add(new EmojiDescriptionSyllableCount(emoji, description, syllables));
      }
    }
    return table;
  }

  public static List<List<EmojiDescriptionSyllableCount>>
  buildCumulativeSyllableTable(Map<Integer, List<EmojiDescriptionSyllableCount>> table) {
    @SuppressWarnings("OptionalGetWithoutIsPresent")
    int max = table.keySet().stream().max(Integer::compare).get();

    List<List<EmojiDescriptionSyllableCount>> list = new ArrayList<>(max + 1);

    list.add(0, Collections.emptyList());
    for (int i = 1; i <= max; i++) {
      ArrayList<EmojiDescriptionSyllableCount> thisEntry = new ArrayList<>();
      if (table.containsKey(i)) {
        thisEntry.addAll(table.get(i));
      }
      thisEntry.addAll(list.get(i - 1));
      list.add(i, thisEntry);
    }
    return list;
  }

  /**
   * Counts the syllables in a word using the provided dictionary.
   * @throws NotFoundException if one of the words in {@code description} couldn't be found.
   */
  public static int countSyllables(
      Map<String, Integer> syllablesByWord, String description) throws NotFoundException {
    String[] words = description.split(NOT_LETTERS_REGEX);
    int count = 0;
    for (String word : words) {
      Integer syllables = syllablesByWord.get(word.toUpperCase());
      if (syllables == null) {
        throw new NotFoundException();
      }
      count += syllables;
    }
    return count;
  }

  static class NotFoundException extends Exception {
  }
}
