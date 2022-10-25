
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

def test_trie_search_hit_prefix():
    trie = CeDictTrie.load()

    from_trad = trie.tokenize('你好！這是我的名字。')

    print(from_trad)







def test_trie_search_prefix():
    trie = CeDictTrie.load()

    tags = tag_text('動物園', trie)
    for tag in tags:
        print(tag)


    # long_word = get_exact(trie, '動物園')
    # assert long_word
    #
    # prefix_also_word = get_exact(trie, '動物')
    # assert prefix_also_word
    #
    # items = get_all(trie, '動物')
    # print(items)
