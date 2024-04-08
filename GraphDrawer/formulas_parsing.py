def parse_formulas(text):
    def_vars = ('x', 'y', 'time')
    formulas = []
    cases = []
    variables = {}
    lst = text.replace(' ', '').replace('^', '**').split('\n')
    while '' in lst:
        lst.remove('')
    for line in lst:
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
            formulas.append(f1 + ' - (' + f2 + ')')
            cases.append(case)

    return formulas, cases,  variables


def check_formula(formula: str):
    if type(formula) is not str:
        return False

    for sym in formula:
        if not (sym.isalnum() or sym in '+-*/_,(). '):
            return False

    return True

