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

    @classmethod
    def middle(self):
        logger.info("Getting middle ... NO Parameters")
        minLexoRank = self.min()
        return minLexoRank.between(self.max(minLexoRank.bucket))

    @classmethod
    def min(self):
        logger.info("Executing min() function ... No Parameters")
        return self._from(
            LexoRankBucket.BUCKET_0(),
            self.MIN_DECIMAL()
        )

    @classmethod
    def MIN_DECIMAL(self):
        if self._MIN_DECIMAL is None:
            self._MIN_DECIMAL = self.ZERO_DECIMAL()

        return self._MIN_DECIMAL

    @classmethod
    def ZERO_DECIMAL(self):
        if self._ZERO_DECIMAL is None:
            self._ZERO_DECIMAL = LexoDecimal.parse('0', self.NUMERAL_SYSTEM())

        return self._ZERO_DECIMAL

    @classmethod
    def NUMERAL_SYSTEM(self):
        if self._NUMERAL_SYSTEM is None:
            self._NUMERAL_SYSTEM = LexoNumeralSystem36()

        return self._NUMERAL_SYSTEM

    @classmethod
    def _from(self, bucket, decimal):
        logger.info(f"Executing _from() function ... bucket: {bucket}, decimal: {decimal}")
        if decimal.getSystem().getBase() != self.NUMERAL_SYSTEM().getBase():
            raise ValueError('Expected different system')

        return self(bucket, decimal)

    @classmethod
    def formatDecimal(self, decimal):
        logger.info(f"Executing formatDecimal. decimal: {decimal}")

        formatVal = decimal.format()
        val = StringBuilder(formatVal)
        partialIndex = formatVal.find(self.NUMERAL_SYSTEM().getRadixPointChar())

        zero = self.NUMERAL_SYSTEM().toChar(0)
        if partialIndex < 0:
            partialIndex = formatVal.length
            val.append(self.NUMERAL_SYSTEM().getRadixPointChar())

        while (partialIndex < 6):
            val.insert(0, zero)
            partialIndex += 1

        while (val[len(val) - 1] == zero):
            val.setLength(val.getLength() - 1)

        return str(val)

    @classmethod
    def max(self, bucket=LexoRankBucket.BUCKET_0()):
        return self._from(bucket, self.MAX_DECIMAL)

    def __init__(self, bucket, decimal):
        self.value = bucket.format() + '|' + self.formatDecimal(decimal)
        self.bucket = bucket
        self.decimal = decimal

        logger.info(
            f"LexonRank object was created. value: {self.value}, bucket: {self.bucket}, decimal: {self.decimal}"
        )
