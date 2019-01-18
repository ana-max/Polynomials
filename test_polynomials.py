import unittest
from parser import *
from polynomial_exceptions import *
from polynomial import *


class PolynomialExceptions(unittest.TestCase):
    def test_init(self):
        polynomial = 'x+1'
        parser = ExceptionChecker(polynomial)
        self.assertEqual(polynomial, parser.txt)

    def test_incorrect_brackets_sequence(self):
        incorrect_str = '((x+1)(x+2y)'
        parser = ExceptionChecker(incorrect_str)
        self.assertFalse(parser._is_correct_bracket_seq())

    def test_correct_brackets_sequence2(self):
        incorrect_str = '2((x+1)(x+2y))(z+10)^10'
        parser = ExceptionChecker(incorrect_str)
        self.assertTrue(parser._is_correct_bracket_seq())

    def test_correct_brackets_sequence3(self):
        incorrect_str = '((()()(())())())'
        parser = ExceptionChecker(incorrect_str)
        self.assertTrue(parser._is_correct_bracket_seq())

    def test_bad_symbols(self):
        incorrect_str = '(x+y)!'
        parser = ExceptionChecker(incorrect_str)
        self.assertFalse(parser._is_corrector_input_symbols())

    def test_bad_symbols2(self):
        incorrect_str = '(xy+1_y+2'
        parser = ExceptionChecker(incorrect_str)
        self.assertFalse(parser._is_corrector_input_symbols())

    def test_bad_symbols3(self):
        incorrect_str = '№#!?%$@'
        parser = ExceptionChecker(incorrect_str)
        self.assertFalse(parser._is_corrector_input_symbols())

    def test_bad_Polynomial(self):
        p = '(x+y)^'
        correcter = ExceptionChecker(p)
        self.assertFalse(correcter._is_correct_polynomial())

    def test_bad_Polynomial2(self):
        p = '(xy+yx)+z-'
        correcter = ExceptionChecker(p)
        self.assertFalse(correcter._is_correct_polynomial())

    def test_bad_Polynomial3(self):
        p = '((x+xy)^(yz+z))'
        correcter = ExceptionChecker(p)
        self.assertFalse(correcter._is_correct_polynomial())

    def test_bad_Polynomial4(self):
        p = '(x+1)**5+5(x+1)**6'
        correcter = ExceptionChecker(p)
        self.assertTrue(correcter._is_correct_polynomial())

    def test_bad_Polynomial5(self):
        p = '(x+1)^!'
        correcter = ExceptionChecker(p)
        self.assertFalse(correcter._is_correct_polynomial())
        self.assertFalse(correcter._is_corrector_input_symbols())


class ParserTest(unittest.TestCase):
    def test_correct_math_str(self):
        abbreviated_entry_str = '2xy(z+1)^5'
        parser = Parser(abbreviated_entry_str)
        full_form = parser.parse_math_form_to_full_form()
        self.assertEqual(full_form, '2*x*y*(z+1)^5')

    def test_correct_math_str2(self):
        abbreviated_entry_str = '(z+1)^5xy'

        parser = Parser(abbreviated_entry_str)
        self.assertEqual(parser.
                         parse_math_form_to_full_form(), '(z+1)^5*x*y')

    def test_correct_multiplication_monomial(self):
        multiplication = '2*(x*y*z+1)'

        parser = Parser(multiplication)
        self.assertEqual(parser._get_monomial_in_bracket(), '(2)*(x*y*z+1)')

    def test_correct_multiplication_monomial2(self):
        multiplication = '2*(x*y*z+1)+59*x*y*(x*n-y*z)+56*x*(y+1)'

        parser = Parser(multiplication)
        self.assertEqual(parser._get_monomial_in_bracket(),
                         '(2)*(x*y*z+1)+(59)*(x)*(y)*(x*n-y*z)+(56)*(x)*(y+1)')

    def test_brackets_in_pow(self):
        p = '(x-y)^5'
        parser = Parser(p)
        self.assertEqual(parser._pow_opener(), '(x-y)*(x-y)*(x-y)*(x-y)*(x-y)')

    def test_brackets_in_pow2(self):
        p = '(x-y)^2*(x*y+1)^3'
        parser = Parser(p)
        self.assertEqual(parser
                         ._pow_opener(), '(x-y)*(x-y)*(x*y+1)*(x*y+1)*(x*y+1)')

    def test_brackets_in_pow3(self):
        p = '(x-y)^2+(z+5)^2'
        parser = Parser(p)
        self.assertEqual(parser._pow_opener(), '(x-y)*(x-y)+(z+5)*(z+5)')

    def test_mult_brackets(self):
        p = '(x-1)(y+xz)'
        parser = Parser(p)
        parser.txt = parser.parse_math_form_to_full_form()
        self.assertEqual(parser
                         ._brackets_multiplication(p), '(+x*y+x*xz-1*y-1*xz)')

    def test_mult_brackets2(self):
        p = '(x-1)(x+1)(y+z)'
        parser = Parser(p)
        parser.txt = parser.parse_math_form_to_full_form()
        parser.txt = parser._pow_opener()
        self.assertEqual(parser._brackets_opener(p),
                         '+x*x*y+x*x*z+x*1*y+x*1*z-1*x*y-1*x*z-1*1*y-1*1*z')

    def test_find_functions(self):
        p = 'sin(2x)+cos(x)'
        parser = Parser(p)
        self.assertEqual(parser._find_functions(), 'SIN[2X]+COS[X]')

    def test_find_functions2(self):
        p = 'log(2x)*sqrt(x)'
        parser = Parser(p)
        self.assertEqual(parser._find_functions(), 'LOG[2X]*SQRT[X]')

    def test_expand(self):
        p = '(xy+z)(x-1)'
        parser = Parser(p)
        self.assertEqual(parser.expand(), '+1.0*x**2*y-1.0*x*y+1.0*z*x-1.0*z')

    def test_expand2(self):
        p = 'sin(x)*cos(x)'
        parser = Parser(p)
        self.assertEqual(parser
                         .expand(), '+1.0*sin(x)cos(x)')


class PolynomialTest(unittest.TestCase):
    def test_many_brackets(self):
        one = '((x+y)(xy+z))(z+1)'
        two = 'x**2yz+x**2y+xy**2z+xy**2+xz**2+xz+yz**2+yz'
        self.assertTrue(Polynomial(one) == Polynomial(two))

    def test_many_brackets2(self):
        one = '(x+y+z)**2(y+7)**2(y+17-z)'
        two = 'x**2y**3-x**2y**2z+31x**2y**2-14x**2yz+287x**2y-' \
              '49x**2z+833x**2' \
              '+2xy**4+62xy**3-2xy**2z**2+34xy**2z+574xy**2' \
              '-28xyz**2+476xyz+' \
              '1666xy-98xz**2+1666xz+y**5+y**4z+31y**4-y**3z**2' \
              '+48y**3z+287y**3' \
              '-y**2z**3+3y**2z**2+525y**2z+833y**2-' \
              '14yz**3+189yz**2+1666yz-49z**3' \
              '+833z**2'
        self.assertTrue(Polynomial(one) == Polynomial(two))

    def test_many_brackets3(self):
        one = 'e(2.3x+5xy+1.9xyz)**2'
        two = '9.813x**2y**2z**2+51.6474x**2y**2z+' \
              '25ex**2y**2+23.7578x**2yz+62.5205x**2y+' \
              '14.3797x**2'
        self.assertTrue(Polynomial(one) == Polynomial(two))

    def test_equals(self):
        p1 = 'cos(x)'
        p2 = 'cos(-x)'
        pol1 = Polynomial(p1)
        pol2 = Polynomial(p2)
        self.assertTrue(pol1 == pol2)

    def test_equals2(self):
        p1 = 'x^2-1'
        p2 = '(x-1)(x+1)'
        pol1 = Polynomial(p1)
        pol2 = Polynomial(p2)
        self.assertTrue(pol1 == pol2)

    def test_equals3(self):
        p1 = 'xy(xz+1)'
        p2 = 'sqrt(x)'
        pol1 = Polynomial(p1)
        pol2 = Polynomial(p2)
        self.assertFalse(pol1 == pol2)

    def test_equals4(self):
        p1 = '(x+y+z)**2+sqrt(y)'
        p2 = '(x+y+z)(x+y+z)+sqrt(y)'
        pol1 = Polynomial(p1)
        pol2 = Polynomial(p2)
        self.assertTrue(pol1 == pol2)

    def test_equals5(self):
        p1 = 'xm+x+xym+xy+xyzm+xyz'
        p2 = '(x+xy+xyz)(m+1)'
        pol1 = Polynomial(p1)
        pol2 = Polynomial(p2)
        self.assertTrue(pol1 == pol2)

    def test_equals6(self):
        p1 = 'cos(x)sqrt(y)'
        p2 = 'cos(y)sqrt(x)'
        pol1 = Polynomial(p1)
        pol2 = Polynomial(p2)
        self.assertFalse(pol1 == pol2)

    def test_equals7(self):
        p1 = 'sin(x)**2+cos(x)**2'
        p2 = '1'
        pol1 = Polynomial(p1)
        pol2 = Polynomial(p2)
        self.assertTrue(pol1 == pol2)

    def test_equals8(self):
        p1 = 'sin(x)'
        p2 = 'sin(-x)'
        pol1 = Polynomial(p1)
        pol2 = Polynomial(p2)
        self.assertFalse(pol1 == pol2)

    def test_equals9(self):
        p1 = 'x**2+y**2'
        p2 = '(-x)**2+(-y)**2'
        pol1 = Polynomial(p1)
        pol2 = Polynomial(p2)
        self.assertTrue(pol1 == pol2)

    def test_equals10(self):
        p1 = 'x**3+3x**2+3x+1'
        p2 = '(x+1)**3'
        pol1 = Polynomial(p1)
        pol2 = Polynomial(p2)
        self.assertTrue(pol1 == pol2)


if __name__ == '__main__':
    unittest.main()
