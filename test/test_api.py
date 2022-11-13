"""Unit tests for the package."""
from typing import List

import pytest
from steamship import Block, File
from steamship.plugin.inputs.block_and_tag_plugin_input import \
    BlockAndTagPluginInput
from steamship.plugin.request import PluginRequest

from api import CEDictTaggerPlugin


def req(text: str):
    # client = Steamship()
    app = CEDictTaggerPlugin(client=None)
    response = app.run(PluginRequest(data=BlockAndTagPluginInput(file=File(blocks=[Block(text=text)]))))
    return response

@pytest.mark.parametrize("text,expected", [
    ("請給我一個大餅", ["請", "給", "我", "一", "個", "大餅"]),
    ("请给我一个大饼", ["请", "给", "我", "一", "个", "大饼"])
])
def test_detect_language(text: str, expected: List[str]):
    """Test the app like a regular Python object."""
    out = req(text)
    assert out.file
    assert out.file.blocks

    block = out.file.blocks[0]

    assert block.tags
    assert len(block.tags) == len(expected)

    for tag in block.tags:
        print(tag.value)
        assert tag.kind == "token"
        assert tag.name == "ce-dict"
        assert tag.value
        assert tag.value.get('en')
        assert tag.value.get('trad')
        assert tag.value.get('simp')
        assert tag.value.get('pynum')
        assert isinstance(tag.value.get('pynum'), list)
        assert tag.value.get('pyacc')
        assert isinstance(tag.value.get('pyacc'), list)
        assert tag.value.get('zhuyin')
        assert isinstance(tag.value.get('zhuyin'), list)

    simps = [''.join(tag.value.get('simp')) for tag in block.tags]
    trads = [''.join(tag.value.get('trad')) for tag in block.tags]

    assert expected == simps or expected == trads

def test_suffix_edge_case():
    """Test the app like a regular Python object."""
    out = req("你好")
    assert out.file
    assert out.file.blocks

    block = out.file.blocks[0]

    assert block.tags
    assert len(block.tags) == 1

    for tag in block.tags:
        assert tag.kind == "token"
        assert tag.name == "ce-dict"
        assert tag.value
        assert tag.value.get('en')
        assert tag.value.get('trad')
        assert tag.value.get('simp')
        assert tag.value.get('pynum')
        assert isinstance(tag.value.get('pynum'), list)
        assert len(tag.value.get('pynum')) == 2

def test_prefix_failure():
    text = """參議院是上議院，有 100個席位，美國 50 個州，無論大小，各有兩名參議員代表本州。

參議員任期六年，每兩年有三分之一的參議院議員面臨競選連任。

眾議院有 435 個議席，每位眾議員代表各自所在州的一個特定選區，任期兩年。

中期選舉包括所有眾議員議席。
    """
    out = req(text)
    assert out.file
    assert out.file.blocks

    block = out.file.blocks[0]

    tag = block.tags[0]
    assert tag.start_idx == 0
    assert tag.end_idx == 3

def test_bread():
    text = "我喜歡麵包"
    out = req(text)
    assert out.file
    assert out.file.blocks

    assert len(out.file.blocks) == 1
    block = out.file.blocks[0]

    tags =  block.tags
    assert len(tags) == 3

    wo = tags[0]
    xihuan = tags[1]
    mianbao = tags[2]

    assert wo.start_idx == 0
    assert wo.end_idx == 1
    assert xihuan.start_idx == 1
    assert xihuan.end_idx == 3
    assert mianbao.start_idx == 3
    assert mianbao.end_idx == 5
