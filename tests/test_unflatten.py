# -*- coding: utf-8 -*-
from itertools import chain, permutations

import pytest

from unflatten import _parse_key, _unparse_key, unflatten


@pytest.mark.parametrize(
    "label, flattened, unflattened",
    [
        ("empty", (), {}),
        ("flat", {"a": 1, "b": 2}, {"a": 1, "b": 2}),
        ("array", {"a[0]": 1, "a[1]": "x"}, {"a": [1, "x"]}),
        (
            "duplicate-array-index",
            [
                ("a[0]", "a0"),
                ("a[0]", "a0-dup"),
            ],
            {"a": ["a0-dup"]},
        ),
        (
            "complex",
            [
                ("b", "b"),
                ("a[0].b", "a0b"),
                ("a[1].b", "a1b"),
                ("a[1].c", "a1c"),
            ],
            {
                "a": [
                    {"b": "a0b"},
                    {"b": "a1b", "c": "a1c"},
                ],
                "b": "b",
            },
        ),
        ("unicode", [("fü.baß", "x")], {"fü": {"baß": "x"}}),
    ],
)
def test_unflatten(label, flattened, unflattened):
    assert unflatten(flattened) == unflattened


def test_unflatten_missing_array_key():
    with pytest.raises(ValueError) as ctx:
        unflatten({"a[1]": "a1"})
    assert str(ctx.value).startswith("missing key")
    assert "a[0]" in str(ctx.value)


@pytest.mark.parametrize(
    "keys",
    chain.from_iterable(
        map(
            permutations,
            [
                ("a", "a[0]"),
                ("a", "a.b"),
                ("a.b", "a[0]"),
                ("a", "a.b", "a[0]"),
            ],
        )
    ),
    ids=repr,
)
def test_unflatten_mixed_node_types(keys):
    with pytest.raises(ValueError) as ctx:
        unflatten((key, {"val_for_key": key}) for key in keys)
    assert str(ctx.value).startswith("conflicting types")


def test_unflatten_nonstring_key():
    with pytest.raises(TypeError) as ctx:
        assert unflatten([(42, "val")])
    assert "must be strings" in str(ctx.value)


@pytest.mark.parametrize(
    "key, parsed",
    [
        ("foo", ["foo"]),
        ('"foo.a"[0]', ["foo.a", 0]),
        ('"foo.a"."foo- .b"[0]', ["foo.a", "foo- .b", 0]),
        ("foo.bar", ["foo", "bar"]),
        (".foo", ["", "foo"]),
        ("foo[1]", ["foo", 1]),
        ("[1]", ["", 1]),
        (".", ["", ""]),
        (".[0]", ["", "", 0]),
        ("foo[1][2]", ["foo", 1, 2]),
        ("foo[1][2].bar", ["foo", 1, 2, "bar"]),
        ('"foo[1][2]bar"', ["foo[1][2]bar"]),
    ],
)
class Test_parse(object):
    def test_parse_key(self, key, parsed):
        assert _parse_key(key) == list(parsed)

    def test_unparse_key(self, key, parsed):
        assert _unparse_key(parsed) == key


@pytest.mark.parametrize(
    "key",
    [
        "foo[1][2]bar",
    ],
)
class Test_parse_bad_case(object):
    def test_parse_key(self, key):
        with pytest.raises(ValueError) as ctx:
            _parse_key(key)


@pytest.mark.parametrize(
    "parsed",
    [],
)
class Test_unparse_bad_case(object):
    def test_unparse_key(self, parsed):
        with pytest.raises(ValueError) as ctx:
            _unparse_key(parsed)
