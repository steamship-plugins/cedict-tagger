import logging
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

    def should_skip(self, entry: Entry) -> bool:
        if "variant of" in entry.en:
            logging.info(f"[SKIP] Variant. Skip: {entry.en}")
            return True
        elif "surname" in entry.en:
            logging.info(f"[SKIP] Surname. Skip: {entry.en}")
            return True
        elif self.get_exact(entry.trad) is not None:
            logging.info(f"[SKIP] Exists. {entry.en} Existing: {self.get_exact(entry.trad).en}")
            return True
        return False

    def trim(self, entry: Entry):
        en = entry.en
        chars = ["[", ",", ";", "("]
        for char in chars:
            i = en.find(char)
            if i > 0:  # Skip the first one too
                logging.info(f"[TRIM] {char} - {en}")
                en = en[:i]
        return Entry(
            en,
            entry.trad,
            entry.simp,
            entry.pynum,
            entry.pyacc,
            entry.zhuyin,
        )


    def save(self):
        return super().save(TRIE_FILE)

    def add_entry(self, entry: Entry):
        # Want to avoid:
        # the old names
        if self.should_skip(entry):
            return
        entry = self.trim(entry)
        if not self.get_exact(entry.trad):
            self.add(entry.trad, entry)
        if entry.simp != entry.trad:
            if not self.get_exact(entry.simp):
                self.add(entry.simp, entry)

    def tokenize(self, text: str) -> List[Tuple[int, int, Entry]]:
        start_i = 0
        end_i = 1

        tags = []

        i = 0
        while i < len(text):
            longest_key, longest_value = self.get_longest_prefix(text[i:])
            if longest_key is None:
                i += 1
                # Advance
            else:
                tag = (i, i + len(longest_key), longest_value)
                tags.append(tag)
                i += len(longest_key)

        return tags
