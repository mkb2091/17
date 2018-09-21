import argparse
import re

import to_javascript
import to_python
import optimize
import verify

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
                ops.append(('INT', int(op, 17) % MAX))
            elif re.fullmatch(r'\+', op):
                ops.append(('ADD', op))
            elif re.fullmatch(r'\-', op):
                ops.append(('SUB', op))
            elif re.fullmatch(r'\*', op):
                ops.append(('MUL', op))
            elif re.fullmatch(r'\/', op):
                ops.append(('DIV', op))
            elif re.fullmatch(r'\@', op):
                ops.append(('STORE', op))
            elif re.fullmatch(r'\#', op):
                ops.append(('LOAD', op))
            elif re.fullmatch(r':', op):
                ops.append(('DUP', op))
            elif re.fullmatch(r'==', op):
                ops.append(('EQ', op))
            elif re.fullmatch(r'!', op):
                ops.append(('NT', op))
            elif re.fullmatch(r'>', op):
                ops.append(('GREATER', op))
            elif re.fullmatch(r'<', op):
                ops.append(('LESS', op))
            elif re.fullmatch(r'\%', op):
                ops.append(('MOD', op))
            elif re.fullmatch(r'I', op):
                ops.append(('INPUT', op))
            elif re.fullmatch(r'\$', op):
                ops.append(('OUTPUT', op))
            elif re.fullmatch(r'\$\$', op):
                ops.append(('OUTPUT_NUM', op))
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
    result = verify.verify_stack_size(ast, MAX)
    if result:
        print('Not enought items in stack for op (%s) in function %s' % result)
        exit(1)
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
