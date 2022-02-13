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
    finalLength = sourceIndex + length

    i = sourceIndex
    while(i < finalLength):
        destinationArray[destination] = sourceArray[i]
        destination += 1

        i += 1
