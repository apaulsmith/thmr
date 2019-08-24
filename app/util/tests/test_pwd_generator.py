import string

from app.util import pwd_generator


def test_pwd_generator():
    p = pwd_generator.password(length=8, letters=True, uppercase=False, digits=False, punctuation=False)
    assert_pwd(p, length=8, letters=True, uppercase=False, digits=False, punctuation=False)


def assert_pwd(p, length, letters, uppercase, digits, punctuation):
    assert len(p) == length
    assert (p == p.lower()) != uppercase
    assert has_letters(p) == letters
    assert has_digits(p) == digits
    assert has_punctuation(p) == punctuation


def has_letters(s):
    return _has(s, string.ascii_letters)


def has_digits(s):
    return _has(s, string.digits)


def has_punctuation(s):
    return _has(s, string.punctuation)


def _has(s, domain):
    for c in s:
        if c in domain:
            return True

    return False
