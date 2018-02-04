import argparse
import re

import to_javascript
import to_python

FUNCTIONS = '([0-9a-g]+) ?{([^}]*)}'
MAX = 18446744073709551616

def parse(code):
    ast = {}
    for name, data in re.findall(FUNCTIONS, code):
        if name in ast:
            print('Duplicate function:', name)
            exit()
        name = int(name, 17)
        ops = []
        stack_min = 0
        for op in re.findall('([\S]+)', data):
            if re.fullmatch('[0-9a-g]+', op):
                ops.append(('INT', int(op, 17) % MAX, stack_min))
                stack_min += 1
            elif re.fullmatch(r'\+', op):
                ops.append(('ADD', op, stack_min))
                stack_min = max(1, stack_min - 1)
            elif re.fullmatch(r'\-', op):
                ops.append(('SUB', op, stack_min))
                stack_min = max(1, stack_min - 1)
            elif re.fullmatch(r'\*', op):
                ops.append(('MUL', op, stack_min))
                stack_min = max(1, stack_min - 1)
            elif re.fullmatch(r'\/', op):
                ops.append(('DIV', op, stack_min))
                stack_min = max(1, stack_min - 1)
            elif re.fullmatch(r'\@', op):
                ops.append(('STORE', op, stack_min))
                stack_min = max(0, stack_min - 2)
            elif re.fullmatch(r'\#', op):
                ops.append(('LOAD', op, stack_min))
                stack_min = max(1, stack_min)
            elif re.fullmatch(r':', op):
                ops.append(('DUP', op, stack_min))
                stack_min += 1
            elif re.fullmatch(r'==', op):
                ops.append(('EQ', op, stack_min))
                stack_min = max(1, stack_min - 1)
            elif re.fullmatch(r'!', op):
                ops.append(('NT', op, stack_min))
                stack_min = max(1, stack_min - 1)
            elif re.fullmatch(r'>', op):
                ops.append(('GREATER', op, stack_min))
                stack_min = max(1, stack_min - 1)
            elif re.fullmatch(r'<', op):
                ops.append(('LESS', op, stack_min))
                stack_min = max(1, stack_min - 1)
            elif re.fullmatch(r'\%', op):
                ops.append(('MOD', op, stack_min))
                stack_min = max(1, stack_min - 1)
            elif re.fullmatch(r'I', op):
                ops.append(('INPUT', op, stack_min))
                stack_min += 1
            elif re.fullmatch(r'\$\$', op):
                ops.append(('OUTPUT_NUM', op, stack_min))
                stack_min = max(0, stack_min - 1)
            else:
                print('Unknown OP:', op)
        if ops:
            ast[name] = ops
    return ast

def optimize(ast):
    changed = True
    while changed:
        changed = False 
        for name in ast:
            block = ast[name]
            for i, x in enumerate(block):
                try:
                    if changed:
                        break
                    if x[0] == 'OUTPUT' and block[i + 1][0] == 'OUTPUT':
                        if isinstance(block[i][1], tuple):
                            if isinstance(block[i + 1][1], tuple):
                                block[i:i + 2] = [('OUTPUT',
                                                   x[1] + block[i + 1][1],
                                                   block[i][2])]
                                changed = True
                    elif x[0] == 'INT' and ast[name][i + 1][0] != 'INT':
                        if block[i + 1][0] == 'ADD':
                            block[i:i + 2] = [('ADD', x[1], block[i][2])]
                            changed = True
                        elif block[i + 1][0] == 'SUB':
                            block[i:i + 2] = [('SUB', x[1], block[i][2])]
                            changed = True
                        elif block[i + 1][0] == 'MUL':
                            block[i:i + 2] = [('MUL', x[1], block[i][2])]
                            changed = True
                        elif block[i + 1][0] == 'DIV':
                            block[i:i + 2] = [('DIV', x[1], block[i][2])]
                            changed = True
                        elif block[i + 1][0] == 'DUP':
                            block[i + 1] = ('INT', block[i][1], block[i + 1][2])
                            changed = True
                        elif block[i + 1][0] == 'STORE':
                            block[i:i + 2] = [('STORE', x[1], block[i][2])]
                            changed = True
                        elif block[i + 1][0] == 'LOAD':
                            if isinstance(block[i + 1][1], str):
                                block[i:i + 2] = [('LOAD', x[1], block[i][2])]
                                changed = True
                        elif block[i + 1][0] == 'OUTPUT':
                            if isinstance(block[i + 1][1], str):
                                block[i:i + 2] = [('OUTPUT', (x[1],),
                                                   block[i][2])]
                                changed = True
                        elif block[i + 1][0] == 'OUTPUT_NUM':
                            if isinstance(block[i + 1][1], str):
                                block[i:i + 2] = [('OUTPUT_NUM', x[1],
                                                   block[i][2])]
                                changed = True
                    elif x[0] == 'INT' and ast[name][i + 1][0] == 'INT':
                        if block[i + 2][0] == 'ADD':
                            num = (block[i][1] + block[i + 1][1]) % MAX
                            block[i:i + 3] = [('INT', num, block[i][2])]
                            changed = True
                        elif block[i + 2][0] == 'SUB':
                            num = (block[i][1] - block[i + 1][1]) % MAX
                            block[i:i + 3] = [('INT', num, block[i][2])]
                            changed = True
                        elif block[i + 2][0] == 'MUL':
                            num = (block[i][1] * block[i + 1][1]) % MAX
                            block[i:i + 3] = [('INT', num, block[i][2])]
                            changed = True
                        elif block[i + 2][0] == 'DIV':
                            num = (block[i][1] // block[i + 1][1]) % MAX
                            block[i:i + 3] = [('INT', num, block[i][2])]
                            changed = True
                        elif block[i + 2][0] == 'STORE':
                            block[i:i + 3] = [('STORE',
                                               (block[i][1], block[i + 1][1]),
                                               block[i][2])]
                except IndexError:
                    pass
                if changed:
                    ast[name] = block
                    break
    return ast


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Code file for 17')
    parser.add_argument('-o', '--output', default='output')
    parser.add_argument('-t', '--target', help='Target language',
                        default='python')
    args = parser.parse_args()
    with open(args.file) as file:
        code = file.read()
    ast = parse(code)
    print('Parsed')
    ast = optimize(ast)
    print('Optimized')
    if args.target == 'python':
        output = to_python.to_python(ast, MAX=MAX)
    elif args.target == 'js':
        output = to_javascript.to_javascript(ast, MAX=MAX)
    else:
        print('Unknown language')
        return
    print('Compiled')
    with open(args.output, 'w') as file:
        file.write(output)

if __name__ == '__main__':
    main()
