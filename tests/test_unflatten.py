# -*- coding: utf-8 -*-
import pytest

from unflatten import (
    unflatten,
    _parse_key,
    _unparse_key,
    DICT,
    LIST,
    )


@pytest.mark.parametrize('label, flattened, unflattened', [
    ('empty', (), {}),
    ('flat', {'a': 1, 'b': 2}, {'a': 1, 'b': 2}),
    ('array', {'a[0]': 1, 'a[1]': 'x'}, {'a': [1, 'x']}),
    ('duplicate-array-index',
     [
        ('a[0]', 'a0'),
        ('a[0]', 'a0-dup'),
        ],
     {'a': ['a0-dup']}),
    ('compex',
     [
        ('b', 'b'),
        ('a[0].b', 'a0b'),
        ('a[1].b', 'a1b'),
        ('a[1].c', 'a1c'),
        ],
     {'a': [
         {'b': 'a0b'},
         {'b': 'a1b', 'c': 'a1c'},
         ],
      'b': 'b',
      }),
    ])
def test_unflatten(label, flattened, unflattened):
    assert unflatten(flattened) == unflattened


def test_unflatten_missing_array_key():
    with pytest.raises(ValueError) as ctx:
        unflatten({'a[1]': 'a1'})
    assert str(ctx.value).startswith('missing')
    assert str(ctx.value).endswith('a[0]')


@pytest.mark.parametrize('keys', [
    ('a', 'a[0]'),
    ('a', 'a.b'),
    ('a.b', 'a[0]'),
    ('a', 'a.b', 'a[0]'),
    ])
def test_unflatten_mixed_node_types(keys):
    with pytest.raises(ValueError) as ctx:
        unflatten((key, 'val') for key in keys)
    assert str(ctx.value).startswith("mixture")


def test_unflatten_nonstring_key():
    with pytest.raises(TypeError) as ctx:
        assert unflatten([(42, 'val')])
    assert "must be strings" in str(ctx.value)


@pytest.mark.parametrize('key, parsed', [
    ('foo', ((DICT, 'foo'),)),
    ('foo.bar', ((DICT, 'foo'), (DICT, 'bar'))),
    ('foo[1]', ((DICT, 'foo'), (LIST, 1))),
    ('foo[1][2].bar', ((DICT, 'foo'), (LIST, 1), (LIST, 2), (DICT, 'bar'))),
    ])
class Test_parse(object):
    def test_parse_key(self, key, parsed):
        assert _parse_key(key) == parsed

    def test_unparse_key(self, key, parsed):
        assert _unparse_key(parsed) == key
