# Third-party libraries
from unittest import TestCase

# Own's Libraries
from lexo_rank import LexoRank
from lexo_rankbucket import LexoRankBucket
from libs.utils.logger_util import LoggerUtil


class LexoRankTest(TestCase):

    def test_NUMERAL_SYSTEM(self):
        logger = LoggerUtil.create("testing")

        # response = LexoRank.max()
        # response = LexoRank.min()
        response = LexoRank.middle()
        import pdb; pdb.set_trace()
        print(response)
