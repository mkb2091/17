import argparse
import re

import to_python

FUNCTIONS = '([0-9a-g]+) ?{([^}]*)}'
MAX = 18446744073709551615

def parse(code):
    ast = {}
    for name, data in re.findall(FUNCTIONS, code):
        if name in ast:
            print('Duplicate function:', name)
            exit()
        name = int(name, 17)
        print(name)
        ops = []
        for op in re.findall('([\S]+)', data):
            print(op)
            if re.fullmatch('[0-9a-g]+', op):
                ops.append(('INT', int(op, 17) % MAX))
            elif re.fullmatch(r'\+', op):
                ops.append(('ADD', op))
            elif re.fullmatch(r'\-', op):
                ops.append(('SUB', op))
            elif re.fullmatch(r'\*', op):
                ops.append(('MUL', op))
            elif re.fullmatch(r'\\', op):
                ops.append(('DIV', op))
            elif re.fullmatch(r'\@', op):
                ops.append(('STORE', op))
            elif re.fullmatch(r'\#', op):
                ops.append(('LOAD', op))
            elif re.fullmatch(r'\$', op):
                ops.append(('OUTPUT', op))
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
                    if x[0] == 'INT' and ast[name][i + 1][0] == 'INT':
                        if block[i + 2][0] == 'ADD':
                            num = (block[i][1] + block[i + 1][1]) % MAX
                            block[i:i + 3] = [('INT', num)]
                            changed = True
                        elif block[i + 2][0] == 'SUB':
                            num = (block[i][1] - block[i + 1][1]) % MAX
                            print(block[i], block[i+1])
                            block[i:i + 3] = [('INT', num)]
                            changed = True
                        elif block[i + 2][0] == 'MUL':
                            num = (block[i][1] * block[i + 1][1]) % MAX
                            block[i:i + 3] = [('INT', num)]
                            changed = True
                        elif block[i + 2][0] == 'DIV':
                            num = int(block[i][1] / block[i + 1][1]) % MAX
                            block[i:i + 3] = [('INT', num)]
                            changed = True
                        if changed:
                            break
                except IndexError:
                    if changed:
                        break
            if changed:
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
    ast = optimize(ast)
    if args.target == 'python':
        output = to_python.to_python(ast)
    else:
        print('Unknown language')
    print(output)
    with open(args.output, 'w') as file:
        file.write(output)

if __name__ == '__main__':
    main()
