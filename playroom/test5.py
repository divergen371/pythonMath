import math


def my_func(x: int) -> int:
    if x == 0:
        return 0
    else:
        return x + my_func(x - 1)


def fib(x: int) -> int:
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return fib(x - 1) + fib(x - 2)


def find_divisors(num: int) -> list:
    divisors = []
    for i in range(1, int(math.sqrt(num)) + 1):
        if num % i == 0:
            divisors.append(i)
            if i != num // i:
                divisors.append(num // i)
    return divisors


print(find_divisors(100))
print(my_func(5))
