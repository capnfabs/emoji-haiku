"""Super lightweight emoji library."""

from typing import NamedTuple, Tuple, Dict, Set, Iterable, Optional, List
import os.path
from collections import defaultdict
import random

CodePoint = int
UnicodeClass = str

# Append these to a string to force text / emoji display.
TEXT_PRESENTATION_SELECTOR = '\uFE0E'
EMOJI_PRESENTATION_SELECTOR = '\uFE0F'

class CodePointInfo(NamedTuple):
    classes: Set[UnicodeClass]
    comments: Set[str]

Modifier = str

def makeCPI() -> CodePointInfo:
    return CodePointInfo(set(), set())

class Emoji:
    def __init__(self, codepoint: int, defaults_to_text: bool, supports_modification: bool):
        self.codepoint = codepoint
        self.base_char = chr(codepoint)
        
        # TODO this doesn't belong here.

        self.defaults_to_text = defaults_to_text
        self.supports_modification = supports_modification


    def char(self, modifier:Modifier = None) -> str:
        if modifier:
            # As per spec:
            # > Emoji presentation selectors are neither needed nor recommended for emoji characters when they are followed by emoji modifiers, and should not be used in newly generated emoji modifier sequences; the emoji modifier automatically implies the emoji presentation style.
            return self.base_char + modifier
        
        if self.defaults_to_text:
            # If you want to validate that this is an actual thing, the datasource for this is in emoji-variation-sequences.txt.
            return self.base_char + EMOJI_PRESENTATION_SELECTOR
        
        return self.base_char

    def __repr__(self) -> str:
        return f'Emoji(codepoint={hex(self.codepoint)}, defaults_to_text={self.defaults_to_text}, supports_modification={self.supports_modification})'


class DataWhatsit:
    def __init__(self, data_directory: str):
        self.data_directory = data_directory
    
    def load_codepoints(self) -> Dict[CodePoint, CodePointInfo]:
        merp: Dict[CodePoint, CodePointInfo] = defaultdict(makeCPI)
        for codepoint_or_range, codepoint_class, comment in self._scan_codepoints_file():
            if '..' in codepoint_or_range:
                start, end = codepoint_or_range.split('..')
            else:
                start = end = codepoint_or_range

            for codepoint in range(int(start, base=16), int(end, base=16) + 1):
                merp[codepoint].classes.add(codepoint_class)
                if comment:
                    merp[codepoint].comments.add(comment)
        return merp


    def _scan_codepoints_file(self) -> Iterable[Tuple[str,str, Optional[str]]]:
        path = os.path.join(self.data_directory, 'emoji-data.txt')
        with open(path, 'r') as file:
            # NOTE(fabian): I thought about using CSV for this, but decided against it because of 
            # the fact that the file structure has comments with # at the end. If you _did_ want
            # to change this to CSV, I'd probably do it by wrapping `file` with something that stripped
            # comments.
            for line in file:
                line, comment = self._remove_comment(line)
                if not line:
                    # It was just a comment, continue
                    continue
            
                fields = [field.strip() for field in line.split(';')]
                #print('Fields:', fields)
                #print('Comment: ', comment)
                assert len(fields) == 2
                # Codepoint or range, class
                yield fields[0], fields[1], comment

    def _remove_comment(self, line: str) -> Tuple[str, Optional[str]]:
        """Returns: [data-part of line] [comment]"""
        vals = line.split('#', maxsplit=1)
        if len(vals) == 1:
            # There is no comment if there is one element
            return vals[0].strip(), None
        else:
            return vals[0].strip(), vals[1].strip()

def make_data() -> Tuple[List[Emoji], List[Modifier]]:
    whatsit = DataWhatsit(data_directory='datasources/emoji-unicode-11/')
    emojis: List[Emoji] = []
    modifiers: List[Modifier] = []
    for k, v in whatsit.load_codepoints().items():
        if (v.classes & {'Emoji', 'Emoji_Component'}) == {'Emoji'}:
            modifiable = 'Emoji_Modifier_Base' in v.classes
            defaults_to_text = 'Emoji_Presentation' not in v.classes
            emojis.append(Emoji(k, defaults_to_text, modifiable))
        elif (v.classes & {'Emoji', 'Emoji_Modifier'}) == {'Emoji', 'Emoji_Modifier'}:
            # it's a modifier!
            print('Modifier!', hex(k), chr(k), v.classes)
            modifiers.append(chr(k))
    return emojis, modifiers

def yield_swatch_chars(emoji: List[Emoji], mods: List[Modifier]) -> Iterable[str]:
    emoji, mods = make_data()
    for e in emoji:
        if e.supports_modification:
            modifier = random.choice(mods)
            yield e.char(modifier=modifier)
        else:
            pass
            #yield e.char()


def main() -> None:
    emoji, mods = make_data()
    e = next(e for e in emoji if e.supports_modification)
    print(e)
    print(e.char(modifier=mods[0]))
    print(e.char().encode('utf-8'))

    print(' '.join(yield_swatch_chars(emoji, mods)))

    

if __name__ == "__main__":
    main()
