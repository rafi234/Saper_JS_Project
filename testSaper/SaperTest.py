import unittest
from saper.SaperGame import GameWindow as gw
import SaperTestMyVariables as myVariables


class MyTestCase(unittest.TestCase):

    def test_shouldRaiseInputError_whenWrongInputIsGiven(self):
        for i in myVariables.paramList:
            self.assertRaises(Exception, gw.GameWindow, i[0], i[1], i[2])


if __name__ == '__main__':
    unittest.main()
