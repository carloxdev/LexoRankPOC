from lexo_integer import LexoInteger
# from lexo_rank import LexoRank
from lexo_numeral_system36 import LexoNumeralSystem36

import logging

logger = logging.getLogger(__name__)


class LexoRankBucket(object):
    _BUCKET_0 = None
    _BUCKET_1 = None
    _BUCKET_2 = None
    _VALUES = None

    _NUMERAL_SYSTEM = None

    @classmethod
    def BUCKET_0(self):
        if self._BUCKET_0 is None:
            self._BUCKET_0 = LexoRankBucket('0')

        return self._BUCKET_0

    @classmethod
    def BUCKET_1(self):
        if self._BUCKET_1 is None:
            self._BUCKET_1 = LexoRankBucket('1')

        return self._BUCKET_1

    @classmethod
    def BUCKET_2(self):
        if self._BUCKET_2 is None:
            self._BUCKET_2 = LexoRankBucket('2')

        return self._BUCKET_2

    @classmethod
    def VALUES(self):
        if self._VALUES is None:
            self._VALUES = [self.BUCKET_0(), self.BUCKET_1(), self.BUCKET_2()]

        return self._VALUES

    @classmethod
    def max(self):
        return self.VALUES[len(self.VALUES()) - 1]

    @classmethod
    def _from(self, str):
        val = LexoInteger.parse(str, self.NUMERAL_SYSTEM())
        var2 = self.VALUES()
        var3 = len(var2)

        for var4 in range(var3):
            bucket = var2[var4]
            if bucket.value.equals(val):
                return bucket

        raise ValueError('Unknown bucket: ' + str)

    @classmethod
    def resolve(self, bucketId):
        var1 = self.VALUES()
        var2 = len(var1)

        for var3 in range(var2):
            bucket = var1[var3]
            if bucket.equals(self._from(str(bucketId))):
                return bucket

        raise ValueError('No bucket found with id ' + bucketId)

    def __init__(self, val):
        self.value = LexoInteger.parse(val, self.NUMERAL_SYSTEM())

    def __repr__(self):
        value = "LexoRankBucket [value: {}]".format(self.value)
        return value

    def format(self):
        return self.value.format()

    def next(self):
        if self.equals(self.BUCKET_0()):
            return self.BUCKET_1

        if self.equals(self.BUCKET_1):
            return self.BUCKET_2

        return self.BUCKET_0() if self.equals(self.BUCKET_2()) else self.BUCKET_2()

    def prev(self):
        if self.equals(self.BUCKET_0()):
            return self.BUCKET_2()

        if self.equals(self.BUCKET_1()):
            return self.BUCKET_0()

        return self.BUCKET_1() if self.equals(self.BUCKET_2()) else self.BUCKET_0()

    def equals(self, other):
        if self is other:
            return True

        if other is None:
            return False

        return self.value.equals(other.value)

    @classmethod
    def NUMERAL_SYSTEM(self):
        if self._NUMERAL_SYSTEM is None:
            self._NUMERAL_SYSTEM = LexoNumeralSystem36()

        return self._NUMERAL_SYSTEM
