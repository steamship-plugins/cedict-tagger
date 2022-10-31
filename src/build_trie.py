"""Processes CEDict and builds the trie Structure to the source data.trie file."""
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

import dragonmapper.transcriptions
from cedict_utils.cedict import CedictEntry, CedictParser

from cedict_tagger import CeDictTrie, Entry

DATA_PATH = Path(__file__).parent.parent / 'data'
CEDICT_FILE = DATA_PATH / 'cedict_ts.u8'

@contextmanager
def _log_time(task_name: str):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"[{end - start: 2.2f}s ] {task_name}")

def _load_ce_dict():
    with _log_time("_load_ce_dict"):
        parser = CedictParser()
        parser.read_file(CEDICT_FILE.absolute())
        entries = parser.parse()
        return entries


U_FIXES = {
    'u:4': 'ǜ',
    'u:3': 'ǚ',
    'u:2': 'ǘ',
    'u:1': 'ǖ',
    'u:': 'ü',
    'u:e': 'üe',
    'u:e1': 'üe',
    'u:e2': 'üú',
    'u:e3': 'üě',
    'u:e4': 'üè',
}

FIXES = {
    'u:4': 'ǜ',
    'u:3': 'ǚ',
    'u:2': 'ǘ',
    'u:1': 'ǖ',
    'u:': 'ü',
    'yo1': 'yō',
    'yo5': 'yo',
    'o1': 'o1',
    'o2': 'o2',
    'o3': 'o3',
    'o4': 'o4',
}

for first in ['l', 'n', 'N', 'L']:
    for fix in U_FIXES:
        # This all feels very silly. Is numeric pinyin incapable of certain sounds?
        FIXES[f"{first}{fix}"] = f"{first}{U_FIXES[fix]}"

def _map_entry(entry: CedictEntry) -> Optional[Entry]:
    if not entry.meanings:
        return None

    pinyin = entry.pinyin

    parts = [part for part in pinyin.split(' ') if dragonmapper.transcriptions.is_pinyin(part)]
    parts = [FIXES.get(part, part) for part in parts]

    if not parts:
        return None

    fixed_pinyin = ' '.join(parts)

    try:
        zhuyin = dragonmapper.transcriptions.pinyin_to_zhuyin(fixed_pinyin).split(' ')
        pyacc = [dragonmapper.transcriptions.to_pinyin(s, True) for s in zhuyin]
        pinyin = [dragonmapper.transcriptions.to_pinyin(s, False) for s in zhuyin]
    except Exception as e:
        print(e)
        print(entry.traditional, entry.pinyin)
        return None

    assert len(zhuyin) == len(pyacc)
    assert len(pyacc) == len(pinyin)
    if len(pinyin) != len(entry.traditional):
        print(entry.traditional)
        print(entry.pinyin)
        # assert len(pinyin) == len(entry.traditional)

    print(entry.meanings[0])

    return Entry(
        en=entry.meanings[0],
        trad=entry.traditional,
        simp=entry.simplified,
        pynum=pinyin,
        pyacc=pyacc,
        zhuyin=zhuyin
    )


def _build_trie(cedict):
    with _log_time("_build_trie"):
        trie = CeDictTrie()
        for cedict_entry in cedict:
            entry = _map_entry(cedict_entry)
            if entry:
                trie.add_entry(entry)
        return trie

if __name__ == "__main__":
    print("Hello! Building dictionary file..")
    print("Reading CEDict...")
    print(dir(dragonmapper))
    cedict = _load_ce_dict()
    trie = _build_trie(cedict)
    trie.save()
