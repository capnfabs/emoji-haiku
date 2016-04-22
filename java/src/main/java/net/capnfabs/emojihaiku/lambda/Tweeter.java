package net.capnfabs.emojihaiku.lambda;

import net.capnfabs.emojihaiku.Generator;
import net.capnfabs.emojihaiku.Util;
import org.apache.commons.lang3.tuple.Pair;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.api.TweetsResources;

import java.io.IOException;

/**
 * Lambda function to post tweets to the account configured in twitter4j.properties.
 */
public class Tweeter {

  private final Generator generator;
  private final TweetsResources tweets;

  public Tweeter() {
    try {
      generator = Util.createGenerator();
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
    tweets = TwitterFactory.getSingleton().tweets();
  }

  public void Tweet() {
    Pair<String, String> haiku = generator.generatePoem(new int[]{5, 7, 5});
    try {
      tweets.updateStatus(String.format("%s\n%s", haiku.getLeft(), haiku.getRight()));
    } catch (TwitterException e) {
      throw new RuntimeException(e);
    }
  }
}
