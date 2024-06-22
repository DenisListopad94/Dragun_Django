import time

CACHE_FACTORIAL: dict = {}

''' result:
6 calculate
5 calculate
4 calculate
3 calculate
2 calculate
1 calculate
factorial(6):  720

6 from chache
factorial(6):  720

7 calculate
6 from chache
factorial(7):  5040

7 from chache
factorial(7):  5040
'''


def factorial(n: int) -> int:
    if n in CACHE_FACTORIAL:
        print(f'{n} from chache')
        return CACHE_FACTORIAL[n]
    else:
        print(f'{n} calculate')
        time.sleep(1)
        if n == 0 or n == 1:
            result = 1
        else:
            result: int = n * factorial(n - 1)

        CACHE_FACTORIAL[n] = result
        return result


print('factorial(6): ', factorial(6))
print('factorial(6): ', factorial(6))
print('factorial(7): ', factorial(7))
print('factorial(7): ', factorial(7))
