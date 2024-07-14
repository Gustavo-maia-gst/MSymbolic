from exponential import Exponential, Logarithm
from symbols import Constant, Variable, ZERO, EULER, PI
from trigonometric import Sine, Cosine

from collections import deque
from sys import exit
from typing import *

class Cradle:
    solvers = {}
    def __init__(self, input: str):
        self._buffer = deque(input.replace(' ', ''))
        pass

    def _getch(self) -> str:
        return self._buffer.popleft()

    def look(self) -> str:
        if not self._buffer: return
        return self._buffer[0]
    
    def match(self, ch, validator: Callable = lambda ch, c: c == ch) -> bool:
        return validator(self._getch(), ch)
    
    def error(self, msg) -> None:
        print(f"\033[31mError: {msg}\033[0m")
        exit(1)

    def expected(self, msg, got = None) -> None:
        print(f"\033[31mExpected: {msg}{f', got: {got}' if got else ''}\033[0m")
        exit(1)
    
    def _getValidated(self, validator: Callable, expected: str) -> str:
        ch = self._getch()
        if not validator(ch):
            self.expected(expected, ch)
        return ch
    
    def getch(self) -> str:
        return self._getValidated(lambda ch: ch.isalpha(), "char")
    
    def getnum(self) -> int:
        number = 0
        while self.look() and self.look().isdigit():
            number = 10 * number + int(self._getch())
        return number
    
    def getname(self) -> str:
        name = self.getch()
        while self.look() and self.look().isalnum():
            name += self._getch()
        return name

def solver(ch: str):
    def dec(func):
        def new_func(self, base):
            self.cradle.match(ch)
            return func(self, base)

        if ch in Cradle.solvers:
            raise Exception(f'Solver for {ch} already registered ({Cradle.solvers[ch]})')
        Cradle.solvers[ch] = new_func

        return new_func
    return dec

class Assembler:
    def __init__(self, input: str):
        self.cradle = Cradle(input)
        self.code = []
        self.func_mapper = {
            'sin': Sine,
            'cos': Cosine,
            'ln': Logarithm
        }
        self.const_mapper = {
            'π': PI,
            'e': EULER
        }
    
    def get_symbol(self):
        name = self.cradle.getname()

        if name == 'x':
            return Variable()

        if self.cradle.look() == '(':
            if name not in self.func_mapper:
                print(f'Unknown function: {name}')
                
            func = self.func_mapper[name]
            self.cradle.match('(')
            param = self.expr()
            self.cradle.match(')')
            return func(param)
        
        raise Exception(f'Unknown name: {name}')
    
    def factor(self):
        looked = self.cradle.look()
        if looked in self.const_mapper:
            return self.const_mapper[self.cradle._getch()]
            
        if looked == '(':
            self.cradle.match('(')
            expr = self.expr()
            self.cradle.match(')')
            return expr

        if looked.isdigit():
            return Constant(self.cradle.getnum())

        if looked.isalpha():
            return self.get_symbol()
    
    def pot(self):
        base = self.factor()
        op = self.cradle.look()
        while op in ['^']:
            solver = self.cradle.solvers[op]
            base = solver(self, base)
            op = self.cradle.look()
        return base
    
    def term(self):
        base = self.pot()
        op = self.cradle.look()
        while op in ['*', '/']:
            solver = self.cradle.solvers[op]
            base = solver(self, base)
            op = self.cradle.look()
        return base
    
    def expr(self):
        if self.cradle.look() in ['+', '-']:
            base = Constant(0)
        else:
            base = self.term()

        op = self.cradle.look()
        while op in ['+', '-']:
            solver = self.cradle.solvers[op]
            base = solver(self, base)
            op = self.cradle.look()
        return base
    
    @solver('+')
    def add(self, base):
        return base + self.term()
    
    @solver('-')
    def sub(self, base):
        return base - self.term()
    
    @solver('*')
    def mult(self, base):
        return base * self.pot()
    
    @solver('/')
    def div(self, base):
        return base / self.pot()
    
    @solver('^')
    def pow(self, base):
        return Exponential(base, self.pot())
    
if __name__ == '__main__':
    assembler = Assembler(input("Put in your function: "))
    expr = assembler.expr()
    print(f'Parsed: {expr}')