package net.capnfabs.emojihaiku.lambda;

import net.capnfabs.emojihaiku.Generator;
import net.capnfabs.emojihaiku.Util;
import org.apache.commons.lang3.tuple.Pair;

import java.io.IOException;

/**
 * AWS Lambda functions
 */
public class Lambda {

  public Lambda() {
    try {
      generator = Util.createGenerator();
    } catch (IOException e) {
      throw new RuntimeException();
    }
  }

  private final Generator generator;

  public static class EmojiResponse {
    public final String emoji;
    public final String descriptions;

    public EmojiResponse(String emoji, String descriptions) {
      this.emoji = emoji;
      this.descriptions = descriptions;
    }
  }

  public EmojiResponse haiku() throws IOException {
    Pair<String, String> p = generator.generatePoem(new int[]{5, 7, 5});
    return new EmojiResponse(p.getLeft(), p.getRight());
  }
}
