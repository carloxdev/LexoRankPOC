# Third-party libraries
from re import L
from unittest import TestCase
from urllib import response

# Own's Libraries
from lexo_rank import LexoRank
from lexo_rankbucket import LexoRankBucket
from libs.utils.logger_util import LoggerUtil


class LexoRankTest(TestCase):

    def Create50(self):
        logger = LoggerUtil.create("testing")

        last_value = None
        for x in range(50):
            if x == 0:
                first_response = LexoRank.middle()
                first_value = first_response.toString()

                last_value = first_value

            else:
                current_response = LexoRank.parse(last_value)
                next_response = current_response.genNext()
                next_value = next_response.toString()

                if next_value == last_value:
                    raise ValueError("Valor repetido")

                last_value = next_value

            logger.info(last_value)

    def test_MiddleValue(self):
        logger = LoggerUtil.create("testing")

        start = "0|i0006v:00m"
        end = "0|i0006v:00r"

        start_response = LexoRank.parse(start)
        start_value = start_response.toString()
        logger.info(f"Start Value: {start_value}")

        end_response = LexoRank.parse(end)
        end_value = end_response.toString()
        logger.info(f"End Value: {end_value}")

        middle_response = start_response.between(end_response)
        middle_value = middle_response.toString()
        logger.info(f"Middle value: {middle_value}")
