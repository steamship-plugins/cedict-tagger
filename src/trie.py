import pickle
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple

import pygtrie
from steamship import SteamshipError

KEY_PRESERVE = lambda word: word

class LongestMatchTree():
    trie: pygtrie.StringTrie
    key_fn: Callable[[str], str]

    def __init__(
            self,
            trie: pygtrie.StringTrie = None,
            key_fn: Optional[Callable[[str], str]] = None
    ):
        if trie is None:
            self.trie = pygtrie.StringTrie()
        else:
            self.trie = trie
        if key_fn is None:
            self.key_fn = KEY_PRESERVE
        else:
            self.key_fn = key_fn

    @staticmethod
    def load(path: Path, key_fn: Optional[Callable[[str], str]] = None):
        if not path.is_file():
            raise SteamshipError(message="Could not load trie data structure: file missing.")

        with open(path, 'rb') as handle:
            trie = pickle.load(handle)
            return LongestMatchTree(trie, key_fn=key_fn)

    def save(self, path: Path):
        with open(path, 'wb') as handle:
            pickle.dump(self.trie, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def has_subtree(self, word: str) -> bool:
        return self.trie.has_subtrie(self.key_fn(word))

    def get_exact(self, word: str) -> Optional[Any]:
        keyed = self.key_fn(word)
        if keyed not in self.trie:
            return None
        return self.trie[keyed]

    def get_all(self, word: str) -> Optional[List[Tuple[str, Any]]]:
        return self.trie.items(prefix=self.key_fn(word))

    def add(self, key: str, value: Any):
        self.trie[self.key_fn(key)] = value

    def has_subtrie(self, key: str) -> bool:
        return self.trie.has_subtrie(self.key_fn(key))

    def has_key(self, key: str) -> bool:
        return self.trie.has_key(self.key_fn(key))

    def has_node(self, key: str) -> bool:
        return self.trie.has_node(self.key_fn(key))
