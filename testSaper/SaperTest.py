import unittest
from saper.SaperGame import GameWindow as gw
import SaperTestMyVariables as myVariables


class MyTestCase(unittest.TestCase):
    GW = gw.GameWindow()

    def test_shouldRaiseInputError_whenWrongInputIsGiven(self):
        for i in myVariables.paramList:
            self.assertRaises(Exception, self.GW.resetGame, i[0], i[1], i[2])


if __name__ == '__main__':
    unittest.main()
