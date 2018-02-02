MAX = 18446744073709551615
def to_python(ast):
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
        for op_type, op in ast[name]:
            if op_type == 'INT':
                code += '        stack.append(%s)\n' % op
            elif op_type == 'ADD':
                code += '        if len(stack) > 1:\n'
                code += '            now = (stack[-2] + stack[-1]) % {MAX}\n'
                code += '            del stack[-2:]\n'
                code += '            stack.append(now)\n'
                code += '        elif stack:\n'
                code += '            stack[-1] = (stack[-1] + 17) % {MAX}\n'
                code += '        else:\n'
                code += '            stack.append(34)\n'
            elif op_type == 'SUB':
                code += '        if len(stack) > 1:\n'
                code += '            now = (stack[-2] - stack[-1]) % {MAX}\n'
                code += '            del stack[-2:]\n'
                code += '            stack.append(now)\n'
                code += '        elif stack:\n'
                code += '            stack[-1] = (stack[-1] - 17) % {MAX}\n'
                code += '        else:\n'
                code += '            stack.append(0)\n'
            elif op_type == 'MUL':
                code += '        if len(stack) > 1:\n'
                code += '            now = (stack[-2] * stack[-1]) % {MAX}\n'
                code += '            del stack[-2:]\n'
                code += '            stack.append(now)\n'
                code += '        elif stack:\n'
                code += '            stack[-1] = (stack[-1] * 17) % {MAX}\n'
                code += '        else:\n'
                code += '            stack.append(%s)\n' % (17 ** 2)
            elif op_type == 'DIV':
                code += '        if len(stack) > 1:\n'
                code += '            now = int(stack[-2] / stack[-1]) % {MAX}\n'
                code += '            del stack[-2:]\n'
                code += '            stack.append(now)\n'
                code += '        elif stack:\n'
                code += '            stack[-1] = int(stack[-1] / 17) % {MAX}\n'
                code += '        else:\n'
                code += '            stack.append(1)\n'
            elif op_type == 'STORE':
                code += '        if len(stack) > 1:\n'
                code += '            mem.set(stack[-1], stack[-2])\n'
                code += '            del stack[-2:]\n'
                code += '        elif stack:\n'
                code += '            mem.set(stack.pop(-1), 17)\n'
                code += '        else:\n'
                code += '            mem.set(17, 17)\n'
            elif op_type == 'LOAD':
                code += '        if stack:\n'
                code += '            stack.append(mem.get(stack.pop(-1)))\n'
                code += '        else:\n'
                code += '            stack.append(mem.get(17))\n'
            
            elif op_type == 'OUTPUT':
                code += '        print(stack.pop(-1))\n'
            print(op_type, op)
        code += '    el'
    code += 'se:\n        break'  
    return code.format(MAX=MAX)
