from parser import *
import copy
from math import *


class Polynomial:
    def __init__(self, polynomial):
        self.p = polynomial

    def __eq__(self, other):
        power_of_one = Parser(self.p).get_max_power() + 1
        power_of_two = Parser(other.p).get_max_power() + 1
        power = max(power_of_one, power_of_two)
        self.p = Parser(self.p).parse_math_form_to_full_form()
        self.p = Parser(self.p).get_function()
        other.p = Parser(other.p).parse_math_form_to_full_form()
        other.p = Parser(other.p).get_function()
        copy_f = copy.copy(self.p)
        copy_s = copy.copy(other.p)
        var_one = list(set(Parser(self.p).get_variables()))
        n = 1
        for i in range(power):
            for j in var_one:
                self.p = self.p.replace(j, str(n))
                other.p = other.p.replace(j, str(n))
                n += 1
            try:
                one = round(eval(self.p), 2)
                two = round(eval(other.p), 2)
            except NameError:
                return False
            if (self.p.isdigit() and
                round(float(self.p)) == round(float(two))) or\
                    (other.p.isdigit() and
                     round(float(other.p)) == round(float(one))):
                n = 31 * n
                self.p = copy.copy(copy_f)
                other.p = copy.copy(copy_s)
            if one != two:
                return False
        return True
