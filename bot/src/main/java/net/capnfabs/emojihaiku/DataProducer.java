package net.capnfabs.emojihaiku;

import com.google.gson.Gson;
import com.google.gson.stream.JsonReader;
import net.capnfabs.emojihaiku.datamodel.EmojiDescriptionSyllableCount;
import net.capnfabs.emojihaiku.datamodel.EmojiEntry;
import net.capnfabs.emojihaiku.datamodel.SyllableEntry;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Functionality for processing input data.
 */
public class DataProducer {

  /**
   * Used to split words in unicode descriptions.
   * <p>
   * Everything except for letters, digits, and apostrophes gets in the way of our syllable
   * dictionary, so we split based on that.
   */
  private static final String NOT_LETTERS_REGEX = "[^A-Za-z'0-9]";
  private static final String BANNED_DESC_REGEX = "TYPE-\\d$";

  public static <T> T loadJsonFromResources(String resourcePath, Class<T> clazz)
      throws FileNotFoundException, IOException {
    ClassLoader classloader = Thread.currentThread().getContextClassLoader();
    try (InputStream inputStream = classloader.getResourceAsStream(resourcePath)) {
      Gson gson = new Gson();
      JsonReader jsonReader = gson.newJsonReader(
          new InputStreamReader(inputStream, Charset.forName("UTF-8")));
      return gson.fromJson(jsonReader, clazz);
    }
  }

  public static <T> T loadJsonFromFile(String resourcePath, Class<T> clazz)
      throws FileNotFoundException, IOException {
    try (InputStream inputStream = new FileInputStream(resourcePath)) {
      Gson gson = new Gson();
      JsonReader jsonReader = gson.newJsonReader(
          new InputStreamReader(inputStream, Charset.forName("UTF-8")));
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
      EmojiEntry[] emojiEntries, List<SyllableEntry> syllableEntries) {
    // TODO: Change EmojiEntry to something iterable, and then filter in a different method.
    Map<String, List<Integer>> syllablesByWord = mapSyllablesByWord(syllableEntries);
    Map<Integer, List<EmojiDescriptionSyllableCount>> table = new HashMap<>();
    for (EmojiEntry emoji : emojiEntries) {
      for (String description : emoji.descriptions) {
        if (description.matches(BANNED_DESC_REGEX)) {
          continue;
        }
        List<Integer> syllablesOptions;
        try {
          syllablesOptions = countSyllables(syllablesByWord, description);
        } catch (NotFoundException e) {
          continue;
        }
        for (int syllables : syllablesOptions) {
          List<EmojiDescriptionSyllableCount> list = table.get(syllables);
          if (list == null) {
            list = new ArrayList<>();
            table.put(syllables, list);
          }
          list.add(new EmojiDescriptionSyllableCount(emoji, description, syllables));
        }
      }
    }
    return table;
  }

  private static Map<String, List<Integer>> mapSyllablesByWord(List<SyllableEntry> syllableEntries) {
    Map<String, List<Integer>> map = new HashMap<>();
    for (SyllableEntry entry : syllableEntries) {
      List<Integer> syllables = map.get(entry.word);
      if (syllables == null) {
        syllables = new ArrayList<>();
        map.put(entry.word, syllables);
      }
      syllables.add(entry.numSyllables);
    }
    return map;
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
   * @return a list; there's often more than one way of pronouncing something.
   * @throws NotFoundException if one of the words in {@code description} couldn't be found.
   */
  public static List<Integer> countSyllables(
      Map<String, List<Integer>> syllablesByWord, String description) throws NotFoundException {
    String[] words = description.split(NOT_LETTERS_REGEX);
    Stream<Integer> options = Stream.of(0);
    for (String word : words) {
      if (word.isEmpty()) {
        continue;
      }
      String WORD = word.toUpperCase();
      List<Integer> syllables = syllablesByWord.get(WORD);
      if (syllables == null) {
        throw new NotFoundException();
      }
      options = options.map(c -> syllables.stream().map(v -> v + c)).flatMap(x -> x).distinct();
    }
    return options.collect(Collectors.toList());
  }

  static class NotFoundException extends Exception {
  }
}
