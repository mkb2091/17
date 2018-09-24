import re

def bf_to_17(bf, MAX=2**64):
    ast = {2149:[['STORE', (200, 1)], ['STORE', (0, 200)]]}
    functions = [2149]
    for instruction in bf:
        if instruction == '>':
            ast[functions[-1]].extend([['LOAD', 1], ['ADD', 1], ['DUP', ':'],
                                       ['GREATER', MAX-100], ['MUL', MAX-100],
                                       ['SUB', '-'], ['STORE', 1]])
        elif instruction == '<':
            ast[functions[-1]].extend([['LOAD', 1], ['SUB', 1], ['DUP', ':'],
                                       ['LESS', 100], ['MUL', MAX-100],
                                       ['ADD', '+'], ['STORE', 1]])
        elif instruction == '+':
            ast[functions[-1]].extend([['LOAD', 1], ['DUP', ':'],['LOAD', '#'],
                                       ['ADD', 1],['STORE', '@']])
        elif instruction == '-':
            ast[functions[-1]].extend([['LOAD', 1], ['DUP', ':'],['LOAD', '#'],
                                       ['SUB', 1],['STORE', '@']])
        elif instruction == '.':
            ast[functions[-1]].extend([['LOAD', 1], ['LOAD', '#'],
                                       ['OUTPUT', '$']])
    ast[functions[-1]].append(['STORE', (0, 0)])
    
    return ast
