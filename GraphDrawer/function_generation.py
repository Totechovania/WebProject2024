from math import cos, sin, tan, gamma




def fac(x):
    return gamma(x)


def tg(x):
    return tan(x)



def generate_function(formulas, variables):
    var_init = ''.join((' ' * 4 + f'{k} = {v}\n' for k, v in variables.items()))
    f_return = ', '.join(formulas)
    # todo Добавить обаботку исключений
    code = f'def fun(x, y, time=0):\n{var_init}    return {f_return}'

    loc = {'cos': cos, "sin": sin, 'tan': tan, 'gamma': gamma, 'fac': fac, 'tg': tg}

    exec(code, loc)
    return loc['fun']


def shift_code(text, level):
    res = ''
    for line in text.split('\n'):
        res += ' ' * 4 * level + line + '\n'
    return res


def generate_vars_fun(variables):
    code = 'def fun(x, y, time=0):\n'

    with open('code_templates/var_template.txt', 'rt',  encoding='utf') as f:
        var_template = f.read()

    for name, expression in variables.items():
        var_code = var_template.format(name=name, expression=expression)
        var_code = shift_code(var_code, 1)
        code += var_code

    code += ' ' * 4 + f"return {', '.join(variables.keys())}"

    loc = {'cos': cos, "sin": sin, 'tan': tan, 'gamma': gamma, 'fac': fac, 'tg': tg}

    print(code)
    exec(code, loc)

    return loc['fun']


