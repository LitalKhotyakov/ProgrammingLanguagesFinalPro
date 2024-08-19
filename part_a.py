
import re
import math

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def variable(self):
        result = ''
        while self.current_char is not None and re.match(r'[a-zA-Z_]', self.current_char):
            result += self.current_char
            self.advance()
        return result

    def number(self):
        result = ''
        while self.current_char is not None and re.match(r'[0-9]', self.current_char):
            result += self.current_char
            self.advance()
        return int(result)

    def parse(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if re.match(r'[a-zA-Z_]', self.current_char):
                var = self.variable()
                if var == 'factorial':
                    tokens.append('FACTORIAL')
                elif var == 'Lambd':
                    tokens.append('LAMBDA')
                else:
                    tokens.append(var)
                continue
            if re.match(r'[0-9]', self.current_char):
                tokens.append(self.number())
                continue
            if self.current_char in '+-*/%()':
                tokens.append(self.current_char)
                self.advance()
                continue
            if self.current_char == '=' and self.peek() == '=':
                tokens.append('==')
                self.advance()
                self.advance()
                continue
            if self.current_char == '>' and self.peek() == '=':
                tokens.append('>=')
                self.advance()
                self.advance()
                continue
            if self.current_char == '<' and self.peek() == '=':
                tokens.append('<=')
                self.advance()
                self.advance()
                continue
            if self.current_char == '>' or self.current_char == '<':
                tokens.append(self.current_char)
                self.advance()
                continue
            if self.current_char == '&' and self.peek() == '&':
                tokens.append('&&')
                self.advance()
                self.advance()
                continue
            if self.current_char == '|' and self.peek() == '|':
                tokens.append('||')
                self.advance()
                self.advance()
                continue
            if self.current_char == '!':
                tokens.append('!')
                self.advance()
                continue
            if self.current_char == '.':
                tokens.append('.')
                self.advance()
                continue
            if self.current_char == '{' or self.current_char == '}':
                tokens.append(self.current_char)
                self.advance()
                continue
            if self.current_char == ',':
                tokens.append(',')
                self.advance()
                continue
            self.error()
        return tokens

    def peek(self):
        if self.pos + 1 < len(self.text):
            return self.text[self.pos + 1]
        return None


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def error(self):
        raise Exception('Invalid syntax')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.tokens) - 1:
            self.current_token = None
        else:
            self.current_token = self.tokens[self.pos]

    def factor(self):
        token = self.current_token
        if isinstance(token, int):
            self.advance()
            return token
        if token == '(':
            self.advance()
            result = self.boolean_expr()
            if self.current_token == ')':
                self.advance()
                return result
            else:
                self.error()
        if token == 'FACTORIAL':
            self.advance()
            if self.current_token == '(':
                self.advance()
                result = self.boolean_expr()
                if self.current_token == ')':
                    self.advance()
                    return math.factorial(result)
                else:
                    self.error()
            self.error()
        if token == 'LAMBDA':
            return self.lambda_expr()
        if isinstance(token, str):
            self.advance()
            return token
        self.error()

    def lambda_expr(self):
        self.advance()  # skip 'LAMBDA'
        if not isinstance(self.current_token, str):
            self.error()
        arg = self.current_token
        self.advance()  # skip argument
        if self.current_token != '.':
            self.error()
        self.advance()  # skip '.'
        body = self.boolean_expr()
        return ('lambda', arg, body)

    def term(self):
        result = self.factor()
        while self.current_token is not None and self.current_token in '*/%':
            op = self.current_token
            self.advance()
            if op == '*':
                result *= self.factor()
            elif op == '/':
                result //= self.factor()
            elif op == '%':
                result %= self.factor()
        return result

    def expr(self):
        result = self.term()
        while self.current_token is not None and self.current_token in '+-':
            op = self.current_token
            self.advance()
            if op == '+':
                result += self.term()
            elif op == '-':
                result -= self.term()
        return result

    def comparison(self):
        left = self.expr()
        if self.current_token in ('==', '!=', '>', '<', '>=', '<='):
            op = self.current_token
            self.advance()
            right = self.expr()
            if op == '==':
                return left == right
            elif op == '!=':
                return left != right
            elif op == '>':
                return left > right
            elif op == '<':
                return left < right
            elif op == '>=':
                return left >= right
            elif op == '<=':
                return left <= right
        return left

    def boolean_expr(self):
        result = self.comparison()
        while self.current_token in ('&&', '||'):
            op = self.current_token
            self.advance()
            right = self.comparison()
            if op == '&&':
                result = result and right
            elif op == '||':
                result = result or right
        return result

    def parse(self):
        result = self.boolean_expr()
        while self.current_token is not None:
            if self.current_token == '(':
                self.advance()  # skip '('
                arg_val = self.boolean_expr()
                if self.current_token == ')':
                    self.advance()  # skip ')'
                    result = ('apply', result, arg_val)
                else:
                    self.error()
            else:
                break
        return result


class Interpreter:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.tokens = self.lexer.parse()
        self.parser = Parser(self.tokens)

    def eval_expr(self, expr, env={}):
        if isinstance(expr, int):
            return expr
        if isinstance(expr, bool):
            return expr
        if isinstance(expr, str):
            if expr in env:
                return env[expr]
            else:
                raise Exception(f"Undefined variable: {expr}")
        if isinstance(expr, tuple):
            if expr[0] == 'lambda':
                return expr
            elif expr[0] == 'apply':
                lambda_expr = self.eval_expr(expr[1], env)
                arg_val = self.eval_expr(expr[2], env)
                return self.interpret_lambda(lambda_expr, arg_val, env)
        raise Exception(f"Invalid expression: {expr}")

    def interpret_lambda(self, lambda_expr, arg_val, env):
        _, arg, body = lambda_expr
        local_env = env.copy()
        local_env[arg] = arg_val
        return self.eval_expr(body, local_env)

    def interpret(self):
        return self.eval_expr(self.parser.parse())


def test_interpreter(text):
    try:
        interpreter = Interpreter(text)
        result = interpreter.interpret()
        return result
    except Exception as e:
        return f"Error: {e}"

# Test cases
print("Result for '3 + 5 * (2 - 8)':", test_interpreter("3 + 5 * (2 - 8)"))  # Should output -27
print("Result for '10 / 2 + 3':", test_interpreter("10 / 2 + 3"))  # Should output 8
print("Result for '5 * 3 + 8 / 4':", test_interpreter("5 * 3 + 8 / 4"))  # Should output 17
print("Result for '(3 + 2) * (7 - 5)':", test_interpreter("(3 + 2) * (7 - 5)"))  # Should output 10
print("Result for '8 % 3 + 2':", test_interpreter("8 % 3 + 2"))  # Should output 4
print("Result for '10 / (2 + 3)':", test_interpreter("10 / (2 + 3)"))  # Should output 2
print("Result for '3 + (2 * (4 - 1))':", test_interpreter("3 + (2 * (4 - 1))"))  # Should output 9
print("Result for '10 - 5 * 2 + 1':", test_interpreter("10 - 5 * 2 + 1"))  # Should output 1
print("Result for '(6 + 2) * (3 - 1)':", test_interpreter("(6 + 2) * (3 - 1)"))  # Should output 16
print("Result for '5 + 3 * 2 - 4 / 2':", test_interpreter("5 + 3 * 2 - 4 / 2"))  # Should output 9
print("Result for '2 * (3 + 4) - 5':", test_interpreter("2 * (3 + 4) - 5"))  # Should output 9
print("Result for '7 - (4 / 2) * 3':", test_interpreter("7 - (4 / 2) * 3"))  # Should output 1

# Boolean test cases
print("Result for '(3 > 0) && (5 < 10)':", test_interpreter("(3 > 0) && (5 < 10)"))  # Should output True
print("Result for '(3 > 0) || (5 > 10)':", test_interpreter("(3 > 0) || (5 > 10)"))  # Should output True
print("Result for '(3 < 0) && (5 < 10)':", test_interpreter("(3 < 0) && (5 < 10)"))  # Should output False
print("Result for '(3 < 0) || (5 < 10)':", test_interpreter("(3 < 0) || (5 < 10)"))  # Should output True

# Factorial test cases
print("Result for 'factorial(5)':", test_interpreter("factorial(5)"))  # Should output 120
print("Result for 'factorial(3)':", test_interpreter("factorial(3)"))  # Should output 6
print("Result for 'factorial(0)':", test_interpreter("factorial(0)"))  # Should output 1
print("Result for 'factorial(7)':", test_interpreter("factorial(7)"))  # Should output 5040

# # Lambda expression test cases
# print("Result for '(Lambd x.(Lambd y. (x + y))) (3) (4)':", test_interpreter("(Lambd x.(Lambd y. (x + y))) (3) (4)"))  # Should output 7
# print("Result for '(Lambd x.(Lambd y. (x * y))) (5) (2)':", test_interpreter("(Lambd x.(Lambd y. (x * y))) (5) (2)"))  # Should output 10
# print("Result for '(Lambd x.(Lambd y. (x - y))) (7) (3)':", test_interpreter("(Lambd x.(Lambd y. (x - y))) (7) (3)"))  # Should output 4
# print("Result for '(Lambd x.(Lambd y. (x / y))) (8) (2)':", test_interpreter("(Lambd x.(Lambd y. (x / y))) (8) (2)"))  # Should output 4
# print("Result for '(Lambd x.(Lambd y. (x % y))) (9) (4)':", test_interpreter("(Lambd x.(Lambd y. (x % y))) (9) (4)"))  # Should output 1

