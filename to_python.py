def to_python(ast, MAX, OPTIMIZE, size=17**3):
    code = '''
from array import array
import sys
stack = []

class InfVector:
    def __init__(self):
        self.data = dict()

    def get(self, key):
        new_key = key // SIZE
        if new_key in self.data:
            return self.data[new_key][1][key % SIZE]
        return 17

    def set(self, key, value):
        new_key = key // SIZE
        value %= {MAX}
        if new_key in self.data:
            if value == 17:
                if self.data[new_key][1][key % SIZE] != 17:
                    self.data[new_key][0] -= 1
                    if self.data[new_key][0] == 0:
                        del self.data[new_key]
                    else:
                        self.data[new_key][1][key % 4913] = 17
                        #value, but thats already known
            else:
                if self.data[new_key][1][key % SIZE] == 17:
                    self.data[new_key][0] += 1
                self.data[new_key][1][key % SIZE] = value
        else:
            self.data[new_key] = [1, array('Q', [17] * SIZE)]
            self.data[new_key][1][key % SIZE] = value

stack = array('Q')
mem = InfVector()
mem.set(0, int('777', 17))
while True:
    name = mem.get(0)
    del stack[:]
    '''.replace('SIZE', str(size))
    for name in ast:
        code += 'if name == %s:\n' % name
        for op_type, op in ast[name]:
            if not OPTIMIZE:
                code += '\n{t}# (%s, %s, %s)\n' % (op_type, op) 
            if op_type == 'INT':
                code += '{t}stack.append(%s)\n' % op
            elif op_type == 'ADD':
                if isinstance(op, int):
                    code += '{t}stack[-1] = (stack[-1] + '
                    code += str(op) + ' ) % {MAX}\n'
                else:
                    code += '{t}stack[-2] = (stack[-2] + stack[-1]) % {MAX}\n'
                    code += '{t}del stack[-1]\n'
            elif op_type == 'SUB':
                if isinstance(op, int):
                    code += '{t}stack[-1] = (stack[-1] - '
                    code += str(op) + ' ) % {MAX}\n'
                else:
                    code += '{t}stack[-2] = (stack[-2] - stack[-1]) % {MAX}\n'
                    code += '{t}del stack[-1]\n'
            elif op_type == 'MUL':
                if isinstance(op, int):
                    code += '{t}stack[-1] = (stack[-1] * '
                    code += str(op) + ' ) % {MAX}\n'
                else:
                    code += '{t}stack[-2] = (stack[-2] * stack[-1]) % {MAX}\n'
                    code += '{t}del stack[-1]\n'
            elif op_type == 'DIV':
                if isinstance(op, int):
                    if op == 0:
                        code += '{t}stack[-1] = 17\n'
                    else:
                        code += '{t}stack[-1] //= %s\n' % o
                else:
                    code += '{t}try:\n'
                    code += '{t}    {t}stack[-2] = (stack[-2] // stack[-1])\n'
                    code += '{t}except ZeroDivisionError:\n'
                    code += '{t}    stack[-2] = 17\n'
                    code += '{t}del stack[-1]\n'
            elif op_type == 'STORE':
                if isinstance(op, tuple):
                    code += '{t}mem.set(%s, %s)\n' % (op[1], op[0])
                elif isinstance(op, int):
                    code += '{t}mem.set(%s, stack[-1])\n' % op
                    code += '{t}del stack[-1]\n'
                else:
                    code += '{t}mem.set(stack[-1], stack[-2])\n'
                    code += '{t}del stack[-2:]\n'
            elif op_type == 'LOAD':
                if isinstance(op, int):
                    code += '{t}stack.append(mem.get(%s))\n' % op
                else:
                    code += '{t}stack.append(mem.get(stack.pop(-1)))\n'
                        
            elif op_type == 'DUP':
                if isinstance(op, int):
                    code += '{t}stack.append(%s)\n' % op
                else:
                    code += '{t}stack.append(stack[-1])\n'
            elif op_type == 'EQ':
                if isinstance(op, int):
                    code += '{t}stack[-1] = int(stack[-1] == %s)\n' % op
                else:
                    code += '{t}stack[-2] = int(stack[-2] == stack[-1])\n'
                    code += '{t}del stack[-1]\n'
            elif op_type == 'NT':
                code += '{t}stack[-1] = int(not stack[-1])\n'
            elif op_type == 'GREATER':
                if isinstance(op, int):
                    code += '{t}stack[-1] = int(stack[-1] > %s)\n' % op
                else:
                    code += '{t}stack[-2] = int(stack[-2] > stack[-1])\n'
                    code += '{t}del stack[-1]\n'
            elif op_type == 'LESS':
                if isinstance(op, int):
                    code += '{t}stack[-1] = int(stack[-1] < %s)\n' % op
                else:
                    code += '{t}stack[-2] = int(stack[-2] < stack[-1])\n'
                    code += '{t}del stack[-1]\n'
            elif op_type == 'MOD':
                if isinstance(op, int):
                    code += '{t}stack[-1] = int(stack[-1] %% %s)\n' % op
                else:
                    code += '{t}stack[-2] = int(stack[-2] % stack[-1])\n'
                    code += '{t}del stack[-1]\n'
            elif op_type == 'INPUT':
                code += '{t}stack.append(ord(sys.stdin.read(1)))\n'
            elif op_type == 'OUTPUT':
                if isinstance(op, list):
                    if op == [ord('\n')]:
                        code += '{t}print()\n'
                    elif op[-1:] == [ord('\n')]:
                        code += '{t}print(%s)\n' % repr(''.join(map(chr, op[:-1])))
                    else:
                        code += '{t}print(%s, end="")\n' % repr(''.join(map(chr, op)))
                else:
                    code += '{t}print(chr(stack.pop(-1)), end="")\n'
            elif op_type == 'OUTPUT_NUM':
                if isinstance(op, int):
                    code += '{t}print(%s, end="")\n' % op
                else:
                    code += '{t}print(stack.pop(-1), end="")\n'
            else:
                print('Unknown op_type:', op_type)
        code += '    el'
    code += 'se:\n        break'  
    return code.format(MAX=MAX, t=' ' * 8)
