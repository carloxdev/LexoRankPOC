import logging

logger = logging.getLogger(__name__)


def arrayCopy(
    sourceArray,
    sourceIndex,
    destinationArray,
    destinationIndex,
    length=None
):
    destination = destinationIndex

    if length:
        finalLength = sourceIndex + length
    else:
        finalLength = sourceIndex

    i = sourceIndex
    while(i > finalLength):
        destinationArray[destination] = sourceArray[i]
        i += 1
