import random
import string


def password(length=12, letters=True, uppercase=True, digits=True, punctuation=False):
    chars = ''
    if letters:
        chars = chars + string.ascii_letters
    if digits:
        chars = chars + string.digits
    if punctuation:
        chars = chars + string.punctuation

    pwd = ''.join(random.choice(chars) for i in range(length))
    if not uppercase:
        pwd = pwd.lower()

    return pwd
