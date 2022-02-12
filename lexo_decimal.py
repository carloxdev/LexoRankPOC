
from lexo_integer import LexoInteger
from string_builder import StringBuilder

import logging

logger = logging.getLogger(__name__)


class LexoDecimal(object):

    @classmethod
    def half(self, sys):
        mid = (sys.getBase() / 2) if (sys.getBase() / 2) else 0
        return self.make(LexoInteger.make(sys, 1, [mid]), 1)

    @classmethod
    def parse(self, str, system):
        partialIndex = str.find(system.getRadixPointChar())
        if str.find(system.getRadixPointChar()) != partialIndex:
            raise ValueError(f"More than one {system.getRadixPointChar()}")

        if partialIndex < 0:
            lexoDecimalObj = LexoDecimal.make(LexoInteger.parse(str, system), 0)
            return lexoDecimalObj

        intStr = str[0, partialIndex] + str[partialIndex + 1]
        return self.make(
            LexoInteger.parse(intStr, system),
            len(str) - 1 - partialIndex
        )

    @classmethod
    def _from(self, integer):
        return self.make(integer, 0)

    @classmethod
    def make(self, integer, sig):
        if integer.isZero():
            return LexoDecimal(integer, 0)

        zeroCount = 0
        i = 0

        while(i < sig and integer.getMag(i) == 0):
            zeroCount += 1
            i += 1

        newInteger = integer.shiftRight(zeroCount)
        newSig = sig - zeroCount
        return LexoDecimal(newInteger, newSig)

    def __init__(self, mag, sig):
        self.mag = mag
        self.sig = sig

    def __repr__(self):
        value = "LexoDecimal [mag: {}, sig: {}]"
        value = value.format(
            self.mag,
            self.sig
        )
        return value

    def getSystem(self):
        return self.mag.getSystem()

    def format(self):
        logger.info("--> LexoDecimal.format()")

        intStr = self.mag.format()
        if self.sig == 0:
            logger.info(f"<-- LexoDecimal.format(): intStr: {intStr}")
            return intStr

        sb = StringBuilder(intStr)

        head = sb[0]
        specialHead = head == self.mag.getSystem().getPositiveChar() or head == self.mag.getSystem().getNegativeChar()
        if specialHead:
            sb.remove(0, 1)

        while (sb.getLength() < self.sig + 1):
            sb.insert(0, self.mag.getSystem().toChar(0))

        sb.insert(sb.getLength() - self.sig, self.mag.getSystem().getRadixPointChar())

        if sb.getLength() - self.sig == 0:
            sb.insert(0, self.mag.getSystem().toChar(0))

        if specialHead:
            sb.insert(0, head)

        logger.info(f"<-- LexoDecimal.format(): sb.toString: {sb.toString()}")
        return sb.toString()

    def subtract(self, other):
        thisMag = self.mag
        thisSig = self.sig
        otherMag = other.mag
        otherSig = other.sig

        while(thisSig < otherSig):
            thisMag = thisMag.shiftLeft()
            thisSig += 1

        while (thisSig > otherSig):
            otherMag = otherMag.shiftLeft()
            otherSig += 1

        return LexoDecimal.make(thisMag.subtract(otherMag), thisSig)

    def compareTo(self, other):
        if self == other:
            return 0

        if other is None:
            return 1

        tMag = self.mag
        oMag = other.mag

        if self.sig > other.sig:
            oMag = oMag.shiftLeft(self.sig - other.sig)

        elif self.sig < other.sig:
            tMag = tMag.shiftLeft(other.sig - self.sig)

        return tMag.compareTo(oMag)

    def add(self, other):
        tmag = self.mag
        tsig = self.sig
        omag = other.mag
        osig = other.sig

        while(tsig < osig):
            tmag = tmag.shiftLeft()

            tsig += 1

        while (tsig > osig):
            omag = omag.shiftLeft()
            osig += 1

        return LexoDecimal.make(tmag.add(omag), tsig)

    def multiply(self, other):
        return LexoDecimal.make(self.mag.multiply(other.mag), self.sig + other.sig)

    # floor() {
    #     return self.mag.shiftRight(self.sig);
    # }
    # ceil() {
    #     if (self.isExact()) {
    #         return self.mag;
    #     }
    #     const floor = self.floor();
    #     return floor.add(lexoInteger_1.LexoInteger.one(floor.getSystem()));
    # }
    # isExact() {
    #     if (self.sig === 0) {
    #         return true;
    #     }
    #     for (let i = 0; i < self.sig; ++i) {
    #         if (self.mag.getMag(i) !== 0) {
    #             return false;
    #         }
    #     }
    #     return true;
    # }

    def getScale(self):
        return self.sig

    def setScale(self, nsig, ceiling=False):
        if nsig >= self.sig:
            return self

        if nsig < 0:
            nsig = 0

        diff = self.sig - nsig
        nmag = self.mag.shiftRight(diff)

        if ceiling:
            nmag = nmag.add(LexoInteger.one(nmag.getSystem()))

        return LexoDecimal.make(nmag, nsig)

    # compareTo(other) {
    #     if (this === other) {
    #         return 0;
    #     }
    #     if (!other) {
    #         return 1;
    #     }
    #     let tMag = self.mag;
    #     let oMag = other.mag;
    #     if (self.sig > other.sig) {
    #         oMag = oMag.shiftLeft(self.sig - other.sig);
    #     }
    #     else if (self.sig < other.sig) {
    #         tMag = tMag.shiftLeft(other.sig - self.sig);
    #     }
    #     return tMag.compareTo(oMag);
    # }

    # equals(other) {
    #     if (this === other) {
    #         return true;
    #     }
    #     if (!other) {
    #         return false;
    #     }
    #     return self.mag.equals(other.mag) && self.sig === other.sig;
    # }

    # toString() {
    #     return self.format();
    # }
