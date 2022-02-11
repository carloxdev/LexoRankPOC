import logging

logger = logging.getLogger(__name__)


class StringBuilder(object):

    def __init__(self, str = ''):
        self.str = str

    def getLength(self):
        return len(self.str)

    def setLength(self, value):
        self.str = self.str[0:value]

    def append(self, str):
        self.str = self.str + str
        return self

    def remove(self, startIndex, length):
        self.str = self.str[0:startIndex] + self.str[startIndex + length]
        return self

    def insert(self, index, value):
        self.str = self.str[0:index] + value + self.str[index]
        return self

    def toString(self):
        return self.str

