from math import cos, sin, tan, gamma, log, pi, e
import math


def fac(x):
    return gamma(x)


def tg(x):
    return tan(x)


def shift_code(text, level):
    res = ''
    for line in text.split('\n'):
        res += ' ' * 4 * level + line + '\n'
    return res


def sign(i):
    if i == 0:
        return 0
    elif i > 0:
        return 1
    elif i < 0:
        return -1


def generate_graph_fun(formulas, variables):
    with open('GraphDrawer/code_templates/graph_template.txt', 'rt', encoding='utf') as f:
        graph_template = f.read()

    code = f"def fun(x, y, {''.join(f'{e}, ' for e in variables.keys())} time=0):\n"

    for i, formula in enumerate(formulas):
        formula_code = graph_template.format(ind=i, expression=formula)
        formula_code = shift_code(formula_code, 1)
        code += formula_code

    f_return = 'return ' + ', '.join(f'f{i}' for i in range(len(formulas)))
    f_return = shift_code(f_return, 1)

    code += f_return

    loc = {'cos': cos, "sin": sin, 'tan': tan, 'gamma': gamma, 'fac': fac, 'tg': tg, 'log': log, 'pi': pi, 'e': math.e, 'sign': sign}

    exec(code, loc)

    return loc['fun']


def generate_vars_fun(variables):
    code = 'def fun(x, y, time=0):\n'

    with open('GraphDrawer/code_templates/var_template.txt', 'rt', encoding='utf') as f:
        var_template = f.read()

    for name, expression in variables.items():
        var_code = var_template.format(name=name, expression=expression)
        var_code = shift_code(var_code, 1)
        code += var_code

    code += ' ' * 4 + f"return {', '.join(variables.keys())}"

    loc = {'cos': cos, "sin": sin, 'tan': tan, 'gamma': gamma, 'fac': fac, 'tg': tg, 'log': log, 'pi': pi, 'e': e, 'sign': sign}

    code = compile(code, '<string>', 'exec')
    exec(code, loc)

    return loc['fun']
