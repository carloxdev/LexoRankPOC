import logging

logger = logging.getLogger(__name__)


class LexoNumeralSystem36(object):

    def __init__(self):
        self.DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'

    def __repr__(self):
        value = "LexoNumeralSystem36"
        return value

    def getBase(self):
        return 36

    def getPositiveChar(self):
        return '+'

    def getNegativeChar(self):
        return '-'

    def getRadixPointChar(self):
        return ':'

    def toDigit(self, ch):
        if ch >= '0' and ch <= '9':
            return ord(ch[0]) - 48

        if ch >= 'a' and ch <= 'z':
            return ord(ch[0]) - 97 + 10

        raise ValueError(f"Not valid digit: {ch}")

    def toChar(self, digit):
        return self.DIGITS[digit]
