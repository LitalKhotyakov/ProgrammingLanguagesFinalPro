

fibonacci = lambda n: [int((((1 + 5**0.5) / 2)**i - ((1 - 5**0.5) / 2)**i) / 5**0.5) for i in range(n)]

print(fibonacci(10))

concat_strings = lambda lst: reduce(lambda x, y: x + ' ' + y, lst)
from functools import reduce
print(concat_strings(["Hello", "world", "this", "is", "Python"]))

cumulative_sum_squares = lambda lst: list(map(lambda sub: sum(map(lambda x: x**2, filter(lambda x: x % 2 == 0, sub))), lst))
print(cumulative_sum_squares([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

cumulative_op = lambda op: lambda seq: reduce(op, seq)
from functools import reduce

factorial = cumulative_op(lambda x, y: x * y)
print(factorial(range(1, 6)))  # 5!

exponentiation = cumulative_op(lambda x, y: x ** y)
print(exponentiation([2, 3]))  # 2^3

from functools import reduce

print(reduce(lambda x, y: x + y, map(lambda x: x**2, filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6]))))

count_palindromes = lambda lst: list(map(lambda sub: reduce(lambda acc, x: acc + 1, filter(lambda x: x == x[::-1], sub), 0), lst))
print(count_palindromes([["madam", "test"], ["racecar", "hello", "level"], ["world","POP"]]))

def generate_values():
    print('Generating values...')
    yield 1
    yield 2
    yield 3

def square(x):
    print(f'Squaring {x}')
    return x * x

print('Eager evaluation:')
values = list(generate_values())
squared_values = [square(x) for x in values]
print(squared_values)

print('\nLazy evaluation:')
squared_values = [square(x) for x in generate_values()]
print(squared_values)

is_prime = lambda x: x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1))
sorted_primes = lambda lst: sorted([x for x in lst if is_prime(x)], reverse=True)
print(sorted_primes([2, 3, 4, 5, 6, 7, 8, 9, 10]))