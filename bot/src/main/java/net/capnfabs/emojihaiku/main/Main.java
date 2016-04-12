package net.capnfabs.emojihaiku.main;

import net.capnfabs.emojihaiku.Generator;
import net.capnfabs.emojihaiku.Util;
import org.apache.commons.lang3.tuple.Pair;

import java.io.IOException;

/**
 * Entry point for command-line utility.
 */
public class Main {
  public static void main(String[] args) {
    try {
      Generator generator = Util.createGenerator();
      Pair<String, String> poem = generator.generatePoem(new int[]{5, 7, 5});
      System.out.println( poem.getLeft() + "\n" + poem.getRight());
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}
