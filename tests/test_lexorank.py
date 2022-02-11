# Third-party libraries
from unittest import TestCase

# Own's Libraries
from lexo_rank import LexoRank
from libs.utils.logger_util import LoggerUtil


class LexoRankTest(TestCase):

    def test_NUMERAL_SYSTEM(self):
        logger = LoggerUtil.create("testing")
        logger.info("Testing ...")

        response = LexoRank.middle()
        print(response)
