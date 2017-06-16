import re

MAP = {
    "w": "a",
    "k": "b",
    "v": "c",
    "1": "d",
    "j": "e",
    "u": "f",
    "2": "g",
    "i": "h",
    "t": "i",
    "3": "j",
    "h": "k",
    "s": "l",
    "4": "m",
    "g": "n",
    "5": "o",
    "r": "p",
    "q": "q",
    "6": "r",
    "f": "s",
    "p": "t",
    "7": "u",
    "e": "v",
    "o": "w",
    "8": "1",
    "d": "2",
    "n": "3",
    "9": "4",
    "c": "5",
    "m": "6",
    "0": "7",
    "b": "8",
    "l": "9",
    "a": "0",
    "_z2C$q": ":",
    "_z&e3B": ".",
    "AzdH3F": "/"
}

T = re.compile(r'([a-w\d])', re.DOTALL)
N = re.compile(r'(_z2C\$q|_z&e3B|AzdH3F)', re.DOTALL)


def uncompile(content):
    if not content:
        return ""
    func = lambda m: MAP[m.group(1)]
    o = re.sub(N, func, content)
    return re.sub(T, func, o)


def uncompile_url(url):
    if not url:
        return ""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return uncompile(url)

