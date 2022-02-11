
from lexo_integer import LexoInteger
# from string_builder import StringBuilder

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
            return LexoDecimal.make(LexoInteger.parse(str, system), 0)

        import pdb; pdb.set_trace()
        intStr = str[0, partialIndex] + str[partialIndex+1]
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
            return self(integer, 0)

        zeroCount = 0
        i = 0
        while(i < sig and integer.getMag(i) == 0):
            zeroCount += 1
            i += 1

        newInteger = integer.shiftRight(zeroCount)
        newSig = sig - zeroCount
        return self(newInteger, newSig)

    def __init__(self, mag, sig):
        self.mag = mag
        self.sig = sig

    def getSystem(self):
        return self.mag.getSystem()

    # def add(self, other):
    #     tmag = self.mag
    #     tsig = self.sig
    #     omag = other.mag
    #     osig = None

        # for (osig = other.sig; tsig < osig; ++tsig) {
        #     tmag = tmag.shiftLeft();
        # }

        # while (tsig > osig) {
        #     omag = omag.shiftLeft();
        #     ++osig;
        # }
        # return LexoDecimal.make(tmag.add(omag), tsig);

    # subtract(self, other):
    #     thisMag = self.mag;
    #     thisSig = self.sig;
    #     otherMag = other.mag;
    #     otherSig = None

    #     for (otherSig = other.sig; thisSig < otherSig; ++thisSig) {
    #         thisMag = thisMag.shiftLeft();
    #     }
    #     while (thisSig > otherSig) {
    #         otherMag = otherMag.shiftLeft();
    #         ++otherSig;
    #     }
    #     return LexoDecimal.make(thisMag.subtract(otherMag), thisSig);

    # multiply(other) {
    #     return LexoDecimal.make(self.mag.multiply(other.mag), self.sig + other.sig);
    # }
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
    # getScale() {
    #     return self.sig;
    # }
    # setScale(nsig, ceiling = false) {
    #     if (nsig >= self.sig) {
    #         return this;
    #     }
    #     if (nsig < 0) {
    #         nsig = 0;
    #     }
    #     const diff = self.sig - nsig;
    #     let nmag = self.mag.shiftRight(diff);
    #     if (ceiling) {
    #         nmag = nmag.add(lexoInteger_1.LexoInteger.one(nmag.getSystem()));
    #     }
    #     return LexoDecimal.make(nmag, nsig);
    # }
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
    # format() {
    #     const intStr = self.mag.format();
    #     if (self.sig === 0) {
    #         return intStr;
    #     }
    #     const sb = new stringBuilder_1.default(intStr);
    #     const head = sb[0];
    #     const specialHead = head === self.mag.getSystem().getPositiveChar() || head === self.mag.getSystem().getNegativeChar();
    #     if (specialHead) {
    #         sb.remove(0, 1);
    #     }
    #     while (sb.length < self.sig + 1) {
    #         sb.insert(0, self.mag.getSystem().toChar(0));
    #     }
    #     sb.insert(sb.length - self.sig, self.mag.getSystem().getRadixPointChar());
    #     if (sb.length - self.sig === 0) {
    #         sb.insert(0, self.mag.getSystem().toChar(0));
    #     }
    #     if (specialHead) {
    #         sb.insert(0, head);
    #     }
    #     return sb.toString();
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