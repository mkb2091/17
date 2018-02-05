import argparse
import re

import to_javascript
import to_python
import optimize

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
            elif re.fullmatch(r'\$', op):
                ops.append(('OUTPUT', op, stack_min))
                stack_min = max(0, stack_min - 1)
            elif re.fullmatch(r'\$\$', op):
                ops.append(('OUTPUT_NUM', op, stack_min))
                stack_min = max(0, stack_min - 1)
            else:
                print('Unknown OP:', op)
        if ops:
            ast[name] = ops
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
    ast = optimize.optimize(ast, MAX)
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
