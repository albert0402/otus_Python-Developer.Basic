# Функция, которая принимает N целых чисел и возвращает список квадратов этих чисел
def power_numbers(*args):
    new_list = [i**2 for i in args]
    return new_list

# Проверка на четность
def is_even(number):
    return number % 2 == 0

# Проверка на нечётность
def is_odd(number):
    return number % 2 != 0

# Проверка на простоту
def is_prime(number):
    return number > 1 and all(number % i != 0 for i in range(2, int(number**0.5) + 1))

# Функция, которая на вход принимает список из целых чисел, и возвращает только
# чётные/нечётные/простые числа (выбор производится передачей дополнительного аргумента)
def filter_numbers(*args):
    numbers = args[0]
    function = args[1]
    func = {"ODD": is_odd, "EVEN": is_even, "PRIME": is_prime}
    return [num for num in numbers if func[function](num)]