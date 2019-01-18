import re


class ExceptionChecker(Exception):
    def __init__(self, text):
        self.txt = text

    def _is_correct_bracket_seq(self):
        """Проверка на корректную скобочную последовательность"""
        pairs = dict()
        pairs.update({'(': ')'})
        stack = list()
        for i in self.txt:
            if i in pairs.keys():
                stack.append(i)
            elif i in pairs.values():
                if len(stack) == 0 or pairs[stack.pop()] != i:
                    return False
            else:
                continue
        return len(stack) == 0

    def _is_corrector_input_symbols(self):
        """Проверка на вхождение недопустимых символов"""
        str_without_spaces = self.txt.replace(' ', '')
        digits = re.findall(r'[0-9]', self.txt)
        variables = re.findall(r'[a-z]', self.txt)
        operations = ['+', '-', '^', '(', ')', '*', '/', '.']
        for e in str_without_spaces:
            if e not in digits and\
                    (e not in variables and e not in operations):
                return False
        return True

    def _is_correct_polynomial(self):
        """Проверка на корректность математических операций"""
        digits = re.findall(r'[0-9]', self.txt)
        variables = re.findall(r'[a-z]', self.txt)
        operations = ['+', '-', '*', '/']
        len_of_str = len(self.txt)
        if self.txt[-1] in operations or self.txt[-1] == '^':
            return False
        for i in range(len_of_str - 1):
            if self.txt[i] == '^' and self.txt[i + 1] not in digits or\
                    (self.txt[i] in operations and
                     (self.txt[i + 1] not in variables) and
                     (self.txt[i + 1] not in digits) and
                     (self.txt[i + 1] != '*') and
                     (self.txt[i + 1] != '(')):
                return False
        return True

    def is_correct(self):
        if not self._is_correct_bracket_seq():
            raise SyntaxError('Не корректная скобочная последовательность')
        elif not self._is_corrector_input_symbols():
            raise SyntaxError('Не допустимые символы')
        elif not self._is_correct_polynomial():
            raise SyntaxError('Не корректный многочлен')
        else:
            return True
