from descriptions import merged_results

from emoji import make_data


def main() -> None:
    emoji_list, modifiers = make_data()

    descriptions = {e.emoji: e for e in merged_results()}
    emoji_dict = {e.base_char: e for e in emoji_list}

    for emoji in emoji_dict.keys() ^ descriptions.keys():
        src = emoji in emoji_dict
        cldr = emoji in descriptions
        desc = descriptions[emoji].description if cldr else ""
        print(f'{emoji}\tsrc={src}\tcldr={cldr}\tdesc={desc}')


if __name__ == "__main__":
    main()
