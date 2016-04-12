package net.capnfabs.emojihaiku;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Created by fabian on 12/04/2016.
 */
public class Main {
    public static void main(String[] args) {
        try {
            EmojiEntry[] emojiEntries = DataProducer.loadJson(new File("../datasources/emoji.json"), EmojiEntry[].class);
            SyllableEntry[] syllableEntries = DataProducer.loadJson(new File("../datasources/syllablecount.json"), SyllableEntry[].class);
            List<List<EmojiDescriptionSyllableCount>> lists = DataProducer.buildEmojiBySyllableCountTable(emojiEntries, syllableEntries);
            Random random = new Random();
            ArrayList<String> emojis = new ArrayList<>();
            ArrayList<String> descriptions = new ArrayList<>();
            for (int syllables : new int[]{5,7,5}) {
                Pair<String, String> p = generateLine(random, lists, syllables);
                emojis.add(p.first);
                descriptions.add(p.second);
            }
            System.out.println(String.join("\n", emojis) + "\n" + String.join("\n", descriptions));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static class Pair<F, S> {
        private final F first;
        private final S second;

        public Pair(F first, S second) {
            this.first = first;
            this.second = second;
        }
    }

    public static Pair<String,String>  generateLine(Random random, List<List<EmojiDescriptionSyllableCount>> table, int syllableCount) {
        List<String> emojis = new ArrayList<>();
        List<String> descriptions = new ArrayList<>();
        for (int i = syllableCount; i > 0; ) {
            // Choose an emoji at random
            List<EmojiDescriptionSyllableCount> selectionSpace = table.get(i);
            EmojiDescriptionSyllableCount emoji = selectionSpace.get(random.nextInt(selectionSpace.size()));
            emojis.add(emoji.emoji.emojiChar);
            descriptions.add(emoji.description);
            i -= emoji.syllableCount;
        }
        return new Pair<>(String.join(" ", emojis), String.join(" ", descriptions));
    }
}
