from hashlib import md5
from app.models import Paste


BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_character(digit):
    return BASE62[digit]


def base_encode(num, base=62):
    digits = []
    while num > 0:
        remainder = num % base
        digits.append(remainder)
        num = num // base
    digits = digits[::-1]
    return list(map(get_character, digits))


def generate_new_shortlink(ip_addr, timestamp, length=8):
    key = str(ip_addr + timestamp).encode('utf-8')
    hexvalue = md5(key).hexdigest()
    decvalue = int(hexvalue, 16)
    url = base_encode(decvalue)
    return ''.join(url[:length])


def generate_shortlink(ip_addr, timestamp, length=8):
    """
    short link must be different than existing shortlinks
    """
    shortlink = generate_new_shortlink(ip_addr, timestamp, length)
    while Paste.query.filter_by(shortlink=shortlink).one_or_none() is not None:
        shortlink = generate_new_shortlink()
    return shortlink
