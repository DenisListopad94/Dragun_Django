from functools import lru_cache


@lru_cache(maxsize=None)
def sum_positive(numbers: tuple) -> int:
    print('inside sum_positive: ', numbers)

    if len(numbers) == 0:
        return 0
    if numbers[0] > 0:
        return numbers[0] + sum_positive(numbers[1:])
    else:
        return sum_positive(numbers[1:])


numbers: list[int] = [1, -2, 3, 4, -5, 6]

# lru_cache кэширует картежи
print('sum_positive-1: ', sum_positive(tuple(numbers)))
# при повтором вызове результат получаем из кэша
print('sum_positive-2: ', sum_positive(tuple(numbers)))
