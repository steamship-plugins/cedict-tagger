import pickle
from collections import namedtuple
from pathlib import Path
from typing import Dict, List, Tuple

from steamship import SteamshipError

from trie import LongestMatchTree

THIS_PATH = Path(__file__).parent
TRIE_FILE = THIS_PATH / 'dict.trie'

Entry = namedtuple("Entry", [
    "en",
    "trad",
    "simp",
    "pynum",
    "pyacc",
    "zhuyin"
])

def entry_to_dict(entry: Entry) -> Dict:
    return {
        "en": entry.en,
        "trad": entry.trad,
        "simp": entry.simp,
        "pynum": entry.pynum,
        "pyacc": entry.pyacc,
        "zhuyin": entry.zhuyin,
    }


KEY_SPLIT = lambda word: "/".join([*word])
KEY_JOIN = lambda word: word.replace("/", "")

class CeDictTrie(LongestMatchTree):
    def __init__(self, trie = None):
        super().__init__(trie, key_fn=KEY_SPLIT)

    @staticmethod
    def load():
        if not TRIE_FILE.is_file():
            raise SteamshipError(message="Could not load trie data structure: file missing.")

        with open(TRIE_FILE, 'rb') as handle:
            trie = pickle.load(handle)
            return CeDictTrie(trie)

    def save(self):
        return super().save(TRIE_FILE)

    def add_entry(self, entry: Entry):
        # Want to avoid:
        # variant of...Entry(en='variant of 是[shi4]', trad='昰', simp='是', pynum='shi4', pyacc='shì', zhuyin='ㄕˋ'))
        # the old names
        if not self.get_exact(entry.trad):
            self.add(entry.trad, entry)
        if entry.simp != entry.trad:
            if not self.get_exact(entry.simp):
                self.add(entry.simp, entry)

    def tokenize(self, text: str) -> List[Tuple[int, int, Entry]]:
        start_i = 0
        end_i = 1

        tags = []

        while start_i < len(text):
            # Advance the window while we still have a subtree
            longest_exact_match = None
            longest_prefix_match = None

            still_matching = True
            while still_matching:
                still_matching = False
                if end_i > len(text):
                    break
                if self.has_key(text[start_i:end_i]):
                    still_matching = True
                    longest_exact_match = text[start_i:end_i]
                if self.has_node(text[start_i:end_i]):
                    still_matching = True
                    longest_prefix_match = text[start_i:end_i]
                if still_matching:
                    end_i += 1

            if not longest_exact_match and not longest_prefix_match:
                start_i += 1
                end_i = start_i + 1
                continue

            if longest_exact_match == longest_prefix_match or (longest_exact_match and not longest_prefix_match):
                # Easy!
                entry = self.get_exact(longest_exact_match)
                new_start = start_i + len(longest_exact_match)
                tag = (start_i, new_start, entry)
                start_i = new_start
                end_i = start_i + 1
                tags.append(tag)
                continue

            # See if we can find a preifx..

            longest_length = None
            longest_entry = None
            longest_entry_match = None

            for item in self.get_all(longest_prefix_match):
                try:
                    if text[start_i:].index(KEY_JOIN(item[0])) == 0:
                        length = len(item[0])
                        entry = item[1]

                        if longest_length is None or length >= longest_length:
                            longest_length = length
                            longest_entry = entry
                            longest_entry_match = KEY_JOIN(item[0])
                except ValueError:
                    pass

            # In case we got thrown on a wild goose chase because of a long phrase.
            if longest_entry is None and longest_exact_match is None:
                raise SteamshipError(message="Couldn't find prefix or exact match")

            entry = longest_entry or self.get_exact(longest_exact_match)
            query = longest_entry_match or longest_exact_match

            if not entry:
                raise SteamshipError(message="Couldn't find prefix or exact match - 2")

            new_start = start_i + len(query)
            tag = (start_i, new_start, entry)
            start_i = new_start
            end_i = start_i + 1
            tags.append(tag)

        return tags
