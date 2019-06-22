# Python version: 3.7


import math


def sqr(x):
    return x*x


def break_comma(exp: str):
    """
    Делит выражение на запятые, если они не лежат внутри внутренней скобочной последовательности.
    Если скобочная последовательность завершена и запятая находится после/до неё, то выражение
    обрезается и добавляется внутрь.
    """
    count_bracket = 0
    last_ind = 0
    expressions = []
    for ind, elem in enumerate(exp):
        if elem == "(":
            count_bracket += 1
        elif elem == ")":
            count_bracket -= 1
        if elem == "," and count_bracket == 0:

            expressions.append(exp[last_ind: ind])
            last_ind = ind + 1
    expressions.append(exp[last_ind:])
    return expressions



def do_func(exp: float, func_name: str, args: list):
    """
    применяет функцию func_name к указанному выражению exp, используя аргументы args
    """
    if args is not None:
        # упрощение и преобразование в числовой формат сторонних аргументов функции
        args = list(map(work, args))
        args = list(map(float, args))
        return functions[func_name](exp, *args)
    else:
        return functions[func_name](exp)


def remove_spaces(exp: str):
    """удаляет пробелы из выражения, для упрощения работы с ним"""
    exp_list = list(exp)
    i = 0
    while i < len(exp_list):
        if exp_list[i] == " ":
            del exp_list[i]
            i -= 1
        i += 1
    return "".join(exp_list)


def div(a: float, b: float):
    """
    самодельное деление двух чисел
    """
    if b != 0:
        return a / b
    else:
        print(f"ZeroDivisionError ({a}/{b})")
        exit()


def get_bracket(exp: str):
    """
    Ищет первое вхождение внешней скобочной последовательности,
    укаывая при этом, является ли она функцией, объявленной в functions.
    """
    count_of_brackets = 0
    have_brackets = False

    first_ind = -1

    func = None
    for ind, elem in enumerate(exp):
        if elem == "(":
            count_of_brackets += 1
            if not have_brackets:
                have_brackets = True
                first_ind = ind
                # индекс первой скобки
                if ind > 2 and exp[ind - 3:ind] in functions:
                    # если есть функция, то получает её название
                    func = exp[ind - 3:ind]

        elif elem == ")":
            count_of_brackets -= 1
        if count_of_brackets == 0 and have_brackets:
            last_ind = ind
            # индекс последней скобки, конец выполнения кода в этом условии
            if func:
                # если скобки были функцией, то разделяются все её аргументы в func_elems
                exp_without_brackets = exp[first_ind+1:last_ind]
                # выделение выражения из скобок, без их самих
                func_elems = break_comma(exp_without_brackets)
                # делит выражение на массив, разделителем является запятая
                # не делит, если выражение внутри скобок
                if len(func_elems) > 1:
                    ind_del = len(func_elems[0])
                    # если аргументов больше, чем один, то ind_del  является первым вхождением запятой
                    # разделяющей первый и последующие аргументы. Она будет представлена как последний
                    # индекс, таким образом остаётся в диапозоне только он.
                    # название функции и прочие аргументы возвращаются в кортеже третиим элементом.
                    # Все символы после первого аргумента удаляются из выражения, путём
                    # смещения первого индекса среза строки, находящейся справа от
                    # выражения. Цифровое значение этого смещения представлено в
                    # качестве четвёртого возвращаемого элемента.
                    return first_ind, ind_del + len(func) + 1, (func, func_elems[1:]), last_ind - ind_del
            # в качестве индексов идут первое и последнее вхождение скобки
            # в качестве func - название функции, None - единственный аргумент функции
            # 0 - отсутствие смещения, т.к. аргумент всего один
            return first_ind, last_ind, (func, None), 0
    return
    # возвращает None, если скобки в выражении не обнаружены


def processing_plus_minus(exp: str) -> str:
    """
    разделяет выражение строкового формата
    на слагаемые, отдельно сохраняя в правильном порядке
    знаки сложения, вычитания и сами слагаемые в строковом формате.
    Не работает, если арифметические знаки будут находиться до знака сложения или вычитания,
    чтобы сохранять отрицательные числа в произведении или делении
    """
    elems_split = ["-", "+"]
    elems_split_mul = ["/", "*", "х", ":"]
    func = {"-": float.__sub__, "+": float.__add__}
    groups = []
    signs = []

    if exp[0] in elems_split:
        # необходимо для того, чтобы программа не вычитали значение из ничего, добавляет 0
        exp = "0"+exp

    last_ind = -1
    for ind, elem in enumerate(exp):
        # разделение на слагаемые
        if elem in elems_split and exp[ind-1] not in elems_split_mul \
                and exp[ind-1] not in elems_split:
            groups.append(exp[last_ind+1:ind])
            signs.append(elem)
            last_ind = ind
    if last_ind == -1:
        # если нет знаков сложения или вычитания, то добавит одно единственное слагаемое
        groups.append(str(processing_mul_div(exp)))
    else:
        # добавление последнего слагаемого
        groups.append(exp[last_ind + 1:])

    for i in signs:
        # выполняет по очереди действия для каждого из слагаемого,
        # заранее посчитав каждый из них в processing_mul_div
        groups[0] = str(func[i](processing_mul_div(groups[0]), processing_mul_div(groups[1])))
        del groups[1]
    return groups[0]


def processing_mul_div(exp: str) -> float:
    """
    выполняет произведение элементов, находящихся в выражении
    """
    elems_split = ["/", "*", "х", ":"]
    func = {"/": div, ":": div, "*": float.__mul__, "х": float.__mul__}
    groups = []
    signs = []

    last_ind = -1
    for ind, elem in enumerate(exp):
        # разделение на множители, делители и делимые, а так же знаки деления и умножения
        if elem in elems_split:
            groups.append(exp[last_ind + 1:ind])
            signs.append(elem)
            last_ind = ind
    if last_ind == -1:
        groups.append(float(exp))
        # добавляет единственный множитель, если он только один
    else:
        groups.append(exp[last_ind + 1:])
        # добавляет последний множитель
    for i in signs:
        # считает произведение, деление
        groups[0] = func[i](float(groups[0]), float(groups[1]))
        del groups[1]
    return groups[0]


def work(exp: str) -> str:
    """
    Возвращает искомое значение выражения в строковом формате
    """
    while True:
        # ищет скобочные последовательности в выражении, отдельно их разбирая
        brackets: tuple = get_bracket(exp)
        # получение информации о внешних скобках в выражении
        if brackets:
            # выполняется при присутствии скобок в выражении
            first_bracket = brackets[0]
            second_bracket = brackets[1]
            # получение индексов внешних скобок
            if not brackets[2][0] is None:
                # выполняется при присутствии функций
                func = brackets[2][0]  # название функции
                func_last_ind = brackets[3]  # смещение
                if not brackets[2][1] is None:
                    func_second_arg = brackets[2][1]  # вторичные аргументы функции, если они есть
                else:
                    func_second_arg = None  # отсутствие вторичных аргументов
                exp = exp[:first_bracket-len(func)] + str(do_func(float(work(exp[first_bracket+1:second_bracket])), func, func_second_arg)) + exp[second_bracket+1+func_last_ind:]
                # всё выражение до функции и после неё остаётся неизменным
                # сама функция будет высчитываться рекурсивно.

            else:
                # функции нет, это обычная скобка
                # происходит высчитывание значения в скобке с помощью рекурсии, после чего всё
                # собирается в выражение без этой скобки.
                # Повтор цикла, пока скобок не останется.
                exp = exp[:first_bracket] + work(exp[first_bracket+1:second_bracket]) + exp[second_bracket+1:]
        else:
            # заканчивается цикл при отсутствии скобок
            break
    # возвращает значнеие выражения в строковом формате
    return processing_plus_minus(exp)


# можно добавить функцию, для увеличения функционала.
# Длина строкового названия должна быть равно 3

functions = {
    "cos": math.cos,
    "sin": math.sin,
    "tan": math.tan,
    "log": math.log,
    "pow": math.pow,
    "sqr": sqr
}


while True:
    expression = input()
    expression_without_spaces = remove_spaces(expression)
    answer = work(expression_without_spaces)
    print(answer)
