def parse_formulas(lst, colors):
    def_vars = ('x', 'y', 'e', 'pi')
    formulas = []
    cases = []
    variables = {}
    res_colors = []
    while '' in lst:
        lst.remove('')
    for line, color in zip(lst, colors):
        line = line.replace(' ', '').replace('^', '**').replace('exit', '')
        var = False
        case = None
        f1, f2 = None, None

        if '>=' in line:
            f1, f2 = line.split('>=')
            case = '>='
        elif '<=' in line:
            f2, f1 = line.split('<=')
            case = '>='
        elif '>' in line:
            f1, f2 = line.split('>')
            case = '>'
        elif '<' in line:
            f2, f1 = line.split('<')
            case = '>'
        elif '=' in line:
            f1, f2 = line.split('=')
            if f1.replace('_', '').isalnum() and (f1 not in variables.keys() and f1 not in def_vars):
                var = True
            case = '='

        if not (check_formula(f1) and check_formula(f2)):
            raise SyntaxError(line)

        if var:
            variables[f1] = f2
        else:
            res_colors.append(color)
            formulas.append(f1 + ' - (' + f2 + ')')
            cases.append(case)

    return formulas, res_colors, cases, variables


def check_formula(formula: str):
    if type(formula) is not str:
        return False

    for sym in formula:
        if not (sym.isalnum() or sym in '+-*/_,().% '):
            return False

    return True
