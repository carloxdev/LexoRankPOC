from lexo_decimal import LexoDecimal
from lexo_rankbucket import LexoRankBucket
from string_builder import StringBuilder
from lexo_numeral_system36 import LexoNumeralSystem36
import logging

logger = logging.getLogger(__name__)


class LexoRank(object):
    _NUMERAL_SYSTEM = None
    _MIN_DECIMAL = None
    _ZERO_DECIMAL = None
    _MAX_DECIMAL = None
    _ONE_DECIMAL = None
    _EIGHT_DECIMAL = None
    _INITIAL_MIN_DECIMAL = None
    _INITIAL_MAX_DECIMAL = None

    @classmethod
    def NUMERAL_SYSTEM(self):
        if self._NUMERAL_SYSTEM is None:
            self._NUMERAL_SYSTEM = LexoNumeralSystem36()

        return self._NUMERAL_SYSTEM

    @classmethod
    def ZERO_DECIMAL(self):
        if self._ZERO_DECIMAL is None:
            self._ZERO_DECIMAL = LexoDecimal.parse('0', LexoRank.NUMERAL_SYSTEM())

        return self._ZERO_DECIMAL

    @classmethod
    def ONE_DECIMAL(self):
        if self._ONE_DECIMAL is None:
            self._ONE_DECIMAL = LexoDecimal.parse('1', LexoRank.NUMERAL_SYSTEM())

        return self._ONE_DECIMAL

    @classmethod
    def EIGHT_DECIMAL(self):
        if self._EIGHT_DECIMAL is None:
            self._EIGHT_DECIMAL = LexoDecimal.parse('8', LexoRank.NUMERAL_SYSTEM())

        return self._EIGHT_DECIMAL

    @classmethod
    def MIN_DECIMAL(self):
        if self._MIN_DECIMAL is None:
            self._MIN_DECIMAL = LexoRank.ZERO_DECIMAL()

        return self._MIN_DECIMAL

    @classmethod
    def MAX_DECIMAL(self):
        if self._MAX_DECIMAL is None:
            self._MAX_DECIMAL = LexoDecimal.parse('1000000', LexoRank.NUMERAL_SYSTEM()).subtract(self.ONE_DECIMAL())

        return self._MAX_DECIMAL

    @classmethod
    def MID_DECIMAL(self):
        if self._MID_DECIMAL is None:
            self._MID_DECIMAL = LexoRank.between(LexoRank.MIN_DECIMAL(), LexoRank.MAX_DECIMAL())

        return self._MID_DECIMAL

    @classmethod
    def INITIAL_MIN_DECIMAL(self):
        if self._INITIAL_MIN_DECIMAL is None:
            self._INITIAL_MIN_DECIMAL = LexoDecimal.parse('100000', LexoRank.NUMERAL_SYSTEM())

        return self._INITIAL_MIN_DECIMAL

    @classmethod
    def INITIAL_MAX_DECIMAL(self):
        if self._INITIAL_MAX_DECIMAL is None:
            self._INITIAL_MAX_DECIMAL = LexoDecimal.parse(LexoRank.NUMERAL_SYSTEM().toChar(LexoRank.NUMERAL_SYSTEM().getBase() - 2) + '00000', LexoRank.NUMERAL_SYSTEM())

        return self._INITIAL_MAX_DECIMAL

    @classmethod
    def min(self):
        bucketObj = LexoRankBucket.BUCKET_0()
        minLexDecimalObj = LexoRank.MIN_DECIMAL()
        lexorankFromObj = self._from(bucketObj, minLexDecimalObj)

        return lexorankFromObj

    @classmethod
    def middle(self):
        minLexoRank = self.min()
        maxObj = self.max(minLexoRank.bucket)
        lexorankObj = minLexoRank.between(maxObj)
        return lexorankObj

    @classmethod
    def max(self, bucket=LexoRankBucket.BUCKET_0()):
        lexorankMaxObj = LexoRank._from(bucket, LexoRank.MAX_DECIMAL())
        return lexorankMaxObj

    @classmethod
    def initial(self, bucket):
        return bucket == LexoRank._from(bucket, LexoRank.INITIAL_MIN_DECIMAL()) if LexoRankBucket.BUCKET_0() else LexoRank._from(bucket, LexoRank.INITIAL_MAX_DECIMAL())

    @classmethod
    def _between(self, oLeft, oRight):
        if oLeft.getSystem().getBase() != oRight.getSystem().getBase():
            raise ValueError('Expected same system')

        left = oLeft
        right = oRight
        nLeft = None
        if oLeft.getScale() < oRight.getScale():
            nLeft = oRight.setScale(oLeft.getScale(), False)
            if oLeft.compareTo(nLeft) >= 0:
                return LexoRank.mid(oLeft, oRight)

            right = nLeft

        if oLeft.getScale() > right.getScale():
            nLeft = oLeft.setScale(right.getScale(), True)
            if nLeft.compareTo(right) >= 0:
                return LexoRank.mid(oLeft, oRight)

            left = nLeft

        nRight = None

        scale = left.getScale()
        while (scale > 0):
            nScale1 = scale - 1
            nLeft1 = left.setScale(nScale1, True)
            nRight = right.setScale(nScale1, False)
            cmp = nLeft1.compareTo(nRight)
            if cmp == 0:
                return LexoRank.checkMid(oLeft, oRight, nLeft1)

            if nLeft1.compareTo(nRight) > 0:
                break

            scale = nScale1
            left = nLeft1

            right = nRight

        mid = LexoRank.middleInternal(oLeft, oRight, left, right)

        nScale = None
        mScale = mid.getScale()
        while (mScale > 0):
            nScale = mScale - 1
            nMid = mid.setScale(nScale)
            if oLeft.compareTo(nMid) >= 0 or nMid.compareTo(oRight) >= 0:
                break

            mid = nMid
            mScale = nScale

        return mid

    @classmethod
    def parse(self, str):
        parts = str.split('|')
        bucket = LexoRankBucket._from(parts[0])
        decimal = LexoDecimal.parse(parts[1], LexoRank.NUMERAL_SYSTEM())
        return LexoRank(bucket, decimal)

    @classmethod
    def _from(self, bucket, decimal):
        if decimal.getSystem().getBase() != self.NUMERAL_SYSTEM().getBase():
            raise ValueError('Expected different system')

        obj = LexoRank(bucket, decimal)
        return obj

    @classmethod
    def middleInternal(self, lbound, rbound, left, right):
        mid = LexoRank.mid(left, right)
        return LexoRank.checkMid(lbound, rbound, mid)

    @classmethod
    def checkMid(self, lbound, rbound, mid):
        if lbound.compareTo(mid) >= 0:
            return LexoRank.mid(lbound, rbound)

        return LexoRank.mid(lbound, rbound) if mid.compareTo(rbound) >= 0 else mid

    @classmethod
    def mid(self, left, right):
        sum = left.add(right)
        mid = sum.multiply(LexoDecimal.half(left.getSystem()))
        scale = left.getScale() if left.getScale() > right.getScale() else right.getScale()

        if mid.getScale() > scale:
            roundDown = mid.setScale(scale, False)
            if roundDown.compareTo(left) > 0:
                return roundDown

            roundUp = mid.setScale(scale, True)
            if roundUp.compareTo(right) < 0:
                return roundUp

        return mid

    @classmethod
    def formatDecimal(self, decimal):
        formatVal = decimal.format()
        val = StringBuilder(formatVal)
        partialIndex = formatVal.find(LexoRank.NUMERAL_SYSTEM().getRadixPointChar())

        zero = LexoRank.NUMERAL_SYSTEM().toChar(0)
        if partialIndex < 0:
            partialIndex = len(formatVal)
            val.append(LexoRank.NUMERAL_SYSTEM().getRadixPointChar())

        while (partialIndex < 6):
            val.insert(0, zero)
            partialIndex += 1

        while (val.str[val.getLength() - 1] == zero):
            val.setLength(val.getLength() - 1)

        return val.toString()

    def __init__(self, bucket, decimal):
        self.value = bucket.format() + '|' + self.formatDecimal(decimal)
        self.bucket = bucket
        self.decimal = decimal

    def __repr__(self):
        value = "LexoRank [value: {}, bucket: {}, decimal: {}]"
        value = value.format(
            self.value,
            self.bucket,
            self.decimal
        )
        return value

    def genPrev(self):
        if self.isMax():
            return LexoRank(self.bucket, LexoRank.INITIAL_MAX_DECIMAL())

        floorInteger = self.decimal.floor()
        floorDecimal = LexoDecimal._from(floorInteger)
        nextDecimal = floorDecimal.subtract(LexoRank.EIGHT_DECIMAL())
        if nextDecimal.compareTo(LexoRank.MIN_DECIMAL()) <= 0:
            nextDecimal = LexoRank.between(LexoRank.MIN_DECIMAL(), self.decimal)

        return LexoRank(self.bucket, nextDecimal)

    def genNext(self):
        if self.isMin():
            return LexoRank(self.bucket, LexoRank.INITIAL_MIN_DECIMAL())

        ceilInteger = self.decimal.ceil()
        ceilDecimal = LexoDecimal._from(ceilInteger)
        nextDecimal = ceilDecimal.add(LexoRank.EIGHT_DECIMAL())
        if nextDecimal.compareTo(LexoRank.MAX_DECIMAL()) >= 0:
            nextDecimal = LexoRank.between(self.decimal, LexoRank.MAX_DECIMAL())

        return LexoRank(self.bucket, nextDecimal)

    def between(self, other):
        if self.bucket.equals(other.bucket) is None:
            raise ValueError('Between works only within the same bucket')

        cmp = self.decimal.compareTo(other.decimal)
        if cmp > 0:
            obj1 = LexoRank._between(other.decimal, self.decimal)
            new_obj = LexoRank(self.bucket, obj1)
            return new_obj

        if cmp == 0:
            raise ValueError(
                f"Try to rank between issues with same rank this={self}"
                f" other={other}"
                f" self.decimal={self.decimal}"
                f" other.decimal={other.decimal}"
            )

        betweenObj = LexoRank._between(self.decimal, other.decimal)
        return LexoRank(self.bucket, betweenObj)

    def getBucket(self):
        return self.bucket

    def getDecimal(self):
        return self.decimal

    def inNextBucket(self):
        return LexoRank._from(self.bucket.next(), self.decimal)

    def inPrevBucket(self):
        return LexoRank._from(self.bucket.prev(), self.decimal)

    def isMin(self):
        return self.decimal.equals(LexoRank.MIN_DECIMAL())

    def isMax(self):
        return self.decimal.equals(LexoRank.MAX_DECIMAL())

    def format(self):
        return self.value

    def equals(self, other):
        if self == other:
            return True

        if other is None:
            return False

        return self.value == other.value

    def toString(self):
        return self.value

    def compareTo(self, other):
        if (self == other):
            return 0

        if other is None:
            return 1

        return self.value.localeCompare(other.value)
