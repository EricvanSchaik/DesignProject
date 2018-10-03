import unittest
from parse_string import custom_function_parser as cfp
from parse_string.parse_exception import ParseException


class FunctionParseTestCase(unittest.TestCase):

    def test_correct_syntax(self):
        self.assertEqual("5+5", cfp.parse("5 + 5"),
                         "Plus operation parsed incorrectly")
        self.assertEqual("10-5", cfp.parse("10 - 5"),
                         "Minus operation parsed incorrectly")
        self.assertEqual("4*a", cfp.parse("4 * a"),
                         "Multiplication operation parsed incorrectly")
        self.assertEqual("25/5", cfp.parse("25 / 5"),
                         "Division operation parsed incorrectly")
        self.assertEqual("x**2", cfp.parse("x^2"),
                         "Power operation parsed incorrectly")
        self.assertEqual("(b)**0.5", cfp.parse("sqrt(b)"),
                         "Square root operation parsed incorrectly")
        self.assertEqual("(x+y)*2", cfp.parse("(x + y) * 2"),
                         "Bracket operation parsed incorrectly")
        self.assertEqual("(Ax**2+Ay**2+Az**2)**0.5", cfp.parse("sqrt(Ax^2 + Ay^2 + Az^2)"),
                         "Vector operation parsed incorrectly")

    def test_incorrect_syntax(self):
        self.assertRaises(ParseException, cfp.parse, "(3 + 4")
        self.assertRaises(ParseException, cfp.parse, "a /")
        self.assertRaises(ParseException, cfp.parse, "3 ** x")
        self.assertRaises(ParseException, cfp.parse, "- 4")
        self.assertRaises(ParseException, cfp.parse, "sqrt 5")
        self.assertRaises(ParseException, cfp.parse, "4^")
