import unittest
import pytest
import GameWindow as gw
import MyException
from parameterized import parameterized


class MyTestCase(unittest.TestCase):

    paramList = [[1, 1, 1],
                 [5, 1, 2],
                 [4, 1, 2],
                 [5, 6, -4],
                 [3, 3, 10],
                 [1, 10, 5]]

    def test_shouldRaiseInputError_whenWrongInputIsGiven(self):
        for i in self.paramList:
            self.assertRaises(Exception, gw.GameWindow, i[0], i[1], i[2])


if __name__ == '__main__':
    unittest.main()
