from math import cos, sin, tan, gamma


def fac(x):
    return gamma(x)


def tg(x):
    return tan(x)


def generate_function(formulas, variables):
    var_init = ''.join((' ' * 4 + f'{k} = {v}\n' for k, v in variables.items()))
    f_return = ', '.join(formulas)
    code = f'def fun(x, y, time=0):\n{var_init}    return {f_return}'
    loc = {'cos': cos, "sin": sin, 'tan': tan, 'gamma': gamma, 'fac': fac, 'tg': tg}
    exec(code, loc)
    return loc['fun']

