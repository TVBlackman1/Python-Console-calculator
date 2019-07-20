# Python version: 3.7

import math


class Calculator:

    def __init__(self, other_func: dict = None, inf=512):
        self.__inf = inf

        # length of names is 3! It`s necessary
        self.__functions = {
            "cos": math.cos,
            "sin": math.sin,
            "tan": math.tan,
            "log": math.log,
            "pow": math.pow,
            "sqr": self.__sqr,
            "sgm": self.__sgm,
            "mul": self.__mul
        }

        if other_func:
            for name, func in other_func.items():
                self.__functions[name] = func

    def func_append(self, name, func):
        self.__functions[name] = func

    def calculate(self, expression: str):
        expression_without_spaces = self.__remove_spaces(expression)
        answer = self.__work(expression_without_spaces)

        return answer

    def __sgm(self, exp: str, variable: str, start: float, end: float):
        sum_ = 0
        for i in range(round(start), round(end) + 1):
            exp_without_var = exp.replace(variable, str(i))

            ans = float(self.__work(exp_without_var))
            sum_ += ans
        return sum_

    def break_comma(self, exp: str) -> list:
        """
        :returns list_of_expressions

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

    def get_bracket(self, exp: str):

        """
        :returns first_bracket_index, first_func_arg_index+1, (func_name, *func_args_besides_first), last_bracket_index
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
                    if ind > 2 and exp[ind - 3:ind] in self.__functions:
                        func = exp[ind - 3:ind]

            elif elem == ")":
                count_of_brackets -= 1
            if count_of_brackets == 0 and have_brackets:
                last_ind = ind
                if func:
                    exp_without_brackets = exp[first_ind + 1:last_ind]
                    func_elems = self.break_comma(exp_without_brackets)
                    if len(func_elems) > 1:
                        ind_del = len(func_elems[0])
                        return first_ind, first_ind + ind_del + 1, (func, func_elems[1:]), last_ind
                return first_ind, last_ind, (func, None), last_ind
        return

    def __remove_spaces(self, exp: str):
        exp = exp.replace(" ", "")
        return exp

    def __do_func(self, exp: float, func_name: str, args: list):

        if args is not None:

            args = list(map(self.__elective_work, args))
            args = list(map(self.__elective_float, args))
            ret = self.__functions[func_name](exp, *args)
        else:
            ret = self.__functions[func_name](exp)
        return ret

    def __div(self, a: float, b: float):
        if b != 0:
            return a / b
        else:
            raise Exception(f"ZeroDivisionError ({a}/{b})")

    def __mul(self, *args):
        m = 1
        for i in args:
            m *= i
        return m

    def __sqr(self, x):
        return x * x

    def __processing_plus_minus(self, exp: str) -> str:
        elems_split = ["-", "+"]
        elems_split_mul = ["/", "*", "х", ":"]
        split_e = "e"
        func = {"-": float.__sub__, "+": float.__add__}
        groups = []
        signs = []
        if exp[0] in elems_split:
            exp = "0" + exp

        last_ind = -1
        for ind, elem in enumerate(exp):
            if elem in elems_split and exp[ind - 1] not in elems_split_mul \
                    and exp[ind - 1] not in elems_split and exp[ind - 1] != split_e:
                groups.append(exp[last_ind + 1:ind])
                signs.append(elem)
                last_ind = ind
        if last_ind == -1:
            groups.append(str(self.__processing_mul_div(exp)))
        else:
            groups.append(exp[last_ind + 1:])

        for i in signs:
            tmp1 = self.__processing_mul_div(groups[0])
            tmp2 = self.__processing_mul_div(groups[1])

            groups[0] = str(func[i](tmp1, tmp2))
            del groups[1]
        return groups[0]

    def __processing_mul_div(self, exp: str) -> float:
        if exp == "inf":
            return self.__inf

        elems_split = ["/", "*", "х", ":"]
        func = {"/": self.__div, ":": self.__div, "*": float.__mul__, "х": float.__mul__}
        groups = []
        signs = []

        last_ind = -1
        for ind, elem in enumerate(exp):
            if elem in elems_split:
                groups.append(exp[last_ind + 1:ind])
                signs.append(elem)
                last_ind = ind
        if last_ind == -1:
            groups.append(float(exp))
        else:
            groups.append(exp[last_ind + 1:])
        for i in signs:
            tmp1 = float(groups[0])
            tmp2 = float(groups[1])
            groups[0] = func[i](tmp1, tmp2)
            del groups[1]

        return groups[0]

    def __work(self, exp: str) -> str:
        while True:
            brackets: tuple = self.get_bracket(exp)
            if brackets:
                first_bracket = brackets[0]
                second_bracket = brackets[1]
                if not brackets[2][0] is None:
                    func = brackets[2][0]
                    func_last_ind = brackets[3]
                    if not brackets[2][1] is None:
                        func_second_arg = brackets[2][1]
                    else:
                        func_second_arg = None
                    if func == "sgm":
                        exp = exp[:first_bracket - len(func)] + \
                              str(self.__do_func(exp[first_bracket + 1:second_bracket], func, func_second_arg)) + \
                              exp[func_last_ind + 1:]
                    else:
                        exp = exp[:first_bracket - len(func)] + \
                              str(self.__do_func(float(self.__work(exp[first_bracket + 1:second_bracket])), func,
                                                 func_second_arg)) + \
                              exp[func_last_ind + 1:]
                else:
                    exp = exp[:first_bracket] + self.__work(exp[first_bracket + 1:second_bracket]) + exp[
                                                                                                   second_bracket + 1:]
            else:
                break
        return self.__processing_plus_minus(exp)

    def __elective_float(self, elem):
        try:
            elem = float(elem)
            return elem
        except:
            return elem

    def __elective_work(self, elem):
        try:
            elem = self.__work(elem)
        except:
            pass
        finally:
            return elem
