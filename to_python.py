def to_python(ast, MAX):
    code = '''
from array import array
import sys
stack = []

class InfVector:
    def __init__(self, size):
        self.size = size
        self.data = dict()

    def get(self, key):
        new_key = key // self.size
        if new_key in self.data:
            return self.data[new_key][key % self.size]
        return 17

    def set(self, key, value):
        new_key = key // self.size
        value %= {MAX}
        if new_key in self.data:
            self.data[new_key][key % self.size] = value
            if value == 17:
                clean = True
                for i in self.data[new_key]:
                    if i != 17:
                        clean = False
                        break
                if clean:
                    del self.data[new_key]
        else:
            self.data[new_key] = array('Q', [17] * self.size)
            self.data[new_key][key % self.size] = value

stack = array('Q')
mem = InfVector(17 ** 3)
mem.set(0, int('777', 17))
while True:
    name = mem.get(0)
    '''
    for name in ast:
        code += 'if name == %s:\n' % name
        for op_type, op, stack_min in ast[name]:
            code += '\n{t}# (%s, %s, %s)\n' % (op_type, op, stack_min) 
            if op_type == 'INT':
                code += '{t}stack.append(%s)\n' % op
            elif op_type == 'ADD':
                if isinstance(op, int):
                    if stack_min:
                        code += '{t}stack[-1] = (stack[-1] + '
                        code += str(op) + ' ) % {MAX}\n'
                    else:
                        code += '{t}if stack:\n'
                        code += '{t}    stack[-1] = (stack[-1] + '
                        code += str(op) + ' ) % {MAX}\n'
                        code += '{t}else:\n'
                        code += '{t}    stack.append(%s)\n' % ((17 + op) % MAX)
                else:
                    if stack_min >= 2:
                        code += '{t}now = (stack[-2] + stack[-1]) % {MAX}\n'
                        code += '{t}del stack[-2:]\n'
                        code += '{t}stack.append(now)\n'
                    elif stack_min:
                        code += '{t}if len(stack) >= 2:\n'
                        code += '{t}    now = (stack[-2] + stack[-1]) % {MAX}\n'
                        code += '{t}    del stack[-2:]\n'
                        code += '{t}    stack.append(now)\n'
                        code += '{t}else:\n'
                        code += '{t}    stack[-1] = (17 + stack[-1]) % {MAX}\n'
                    else:
                        code += '{t}if len(stack) >= 2:\n'
                        code += '{t}    now = (stack[-2] + stack[-1]) % {MAX}\n'
                        code += '{t}    del stack[-2:]\n'
                        code += '{t}    stack.append(now)\n'
                        code += '{t}elif stack:\n'
                        code += '{t}    stack[-1] = (17 + stack[-1]) % {MAX}\n'
                        code += '{t}else:\n'
                        code += '{t}    stack.append(34)\n'
            elif op_type == 'SUB':
                if isinstance(op, int):
                    if stack_min:
                        code += '{t}stack[-1] = (stack[-1] - '
                        code += str(op) + ' ) % {MAX}\n'
                    else:
                        code += '{t}if stack:\n'
                        code += '{t}    stack[-1] = (stack[-1] - '
                        code += str(op) + ' ) % {MAX}\n'
                        code += '{t}else:\n'
                        code += '{t}    stack.append(%s)\n' % ((17 - op) % MAX)
                else:
                    if stack_min >= 2:
                        code += '{t}now = (stack[-2] - stack[-1]) % {MAX}\n'
                        code += '{t}del stack[-2:]\n'
                        code += '{t}stack.append(now)\n'
                    elif stack_min:
                        code += '{t}if len(stack) >= 2:\n'
                        code += '{t}    now = (stack[-2] - stack[-1]) % {MAX}\n'
                        code += '{t}    del stack[-2:]\n'
                        code += '{t}    stack.append(now)\n'
                        code += '{t}else:\n'
                        code += '{t}    stack[-1] = (17 - stack[-1]) % {MAX}\n'
                    else:
                        code += '{t}if len(stack) >= 2:\n'
                        code += '{t}    now = (stack[-2] - stack[-1]) % {MAX}\n'
                        code += '{t}    del stack[-2:]\n'
                        code += '{t}    stack.append(now)\n'
                        code += '{t}elif stack:\n'
                        code += '{t}    stack[-1] = (17 - stack[-1]) % {MAX}\n'
                        code += '{t}else:\n'
                        code += '{t}    stack.append(0)\n'
            elif op_type == 'MUL':
                if isinstance(op, int):
                    if stack_min:
                        code += '{t}stack[-1] = (stack[-1] * '
                        code += str(op) + ' ) % {MAX}\n'
                    else:
                        code += '{t}if stack:\n'
                        code += '{t}    stack[-1] = (stack[-1] * '
                        code += str(op) + ' ) % {MAX}\n'
                        code += '{t}else:\n'
                        code += '{t}    stack.append(%s)\n' % ((17 * op) % MAX)
                else:
                    if stack_min >= 2:
                        code += '{t}now = (stack[-2] * stack[-1]) % {MAX}\n'
                        code += '{t}del stack[-2:]\n'
                        code += '{t}stack.append(now)\n'
                    elif stack_min:
                        code += '{t}if len(stack) >= 2:\n'
                        code += '{t}    now = (stack[-2] * stack[-1]) % {MAX}\n'
                        code += '{t}    del stack[-2:]\n'
                        code += '{t}    stack.append(now)\n'
                        code += '{t}else:\n'
                        code += '{t}    stack[-1] = (17 * stack[-1]) % {MAX}\n'
                    else:
                        code += '{t}if len(stack) >= 2:\n'
                        code += '{t}    now = (stack[-2] * stack[-1]) % {MAX}\n'
                        code += '{t}    del stack[-2:]\n'
                        code += '{t}    stack.append(now)\n'
                        code += '{t}elif stack:\n'
                        code += '{t}    stack[-1] = (17 * stack[-1]) % {MAX}\n'
                        code += '{t}else:\n'
                        code += '{t}    stack.append(%s)\n' % (17 * 17)
            elif op_type == 'DIV':
                if isinstance(op, int):
                    if stack_min:
                        if op == 0:
                            code += '{t}stack[-1] = 17\n'
                        else:
                            code += '{t}stack[-1] //= %s\n' % op
                    else:
                        code += '{t}if stack:\n'
                        if op == 0:
                            code += '{t}    stack[-1] = 17\n' % op
                        else:
                            code += '{t}    stack[-1] //= %s\n' % op
                        code += '{t}else:\n'
                        if op == 0:
                            code += '{t}    stack.append(17)\n'
                        else:
                            code += '{t}    stack.append(%s)\n' % (17 // op)
                else:
                    if stack_min >= 2:
                        code += '{t}try:\n'
                        code += '{t}    {t}now = (stack[-2] // stack[-1])\n'
                        code += '{t}except ZeroDivisionError:\n'
                        code += '{t}    now = 17\n'
                        code += '{t}del stack[-2:]\n'
                        code += '{t}stack.append(now)\n'
                    elif stack_min:
                        code += '{t}if len(stack) >= 2:\n'
                        code += '{t}    try:\n'
                        code += '{t}        now = (stack[-2] // stack[-1])\n'
                        code += '{t}    except ZeroDivisionError:\n'
                        code += '{t}        now = 17\n'
                        code += '{t}    del stack[-2:]\n'
                        code += '{t}    stack.append(now)\n'
                        code += '{t}else:\n'
                        code += '{t}    try:\n'
                        code += '{t}        stack[-1] = (17 // stack[-1])\n'
                        code += '{t}    except ZeroDivisionError:\n'
                        code += '{t}        stack[-1] = 17\n'
                    else:
                        code += '{t}if len(stack) >= 2:\n'
                        code += '{t}    try:\n'
                        code += '{t}        now = (stack[-2] // stack[-1])\n'
                        code += '{t}    except ZeroDivisionError:\n'
                        code += '{t}        now = 17\n'
                        code += '{t}    del stack[-2:]\n'
                        code += '{t}    stack.append(now)\n'
                        code += '{t}elif stack:\n'
                        code += '{t}    try:\n'
                        code += '{t}        stack[-1] = (17 // stack[-1])\n'
                        code += '{t}    except ZeroDivisionError:\n'
                        code += '{t}        stack[-1] = 17\n'
                        code += '{t}else:\n'
                        code += '{t}    stack.append(17)\n'
            elif op_type == 'STORE':
                if isinstance(op, tuple):
                    code += '{t}mem.set(%s, %s)\n' % (op[1], op[0])
                elif isinstance(op, int):
                    if stack_min:
                        code += '{t}mem.set(%s, stack[-1])\n' % op
                        code += '{t}del stack[-1]\n'
                    else:
                        code += '{t}if stack:\n'
                        code += '{t}    mem.set(%s, stack[-1])\n' % op
                        code += '{t}    del stack[-1]\n'
                        code += '{t}else:\n'
                        code += '{t}    mem.set(%s, 17)\n' % op
                else:
                    if stack_min >= 2:
                        code += '{t}mem.set(stack[-1], stack[-2])\n'
                        code += '{t}del stack[-2:]\n'
                    elif stack_min:
                        code += '{t}if len(stack) >= 2:\n'
                        code += '{t}    mem.set(stack[-1], stack[-2])\n'
                        code += '{t}    del stack[-2:]\n'
                        code += '{t}else:\n'
                        code += '{t}    mem.set(stack[-1], 17)\n'
                        code += '{t}    del stack[-1:]\n'
                    else:
                        code += '{t}if len(stack) >= 2:\n'
                        code += '{t}    mem.set(stack[-1], stack[-2])\n'
                        code += '{t}    del stack[-2:]\n'
                        code += '{t}elif stack:\n'
                        code += '{t}    mem.set(stack[-1], 17)\n'
                        code += '{t}    del stack[-1:]\n'
                        code += '{t}else:'
                        code += '{t}    mem.set(17, 17)\n'
            elif op_type == 'LOAD':
                if isinstance(op, int):
                    code += '{t}stack.append(mem.get(%s))\n' % op
                else:
                    if stack_min:
                        code += '{t}stack.append(mem.get(stack.pop(-1)))\n'
                    else:
                        code += '{t}if stack:\n'
                        code += '{t}    stack.append(mem.get(stack.pop(-1)))\n'
                        code += '{t}else:\n'
                        code += '{t}    stack.append(mem.get(17))\n'
                        
            elif op_type == 'DUP':
                if isinstance(op, int):
                    code += '{t}stack.append(%s)\n' % op
                else:
                    if stack_min:
                        code += '{t}stack.append(stack[-1])\n'
                    else:
                        code += '{t}if stack:\n'
                        code += '{t}    stack.append(stack[-1])\n'
                        code += '{t}else:\n'
                        code += '{t}    stack.append(17)\n'
            elif op_type == 'EQ':
                if stack_min >= 2:
                    code += '{t}now = int(stack[-2] == stack[-1])\n'
                    code += '{t}del stack[-2:]\n'
                    code += '{t}stack.append(now)\n'
                elif stack_min:
                    code += '{t}if len(stack) >= 2:\n'
                    code += '{t}    now = int(stack[-2] == stack[-1])\n'
                    code += '{t}    del stack[-2:]\n'
                    code += '{t}    stack.append(now)\n'
                    code += '{t}else:\n'
                    code += '{t}    now = int(17 == stack[-1])\n'
                    code += '{t}    stack[-1] = now\n'
                else:
                    code += '{t}if len(stack) >= 2:\n'
                    code += '{t}    now = int(stack[-2] == stack[-1])\n'
                    code += '{t}    del stack[-2:]\n'
                    code += '{t}    stack.append(now)\n'
                    code += '{t}elif stack:\n'
                    code += '{t}    now = int(17 == stack[-1])\n'
                    code += '{t}    stack[-1] = now\n'
                    code += '{t}else:\n'
                    code += '{t}    stack.append(0)'
            elif op_type == 'NT':
                if stack_min:
                    code += '{t}stack[-1] = int(not stack[-1])\n'
                else:
                    code += '{t}if stack:\n'
                    code += '{t}    stack[-1] = int(not stack[-1])\n'
                    code += '{t}else:\n'
                    code += '{t}    stack.append(0)\n'
            elif op_type == 'GREATER':
                if stack_min >= 2:
                    code += '{t}now = int(stack[-2] > stack[-1])\n'
                    code += '{t}del stack[-2:]\n'
                    code += '{t}stack.append(now)\n'
                elif stack_min:
                    code += '{t}if len(stack) >= 2:\n'
                    code += '{t}    now = int(stack[-2] > stack[-1])\n'
                    code += '{t}    del stack[-2:]\n'
                    code += '{t}    stack.append(now)\n'
                    code += '{t}else:\n'
                    code += '{t}    now = int(17 > stack[-1])\n'
                    code += '{t}    stack[-1] = now\n'
                else:
                    code += '{t}if len(stack) >= 2:\n'
                    code += '{t}    now = int(stack[-2] > stack[-1])\n'
                    code += '{t}    del stack[-2:]\n'
                    code += '{t}    stack.append(now)\n'
                    code += '{t}elif stack:\n'
                    code += '{t}    now = int(17 > stack[-1])\n'
                    code += '{t}    stack[-1] = now\n'
                    code += '{t}else:\n'
                    code += '{t}    stack.append(0)'
            elif op_type == 'LESS':
                if stack_min >= 2:
                    code += '{t}now = int(stack[-2] < stack[-1])\n'
                    code += '{t}del stack[-2:]\n'
                    code += '{t}stack.append(now)\n'
                elif stack_min:
                    code += '{t}if len(stack) >= 2:\n'
                    code += '{t}    now = int(stack[-2] < stack[-1])\n'
                    code += '{t}    del stack[-2:]\n'
                    code += '{t}    stack.append(now)\n'
                    code += '{t}else:\n'
                    code += '{t}    now = int(17 < stack[-1])\n'
                    code += '{t}    stack[-1] = now\n'
                else:
                    code += '{t}if len(stack) >= 2:\n'
                    code += '{t}    now = int(stack[-2] < stack[-1])\n'
                    code += '{t}    del stack[-2:]\n'
                    code += '{t}    stack.append(now)\n'
                    code += '{t}elif stack:\n'
                    code += '{t}    now = int(17 < stack[-1])\n'
                    code += '{t}    stack[-1] = now\n'
                    code += '{t}else:\n'
                    code += '{t}    stack.append(0)\n'
            elif op_type == 'MOD':
                if stack_min >= 2:
                    code += '{t}now = int(stack[-2] % stack[-1])\n'
                    code += '{t}del stack[-2:]\n'
                    code += '{t}stack.append(now)\n'
                elif stack_min:
                    code += '{t}if len(stack) >= 2:\n'
                    code += '{t}    now = int(stack[-2] % stack[-1])\n'
                    code += '{t}    del stack[-2:]\n'
                    code += '{t}    stack.append(now)\n'
                    code += '{t}else:\n'
                    code += '{t}    now = int(17 % stack[-1])\n'
                    code += '{t}    stack[-1] = now\n'
                else:
                    code += '{t}if len(stack) >= 2:\n'
                    code += '{t}    now = int(stack[-2] % stack[-1])\n'
                    code += '{t}    del stack[-2:]\n'
                    code += '{t}    stack.append(now)\n'
                    code += '{t}elif stack:\n'
                    code += '{t}    now = int(17 % stack[-1])\n'
                    code += '{t}    stack[-1] = now\n'
                    code += '{t}else:\n'
                    code += '{t}    stack.append(0)\n'
            elif op_type == 'INPUT':
                code += '{t}stack.append(ord(sys.stdin.read(1)))'
            elif op_type == 'OUTPUT':
                if isinstance(op, tuple):
                    code += '{t}print(%s, end="")\n' % repr(''.join(map(chr, op)))
                else:
                    if stack_min:
                        code += '{t}print(chr(stack.pop(-1)), end="")\n'
                    else:
                        code += '{t}if stack:\n'
                        code += '{t}    print(chr(stack.pop(-1)), end="")\n'
                        code += '{t}else:\n'
                        code += '{t}    print(chr(17), end="")\n'
            elif op_type == 'OUTPUT_NUM':
                if isinstance(op, int):
                    code += '{t}print(%s, end="")\n' % op
                else:
                    if stack_min:
                        code += '{t}print(stack.pop(-1), end="")\n'
                    else:
                        code += '{t}if stack:\n'
                        code += '{t}    print(stack.pop(-1), end="")\n'
                        code += '{t}else:\n'
                        code += '{t}    print(17, end="")\n'
            else:
                print('Unknown op_type:', op_type)
        code += '    el'
    code += 'se:\n        break'  
    return code.format(MAX=MAX, t=' ' * 8)
