from builtins import isinstance, list

from app.util import collection_utils


def test_coerce_to_list():
    assert isinstance(collection_utils.coerce_to_list('abc'), list)

    l = [1, 2, 3]
    assert collection_utils.coerce_to_list(l) == l


def test_append_dicts():
    d = {
        'a': 1,
        'b': 2
    }

    d2 = {
        'a': 3,
        'b': 4
    }

    collection_utils.append_dicts(d, d2)

    assert d['a'] == [1, 3]
    assert d['b'] == [2, 4]
