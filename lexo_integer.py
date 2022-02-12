from xml.dom import ValidationErr
from lexo_helper import arrayCopy
from string_builder import StringBuilder
import logging

logger = logging.getLogger(__name__)

ZERO_MAG = [0]
ONE_MAG = [1]
NEGATIVE_SIGN = -1
ZERO_SIGN = 0
POSITIVE_SIGN = 1


class LexoInteger(object):

    def __init__(self, system, sign, mag):
        self.sys = system
        self.sign = sign
        self.mag = mag

    def __repr__(self):
        value = "LexoInteger [sys: {}, sign: {}, mag: {}]"
        value = value.format(
            self.sys,
            self.sign,
            self.mag
        )
        return value

    @classmethod
    def parse(self, strFull, system):
        str = strFull
        sign = 1

        if strFull.find(system.getPositiveChar()) == 0:
            str = strFull[1:]

        elif strFull.find(system.getNegativeChar()) == 0:
            str = strFull[1:]
            sign = -1

        mag = [None] * len(str)

        strIndex = len(mag) - 1

        magIndex = 0
        while(strIndex >= 0):
            mag[magIndex] = system.toDigit(str[strIndex])
            strIndex -= 1
            magIndex += 1

        lexointegerObj = self.make(system, sign, mag)
        return lexointegerObj

    @classmethod
    def zero(self, sys):
        return LexoInteger(sys, 0, ZERO_MAG)

    @classmethod
    def one(self, sys):
        return LexoInteger.make(sys, 1, ONE_MAG)

    @classmethod
    def make(self, sys, sign, mag):
        actualLength = len(mag)

        while (actualLength > 0 and mag[actualLength - 1] == 0):
            actualLength -= 1
            # ingnore

        if actualLength == 0:
            lexointegerObj = LexoInteger.zero(sys)
            return lexointegerObj

        if actualLength == len(mag):
            lexointegerObj = LexoInteger(sys, sign, mag)
            return lexointegerObj

        nmag = [0] * actualLength
        arrayCopy(mag, 0, nmag, 0, actualLength)
        lexointegerObj = LexoInteger(sys, sign, nmag)
        return lexointegerObj

    @classmethod
    def _add(self, sys, li, r):
        estimatedSize = max(len(li), len(r))
        result = [0] * estimatedSize
        carry = 0

        for i in range(estimatedSize):
            lnum = li[i] if i < len(li) else 0
            rnum = r[i] if i < len(r) else 0
            sum = lnum + rnum + carry

            carry = 0
            while(sum >= sys.getBase()):
                carry += 1
                sum -= sys.getBase()

            result[i] = sum

        return LexoInteger.extendWithCarry(result, carry)

    @classmethod
    def extendWithCarry(self, mag, carry):
        if carry > 0:
            extendedMag = [0] * (len(mag) + 1)
            arrayCopy(mag, 0, extendedMag, 0, len(mag))
            extendedMag[len(extendedMag) - 1] = carry
            return extendedMag

        return mag

    @classmethod
    def _subtract(self, sys, li, r):
        rComplement = LexoInteger.complement(sys, r, len(li))
        rSum = LexoInteger._add(sys, li, rComplement)
        rSum[len(rSum) - 1] = 0
        return LexoInteger._add(sys, rSum, ONE_MAG)

    @classmethod
    def _multiply(self, sys, la, r):
        result = [0] * (len(la) + len(r))

        li = 0
        while(li < len(la)):
            ri = 0
            while(ri < len(r)):
                resultIndex = li + ri

                result[resultIndex] += la[li] * r[ri]
                while(result[resultIndex] >= sys.getBase()):
                    result[resultIndex + 1] += 1

                    result[resultIndex] -= sys.getBase()

                ri += 1

            li += 1

        return result

    @classmethod
    def complement(self, sys, mag, digits):
        if digits <= 0:
            raise ValidationErr('Expected at least 1 digit')

        nmag = [sys.getBase() - 1] * digits

        for i in range(len(mag)):
            nmag[i] = sys.getBase() - 1 - mag[i]

        return nmag

    @classmethod
    def compare(self, li, r):
        if (len(li) < len(r)):
            return -1

        if (len(li) > len(r)):
            return 1

        i = len(li) - 1
        while(i >= 0):
            if li[i] < r[i]:
                return -1

            if li[i] > r[i]:
                return 1

            i -= 1

        return 0

    def add(self, other):
        self.checkSystem(other)
        if self.isZero():
            return other

        if other.isZero():
            return self

        if self.sign != other.sign:
            pos = None
            if self.sign == -1:
                pos = self.negate()
                val = pos.subtract(other)
                return val.negate()

            pos = other.negate()
            return self.subtract(pos)

        result = LexoInteger.add(self.sys, self.mag, other.mag)
        return LexoInteger.make(self.sys, self.sign, result)

    def subtract(self, other):
        self.checkSystem(other)
        if self.isZero():
            return other.negate()

        if other.isZero():
            return self

        if self.sign != other.sign:
            negate = None
            if self.sign == -1:
                negate = self.negate()
                sum = negate.add(other)
                return sum.negate()

            negate = other.negate()
            return self.add(negate)

        cmp = LexoInteger.compare(self.mag, other.mag)
        if cmp == 0:
            return LexoInteger.zero(self.sys)

        return LexoInteger.make(self.sys, 1 if self.sign == -1 else -1, LexoInteger._subtract(self.sys, other.mag, self.mag)) if cmp < 0 else LexoInteger.make(self.sys, -1 if self.sign == -1 else 1, LexoInteger._subtract(self.sys, self.mag, other.mag))

    def multiply(self, other):
        self.checkSystem(other)
        if self.isZero():
            return self

        if other.isZero():
            return other

        if self.isOneish():
            return LexoInteger.make(self.sys, 1, other.mag) if self.sign == other.sign else LexoInteger.make(self.sys, -1, other.mag)

        if other.isOneish():
            return LexoInteger.make(self.sys, 1, self.mag) if self.sign == other.sign else LexoInteger.make(self.sys, -1, self.mag)

        newMag = LexoInteger._multiply(self.sys, self.mag, other.mag)
        return LexoInteger.make(self.sys, 1, newMag) if self.sign == other.sign else LexoInteger.make(self.sys, -1, newMag)

    def negate(self):
        return self if self.isZero() else LexoInteger.make(self.sys, -1 if self.sign == 1 else 1, self.mag)

    def shiftRight(self, times=1):
        if len(self.mag) - times <= 0:
            return LexoInteger.zero(self.sys)

        nmag = [0] * (len(self.mag) - times)

        arrayCopy(self.mag, times, nmag, 0, len(nmag))
        return self.make(self.sys, self.sign, nmag)

    def isZero(self):
        return self.sign == 0 and len(self.mag) == 1 and self.mag[0] == 0

    def getMag(self, index):
        return self.mag[index]

    def compareTo(self, other):
        if self == other:
            return 0

        if other is None:
            return 1

        if self.sign == -1:
            if other.sign == -1:
                cmp = LexoInteger.compare(self.mag, other.mag)
                if cmp == -1:
                    return 1

                return -1 if cmp == 1 else 0

            return -1

        if self.sign == 1:
            return LexoInteger.compare(self.mag, other.mag) if other.sign == 1 else 1

        if other.sign == -1:
            return 1

        return -1 if other.sign == 1 else 0

    def getSystem(self):
        return self.sys

    def format(self):
        if self.isZero():
            return '' + self.sys.toChar(0)

        sb = StringBuilder()
        var2 = self.mag
        var3 = len(var2)

        for var4 in range(var3):
            digit = var2[var4]
            sb.insert(0, self.sys.toChar(digit))

        if self.sign == -1:
            sb.insert(0, self.sys.getNegativeChar())

        return sb.toString()

    def isOneish(self):
        return len(self.mag) == 1 and self.mag[0] == 1

    def checkSystem(self, other):
        if self.sys.getBase() != other.sys.getBase():
            raise ValueError('Expected numbers of same numeral sys')
