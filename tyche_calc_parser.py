import re

class Calculator:
    def __init__(self, tokens):
        self._tokens = tokens
        self._current = tokens[0]

    def exp(self):
        result = self.term()
        while self._current in ('+', '-'):
            if self._current == '+':
                self.next()
                result += self.term()
            if self._current == '-':
                self.next()
                result -= self.term()
        return result

    def term(self):
        result = self.factor()
        while self._current in ('*', '/'):
            if self._current == '*':
                self.next()
                result *= self.term()
            if self._current == '/':
                self.next()
                result /= self.term()
        return result

    def factor(self):
        result = None
        if self._current[0].isdigit():
            result = int(self._current)
            self.next()
        elif self._current is '+':
            self.next()
            result = self.factor()
        elif self._current is '-':
            self.next()
            result = -self.factor()
        elif self._current is '(':
            self.next()
            result = self.exp()
            self.next()
        return result

    def next(self):
        self._tokens = self._tokens[1:]
        self._current = self._tokens[0] if len(self._tokens) > 0 else None


def evaluate(expr):
    expr = expr.replace(r'^\s+', '')

    def remove_unmatched_from_pair(repl):
        return repl.group(1) + repl.group(2)

    expr = re.sub(r'([+-/*(]+)\s+([+-/*(]+)', remove_unmatched_from_pair, expr)
    expr = re.sub(r'([+-/*)]+)\s+([+-/*)]+)', remove_unmatched_from_pair, expr)
    expr = re.sub(r'([+-/*(])\s+([\d+])', remove_unmatched_from_pair, expr)
    expr = re.sub(r'([\d+])\s+([+-/*)])', remove_unmatched_from_pair, expr)

    def calculate(repl):
        calculate_tokens = re.findall(r'[\d.]+|[+-/*()]', repl.group(0))
        return str(Calculator(calculate_tokens).exp())

    result = re.sub('[\d+-/*()]+', calculate, expr)
    return result
