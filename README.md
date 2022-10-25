# CEDict Tagger Plugin - Steamship

This project contains a Steamship Tagger plugin that applies CEDict to a span of Mandarin Text.

## Output

The output is tags with:

* `kind`    - `token`
* `name` - `ce-dict`
* `value`     - A CE-Dict object, as defined below

The CE-Dict object represents the following with respect to the tagged text:

* `en` - English translation
* `trad` - Traditional characters
* `simp` - Simplified characters
* `pynum` - Pinyin (numeric style)
* `pyacc` - Pinyin (accent style)
* `zhuyin` - Zhuyin (bopomofo)

## Algorithm

A best-effort is made to match:

* The first entry in CEDict among competing alternatives
* The longest contiguous chunk of text, in greedy-search fashion

That approach certainly falls short whereas translation of meaning is concerned, 
but should fare well where word lookup and tokenization is concerned.



