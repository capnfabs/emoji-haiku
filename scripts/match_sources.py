from emoji import descriptions
from emoji.spec_parser import load_emoji_and_modifiers


def main() -> None:
    emoji_list, modifiers = load_emoji_and_modifiers()

    d = {e.emoji: e for e in descriptions.extract_emoji_pairs()}
    emoji_dict = {e.base_char: e for e in emoji_list}

    for emoji in sorted(emoji_dict.keys() ^ d.keys()):
        src = emoji in emoji_dict
        cldr = emoji in d
        desc = d[emoji].description if cldr else ""
        print(f'{emoji}\tsrc={src}\tcldr={cldr}\tdesc={desc}')


if __name__ == "__main__":
    main()
