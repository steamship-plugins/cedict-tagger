
__copyright__ = "Steamship"
__license__ = "MIT"

from cedict_tagger import CeDictTrie


def test_trie_search_hit_trad():
    trie = CeDictTrie.load()

    from_trad = trie.get_exact('什麼')
    from_simp = trie.get_exact('什么')
    assert trie.get_exact('名字')

    assert from_trad
    assert from_simp

    assert from_trad == from_simp


def test_trie_search_miss_trad():
    trie = CeDictTrie.load()

    from_trad = trie.get_exact('麼名')
    from_simp = trie.get_exact('么名')

    assert from_trad is None
    assert from_simp is None

def test_trie_subtree():
    trie = CeDictTrie.load()
    assert trie.has_node('你')
    assert trie.has_node('你好')
    assert not trie.has_node('你好嗎')

# def test_trie_search_hit_prefix():
#     trie = CeDictTrie.load()
#
#     from_trad = trie.tokenize('你好！這是我的名字。')
