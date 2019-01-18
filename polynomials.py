from polynomial import *
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('first_polynomial', type=str,
                        help='Enter the first polynomial to comparison')
    parser.add_argument('second_polynomial', type=str,
                        help='Enter the second polynomial to comparison')

    parse = parser.parse_args()

    polynomial_one = Polynomial(parse.first_polynomial)
    polynomial_two = Polynomial(parse.second_polynomial)
    if polynomial_one == polynomial_two:
        print('Многочлены равны')
    else:
        print('Многочлены не равны')


if __name__ == '__main__':
    main()
