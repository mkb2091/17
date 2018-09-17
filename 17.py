import argparse
import re

import to_javascript
import to_python
import optimize

FUNCTIONS = '([0-9a-g]+) ?{([^}]*)}'
MAX = 2**64

def parse(code):
    ast = {}
    for name, data in re.findall(FUNCTIONS, code):
        if name in ast:
            print('Duplicate function:', name)
            exit()
        name = int(name, 17)
        ops = []
        for op in re.findall('([\S]+)', data):
            if re.fullmatch('[0-9a-g]+', op):
                ops.append(('INT', int(op, 17) % MAX, 0))
            elif re.fullmatch(r'\+', op):
                ops.append(('ADD', op, 0))
            elif re.fullmatch(r'\-', op):
                ops.append(('SUB', op, 0))
            elif re.fullmatch(r'\*', op):
                ops.append(('MUL', op, 0))
            elif re.fullmatch(r'\/', op):
                ops.append(('DIV', op, 0))
            elif re.fullmatch(r'\@', op):
                ops.append(('STORE', op, 0))
            elif re.fullmatch(r'\#', op):
                ops.append(('LOAD', op, 0))
            elif re.fullmatch(r':', op):
                ops.append(('DUP', op, 0))
            elif re.fullmatch(r'==', op):
                ops.append(('EQ', op, 0))
            elif re.fullmatch(r'!', op):
                ops.append(('NT', op, 0))
            elif re.fullmatch(r'>', op):
                ops.append(('GREATER', op, 0))
            elif re.fullmatch(r'<', op):
                ops.append(('LESS', op, 0))
            elif re.fullmatch(r'\%', op):
                ops.append(('MOD', op, 0))
            elif re.fullmatch(r'I', op):
                ops.append(('INPUT', op, 0))
            elif re.fullmatch(r'\$', op):
                ops.append(('OUTPUT', op, 0))
            elif re.fullmatch(r'\$\$', op):
                ops.append(('OUTPUT_NUM', op, 0))
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
    parser.add_argument('-O', '--optimize', type=int, default=1)
    args = parser.parse_args()
    with open(args.file) as file:
        code = file.read()
    ast = parse(code)
    print('Parsed')
    ast = optimize.optimize(ast, MAX, args.optimize)
    print('Optimized')
    if args.target == 'python':
        output = to_python.to_python(ast, MAX, args.optimize)
    elif args.target == 'js':
        output = to_javascript.to_javascript(ast, MAX)
    else:
        print('Unknown language')
        return
    print('Compiled')
    with open(args.output, 'w') as file:
        file.write(output)

if __name__ == '__main__':
    main()
