
# Part B, Section 1: Generating Fibonacci sequence
# This lambda expression generates the Fibonacci sequence up to n terms
fibonacci = lambda n: [int((((1 + 5**0.5) / 2)**i - ((1 - 5**0.5) / 2)**i) / 5**0.5) for i in range(n)]
print(fibonacci(10))

concat_strings = lambda lst: reduce(lambda x, y: x + ' ' + y, lst)
from functools import reduce
fibonacci = lambda n: [int((((1 + 5**0.5) / 2)**i - ((1 - 5**0.5) / 2)**i) / 5**0.5) for i in range(n)]

print(fibonacci(10))
# Part B, Section 2: Concatenating strings with a space using lambda
# This lambda expression concatenates all strings in a list with a space between them
concat_strings = lambda lst: reduce(lambda x, y: x + ' ' + y, lst)
from functools import reduce
print(concat_strings(["Hello", "world", "this", "is", "Python"]))

# Part B, Section 3: Cumulative sum of squares of even numbers using nested lambda expressions
# This lambda expression computes the cumulative sum of squares of even numbers in each sublist
cumulative_sum_squares = lambda lst: list(map(lambda sub: sum(map(lambda x: x**2, filter(lambda x: x % 2 == 0, sub))), lst))
print(cumulative_sum_squares([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

# Part B, Section 4: Higher-order function to apply a binary operation cumulatively
# This higher-order lambda function applies a binary operation cumulatively to a sequence of values
cumulative_op = lambda op: lambda seq: reduce(op, seq)
from functools import reduce

# Factorial using the higher-order function
# Computes the factorial of a number using the cumulative_op function
factorial = cumulative_op(lambda x, y: x * y)
print(factorial(range(1, 6)))  # 5!

# Exponentiation using the higher-order function
# Computes the exponentiation of a number using the cumulative_op function
exponentiation = cumulative_op(lambda x, y: x ** y)
print(exponentiation([2, 3]))  # 2^3

from functools import reduce

# Part B, Section 5: Rewriting a loop using lambda, filter, map, and reduce
# This lambda expression rewrites a loop to sum the squares of even numbers using filter, map, and reduce
print(reduce(lambda x, y: x + y, map(lambda x: x**2, filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6]))))


# Part B, Section 6: Counting palindromes in a list of lists using lambda
# This lambda expression counts the number of palindromes in each sublist
count_palindromes = lambda lst: list(map(lambda sub: reduce(lambda acc, x: acc + 1, filter(lambda x: x == x[::-1], sub), 0), lst))
print(count_palindromes([["madam", "test"], ["racecar", "hello", "level"], ["world","POP"]]))

# Part B, Section 7: Lazy evaluation demonstration
# This part of the program demonstrates lazy evaluation using Python's generator functions
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

# Part B, Section 8: Sorting prime numbers in descending order using lambda
# This lambda expression sorts prime numbers in descending order
is_prime = lambda x: x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1))
sorted_primes = lambda lst: sorted([x for x in lst if is_prime(x)], reverse=True)
print(sorted_primes([2, 3, 4, 5, 6, 7, 8, 9, 10]))
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