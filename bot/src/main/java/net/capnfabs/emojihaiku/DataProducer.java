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
 * Created by fabian on 12/04/2016.
 */
public class DataProducer {

    public static final String NOT_LETTERS_REGEX = "[^A-Za-z]";

    public static <T> T loadJson(File json, Class<T> clazz) throws FileNotFoundException, IOException {
        try (FileInputStream inputStream = new FileInputStream(json)) {
            Gson gson = new Gson();
            JsonReader jsonReader = gson.newJsonReader(new InputStreamReader(inputStream));
            return gson.fromJson(jsonReader, clazz);
        }
    }


    public static List<List<EmojiDescriptionSyllableCount>> buildEmojiBySyllableCountTable(EmojiEntry[] emojiEntries, SyllableEntry[] syllableEntries) {
        Map<String, Integer> syllablesByWord = Arrays.stream(syllableEntries).collect(
                Collectors.toMap(
                        s -> s.word,
                        s -> s.numSyllables));
        Map<Integer, List<EmojiDescriptionSyllableCount>> set = new HashMap<>();
        for (EmojiEntry emoji : emojiEntries) {
            for (String description : emoji.descriptions) {
                int syllables;
                try {
                    syllables = countSyllables(syllablesByWord, description);
                } catch (NotFoundException e) {
                    continue;
                }
                List<EmojiDescriptionSyllableCount> list = set.get(syllables);
                if (list == null) {
                    list = new ArrayList<>();
                    set.put(syllables, list);
                }
                list.add(new EmojiDescriptionSyllableCount(emoji, description, syllables));
            }
        }
        int max = set.keySet().stream().max(Integer::compare).get();
        List<List<EmojiDescriptionSyllableCount>> list = new ArrayList<>();
        list.add(Collections.emptyList());
        for (int i = 1; i <= max; i++) {
            ArrayList<EmojiDescriptionSyllableCount> thisEntry = new ArrayList<>();
            if (set.containsKey(i)) {
                thisEntry.addAll(set.get(i));
            }
            thisEntry.addAll(list.get(i-1));
            list.add(i, thisEntry);
        }
        return list;
    }

    public static int countSyllables(Map<String, Integer> syllablesByWord, String description) throws NotFoundException {
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

    static class NotFoundException extends Exception {}
}
