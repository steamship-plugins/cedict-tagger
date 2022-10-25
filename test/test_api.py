# """Unit tests for the package."""
# from typing import List, Optional
#
# import pytest
# from steamship import Steamship
#
# from api import TokenizeCjk, Language
#
# @pytest.mark.parametrize("text,expected", [
#     ("請給我一個大餅", Language.MANDARIN_TRADITIONAL.value),
#     ("请给我一个大饼", Language.MANDARIN_SIMPLIFIED.value),
#     ("こんにちは", Language.JAPANESE.value),
# ])
# def test_detect_language(text: str, expected: str):
#     """Test the app like a regular Python object."""
#     client = Steamship()
#     app = TokenizeCjk(client=client)
#     response = app.detect_language(text)
#     predicted = response.data.get("language")
#     assert predicted == expected
#
#
# @pytest.mark.parametrize("input,into,expected", [
#     ("請給我一個大餅", Language.MANDARIN_TRADITIONAL, "請給我一個大餅"),
#     ("請給我一個大餅", Language.MANDARIN_SIMPLIFIED, "请给我一个大饼"),
#     ("请给我一个大饼", Language.MANDARIN_TRADITIONAL, "請給我一個大餅"),
#     ("请给我一个大饼", Language.MANDARIN_SIMPLIFIED, "请给我一个大饼"),
# ])
# def test_convert_variant(input: str, into: Language, expected: str):
#     """Test the app like a regular Python object."""
#     client = Steamship()
#     app = TokenizeCjk(client=client)
#     response = app.convert_variant(input, into=into.value)
#     predicted = response.data.get("text")
#     assert predicted == expected
#
# @pytest.mark.parametrize("input,expected", [
#     ("こんにちは", ["こんにちは"])
# ])
# def test_tokenize_japanese(input: str, expected: List[str]):
#     """Test the app like a regular Python object."""
#     client = Steamship()
#     app = TokenizeCjk(client=client)
#     response = app.tokenize_japanese(input)
#     predicted = response.data.get("tokens", [])
#     tokens = [token.get("text") for token in predicted]
#     assert tokens == expected
#
# @pytest.mark.parametrize("input,expected", [
#     # ("請給我一個大餅", ["請", "給", "我", "一", "個", "大", "餅"]),
#     # ("我是美國人", ["我", "是", "美國", "人"]),
#     ("你好！你叫什麼名字？", ["你好", "！", "你叫", "什麼", "名字", "？"]),
#     ("你好！你叫什么名字？", ["你好", "！", "你叫", "什么", "名字", "？"]),
#     # ("请给我一个大饼", ["请", "给", "我", "一", "个", "大", "饼"])
# ])
# def test_tokenize_mandarin(input: str, expected: List[str]):
#     """Test the app like a regular Python object."""
#     client = Steamship()
#     app = TokenizeCjk(client=client)
#     response = app.tokenize_japanese(input)
#     predicted = response.data.get("tokens", [])
#     tokens = [token.get("text") for token in predicted]
#     assert tokens == expected
#
# TRAD_TOKS = ["你好", "！", "你", "叫", "什麼", "名字", "？"]
# SIMP_TOKS = ["你好", "！", "你", "叫", "什么", "名字", "？"]
#
# @pytest.mark.parametrize("input,into,expected", [
#     ("你好！你叫什麼名字？", Language.MANDARIN_TRADITIONAL, TRAD_TOKS),
#     ("你好！你叫什麼名字？", Language.MANDARIN_SIMPLIFIED, SIMP_TOKS),
#     ("你好！你叫什麼名字？", None, TRAD_TOKS),
#     ("こんにちは", None, ["こんにちは"]),
#     ("你好！你叫什么名字？", Language.MANDARIN_TRADITIONAL, TRAD_TOKS),
#     ("你好！你叫什么名字？", Language.MANDARIN_SIMPLIFIED, SIMP_TOKS),
#     ("你好！你叫什么名字？", None, SIMP_TOKS),
# ])
# def test_tokenize(input: str, into: Optional[Language], expected: List[str]):
#     """Test the app like a regular Python object."""
#     client = Steamship()
#     app = TokenizeCjk(client=client)
#     response = app.tokenize(input, prefer_traditional=(into == Language.MANDARIN_TRADITIONAL))
#     predicted = response.data.get("tokens", [])
#     tokens = [token.get("text") for token in predicted]
#     assert tokens == expected
