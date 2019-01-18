from polynomial_exceptions import *

elementary_function = ['acos', 'asin', 'atan', 'log', 'sqrt',
                       'cos', 'sin', 'tan', 'pi', 'e']


class Parser(ExceptionChecker):
    def __init__(self, polynomial):
        self.txt = str(polynomial).replace(' ', '').replace('**', '^')
        super().__init__(polynomial)

    @staticmethod
    def _brackets_pairs_finder(string, open_s, close_s):
        """Search all pairs open and close brackets"""
        brackets_dict = dict()
        open_brackets = list()
        for i in range(len(string)):
            if string[i] == open_s:
                open_brackets.append(i)
            if string[i] == close_s:
                index_of_open = open_brackets.pop()
                brackets_dict[index_of_open] = i
        return brackets_dict

    @staticmethod
    def _string_priorities(string, open_brackets_priorities):
        """Calculate priority of strings"""
        priority = int()
        max_priority = int()
        for i in range(len(string)):
            if string[i] == '(':
                priority += 1
                if priority > max_priority:
                    max_priority = priority
                open_brackets_priorities[i] = priority
            if string[i] == ')':
                priority -= 1
        return max_priority

    def expand(self):
        self.is_correct()
        self.txt = self.parse_math_form_to_full_form()
        self.txt = self._pow_opener()
        self.txt = self._get_monomial_in_bracket()
        self.txt = self._brackets_opener(self.txt)
        self.txt = self._pow_maker()
        self.txt = self.get_function()
        return self.txt

    def get_max_power(self):
        """Find polynomial's deg"""
        self.txt = Parser(self.txt).expand()
        powers = re.findall(r'\^[0-9]+', self.txt)
        max_power = 1
        for e in powers:
            if int(e[1:]) > max_power:
                max_power = int(e[1:])
        return max_power

    def get_variables(self):
        string = self._find_functions()
        symbols = re.findall(r'[a-z]', string)
        brackets = self._brackets_pairs_finder(string, '[', ']')
        for e in brackets:
            vars = string[e+1:brackets[e]]
            for v in vars:
                if not v.isdigit() and v != '*' and v != '-':
                    symbols.append(v.lower())
        return symbols

    def get_function(self):
        """Return to good record of function"""
        self.txt = str(self.txt)
        for e in elementary_function:
            find = self.find_all(e.upper())
            if len(find) > 0:
                for i in find:
                    position = i
                    new_position = self._replace_functions(e.upper(), position)
                    replace_sub_str = self.txt[position:new_position]
                    self.txt = self.txt.replace(replace_sub_str,
                                                replace_sub_str.
                                                replace('[', '(').
                                                replace(']', ')').lower())
        return self.txt

    def parse_math_form_to_full_form(self):
        """Give polynomial to full record"""
        self._find_functions()
        result = ''
        len_of_str = len(self.txt)
        symbols = re.findall(r'[a-z]', self.txt)
        for i in range(len_of_str):
            if i == 0:
                result += self.txt[i]
            elif self._is_abbreviated_entry(i, i - 1, symbols):
                result += '*' + self.txt[i]
            else:
                result += self.txt[i]
        self.txt = result.replace(' ', '')
        return self.txt

    def _is_abbreviated_entry(self, c, p, symbols):
        """Check for abbreviated entry"""
        return (self.txt[p] in symbols and self.txt[c] in symbols) or \
               (self.txt[p] == ')' and self.txt[c] == '(') or \
               (self.txt[p].isdigit() and self.txt[c] == '(') or \
               (self.txt[p] == ')' and self.txt[c].isalpha()) or \
               (self.txt[p].isdigit() and self.txt[c].isalpha()) or \
               (self.txt[p].isalpha() and self.txt[c].isdigit()) or \
               (self.txt[p].isalpha() and self.txt[c] == '(') or \
               (self.txt[p] == ')' and self.txt[c].isdigit()) or\
               (self.txt[p] == ']' and self.txt[c] == '[') or\
               (self.txt[p] == ']' and self.txt[c].isdigit()) or \
               (self.txt[p] == ']' and self.txt[c].isalpha()) or \
               (self.txt[p] == ']' and self.txt[c] == '(') or \
               (self.txt[p] == ')' and self.txt[c] == '[') or \
               (self.txt[p].isupper() and self.txt[c].islower()) or \
               (self.txt[p].islower() and self.txt[c].isupper())

    def _get_monomial_in_bracket(self):
        """Give constant into brackets"""
        brackets_dict = self._brackets_pairs_finder(self.txt, '(', ')')
        if len(brackets_dict) == 0:
            return self.txt
        numbers_in_brackets = list()
        for key, value in brackets_dict.items():
            counter = key
            while counter <= value:
                numbers_in_brackets.append(counter)
                counter += 1
        i = 0
        count = 0
        begin_end = dict()
        while i < len(self.txt):
            if (self.txt[i].isdigit() or self.txt[i].isalpha())\
                    and i not in numbers_in_brackets:
                begin = i + count
                while i < len(self.txt) and \
                        (self.txt[i].isdigit() or
                         self.txt[i].isalpha() or self.txt == '*'):
                    i += 1
                begin_end[begin] = i - 1 + count
                count += 2
                continue
            i += 1
        for k, v in begin_end.items():
            self.txt = self.txt[:k] + '(' \
                       + self.txt[k:v + 1] + ')' + self.txt[v+1:]
        return self.txt

    def _pow_opener(self):
        """Write deg as multiplier"""
        brackets_dict = self._brackets_pairs_finder(self.txt, '(', ')')
        if len(brackets_dict) == 0:
            return self.txt
        strings_before_changes = list()
        strings_after_changes = list()
        for key, value in brackets_dict.items():
            if value + 1 == len(self.txt):
                break
            if self.txt[value + 1] == '^':
                expression = self.txt[key:value + 1]
                digit = self.txt[value + 2]
                index = value + 2
                number = ''
                while digit not in ['+', '-', '*']:
                    number += self.txt[index]
                    index += 1
                    if index == len(self.txt):
                        break
                    digit = self.txt[index]
                expression_in_pow = expression
                for i in range(int(number) - 1):
                    expression_in_pow += '*' + expression
                strings_before_changes.append(self.txt[key:index])
                strings_after_changes.append(expression_in_pow)
        for i in range(len(
                strings_before_changes)):
            self.txt = self.txt.replace(
                strings_before_changes[i], strings_after_changes[i])
        return self.txt

    def _brackets_multiplication(self, string):
        """Multiplication of two brackets"""
        brackets_dict = self._brackets_pairs_finder(string, '(', ')')
        if len(brackets_dict) == 0:
            return self.txt
        two_expressions = ''
        for key, value in brackets_dict.items():
            expression = string[key + 1:value]
            if expression[0] not in ['+', '-']:
                two_expressions += '+' + expression + ' '
            else:
                two_expressions += expression + ' '
        multiplication_list = two_expressions[:-1].split(' ')
        if len(multiplication_list) == 2:
            first_bracket = multiplication_list[0].replace('+', '%+')\
                .replace('-', '%-').split('%')
            second_bracket = multiplication_list[1].replace('+', '%+')\
                .replace('-', '%-').split('%')
            first_bracket.pop(0)
            second_bracket.pop(0)
            output_string = ''
            for a in first_bracket:
                for b in second_bracket:
                    if a[0] == '-' and b[0] == '-' \
                            or a[0] == '+' and b[0] == '+':
                        output_string += '+' + a[1:] + '*' + b[1:]
                    else:
                        output_string += '-' + a[1:] + '*' + b[1:]
            return '(' + output_string + ')'

    def _brackets_opener(self, s):
        """Expand the brackets expression"""
        exit_checker = int()
        for symbol in s:
            if symbol == '(':
                exit_checker += 1
        if exit_checker < 2:
            if exit_checker == 1:
                self.txt = s[1:-1]
            return self.txt
        brackets_dict = self._brackets_pairs_finder(s, '(', ')')
        if len(brackets_dict) == 0:
            return self.txt
        open_brackets_priorities = dict()
        max_priority = self._string_priorities(
            s, open_brackets_priorities)
        op_br = list(brackets_dict.keys())
        cl_br = list(brackets_dict.values())
        for i in range(1, len(op_br)):
            if op_br[i] + 1 == op_br[i - 1] and cl_br[i] - 1 == cl_br[i - 1]:
                return self._brackets_opener(
                    s[:op_br[i - 1]] +
                    s[op_br[i - 1] + 1:cl_br[i - 1]] +
                    s[cl_br[i - 1] + 1:])
            i += 1
        prev_value = prev_key = -1
        this_k = ''
        biggest_priority_str = ''
        for k in brackets_dict.keys():
            if open_brackets_priorities[k] == prev_value == max_priority:
                biggest_priority_str = s[prev_key:brackets_dict[k] + 1]
                this_k = k
                break
            prev_value = open_brackets_priorities[k]
            prev_key = k
        if brackets_dict[prev_key] + 2 == this_k:
            if s[this_k - 1] in ['+', '-']:
                return self._brackets_opener(
                    s[:this_k - 2] + s[this_k - 1] + s[this_k + 1:])
        return self._brackets_opener(
            s.replace(biggest_priority_str,
                      self._brackets_multiplication(biggest_priority_str), 1))

    def _pow_maker(self):
        """Same multiplier into deg"""
        if '**' in self.txt:
            return self.txt
        if self.txt[0] != '+' and self.txt[0] != '-':
            self.txt = '+' + self.txt
        monomials = self.txt.replace('+', '%+').replace('-', '%-').split('%')
        if monomials[0] == '':
            monomials.pop(0)
        all_monomials = ''
        m = ''
        for monomial in monomials:
            double_part = 1.0
            string_part = dict()
            i = 0
            while i < len(monomial):
                new_number = ''
                if monomial[i].isdigit() and len(m) == 0:
                    while i < len(monomial) and\
                            (monomial[i].isdigit() or monomial[i] == '.'):
                        new_number += monomial[i]
                        i += 1
                    double_part *= float(new_number)
                    continue
                if monomial[i].isalpha() or \
                        (monomial[i].isdigit() and len(m) > 0) \
                        or monomial[i] == '[' or monomial[i] == ']':
                    if monomial[i] == monomial[i].upper() or \
                            monomial[i].isdigit() \
                            or monomial[i] == '[' \
                            or monomial[i] == ']':
                        m += monomial[i]
                    elif monomial[i] not in string_part:
                        string_part[monomial[i]] = 1
                    else:
                        string_part[monomial[i]] += 1
                i += 1
            if len(m) != 0:
                string_part[m] = 1
                m = ''
            monomial_string = monomial[0] + double_part .__str__()
            for key, value in string_part.items():
                if string_part[key] != 1:
                    monomial_string += f'*{key}^{value}'
                else:
                    monomial_string += f'*{key}'
            all_monomials += monomial_string
        return all_monomials.replace('^', '**')

    def _replace_functions(self, func, position):
        """Replacement of functions"""
        self.txt = str(self.txt)
        new_position = position
        for sym in self.txt[position:]:
            if sym == ')' or sym == ']':
                new_position += 1
                break
            new_position += 1
        return new_position

    def find_all(self, sub):
        start = 0
        result = list()
        while True:
            start = self.txt.find(sub, start)
            if start == -1:
                break
            result.append(start)
            start += len(sub)
        return result

    def _find_functions(self):
        """Check for elementary functions"""
        self.txt = str(self.txt)
        self.txt = self.txt.replace('tg', 'tan')\
            .replace('arcsin', 'asin')\
            .replace('arccos', 'acos')\
            .replace('arctg', 'atan')
        for e in elementary_function:
            if e == 'pi' or e == 'e':
                self.txt = self.txt.replace(e, e.upper())
                continue
            find = self.find_all(e)
            if len(find) > 0:
                for i in find:
                    position = i
                    new_position = self._replace_functions(e, position)
                    replace_sub_str = self.txt[position:new_position]
                    self.txt = self.txt.replace(replace_sub_str,
                                                replace_sub_str
                                                .replace('(', '[')
                                                .replace(')', ']').upper())
        return self.txt
