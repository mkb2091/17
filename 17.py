import argparse
import re

import bf_to_17
import to_python
import optimize
import verify
import logger

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
    parser.add_argument('-i', '--input', default='17', help='Input language')
    parser.add_argument('-t', '--target', help='Target language',
                        default='python')
    parser.add_argument('-O', '--optimize', type=int, default=1)
    parser.add_argument('-v', '--verbose', type=int, default=0)
    args = parser.parse_args()
    LOGGER = logger.Logger(level=args.verbose)
    with open(args.file) as file:
        code = file.read()
    if args.input == '17':
        ast = parse(code)
    elif args.input == 'bf':
        ast = bf_to_17.bf_to_17(code, MAX=MAX)
    LOGGER.info('Parsed')
    result = verify.verify_stack_size(ast, MAX, LOGGER)
    if result:
        LOGGER.error('Not enought items in stack for op (%s) in function %s'
                     % result)
        exit(1)
    LOGGER.info('Verified')
    ast = optimize.optimize(ast, MAX, args.optimize, LOGGER)
    LOGGER.info('Optimized')
    if args.target == 'python':
        output = to_python.to_python(ast, MAX, args.optimize, LOGGER)
    else:
        LOGGER.error('Unknown language')
        exit(1)
    LOGGER.info('Compiled')
    with open(args.output, 'w') as file:
        file.write(output)

if __name__ == '__main__':
    main()
