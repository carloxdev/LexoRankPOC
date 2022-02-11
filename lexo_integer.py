from lexo_helper import arrayCopy
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

    @classmethod
    def parse(self, strFull, system):
        str = strFull
        sign = 1

        if strFull.find(system.getPositiveChar()) == 0:
            str = strFull[1:]

        elif strFull.find(system.getNegativeChar()) == 0:
            str = strFull[1:]
            sign = -1

        mag = [] * len(str)

        strIndex = len(mag) - 1

        magIndex = 0
        while(strIndex >= 0):
            mag[magIndex] = system.toDigit(str[strIndex])
            strIndex -= 1
            magIndex += 1

        return self.make(system, sign, mag)

    @classmethod
    def make(self, sys, sign, mag):
        actualLength = None

        # while (actualLength > 0 and mag[actualLength - 1]) == 0:
        #     # ingnore
        #     actualLength -= 1

        # if actualLength == 0:
        #     return self.zero(sys)

        # if actualLength == len(mag):
        #     return self(sys, sign, mag)

        if actualLength:
            nmag = [0] * actualLength
        else:
            nmag = [0]

        arrayCopy(mag, 0, nmag, 0, actualLength)

        return self(sys, sign, nmag)

    @classmethod
    def zero(self, sys):
        return self(sys, 0, ZERO_MAG)

    def shiftRight(times = 1) {
        if (this.mag.length - times <= 0) {
            return LexoInteger.zero(this.sys);
        }
        const nmag = new Array(this.mag.length - times).fill(0);
        lexoHelper_1.lexoHelper.arrayCopy(this.mag, times, nmag, 0, nmag.length);
        return LexoInteger.make(this.sys, this.sign, nmag);
    }

    def isZero(self):
        return self.sign == 0 and len(self.mag) == 1 and self.mag[0] == 0
