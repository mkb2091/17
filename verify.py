EFFECT = {'INT':(0,0),
          'ADD':(2,1),
          'SUB':(2,1),
          'MUL':(2,1),
          'DIV':(2,1),
          'STORE':(2,0),
          'LOAD':(1,1),
          'DUP':(1,2),
          'EQ':(2,1),
          'NT':(1,1),
          'GREATER':(2,1),
          'LESS':(2,1),
          'MOD':(2,1),
          'INPUT':(0,1),
          'OUTPUT':(1,0),
          'OUTPUT_NUM':(1,0)
        }

def verify_stack_size(ast, MAX, logger):
    for name in ast:
        stack = 0
        for op_type, op in ast[name]:
            if isinstance(op, int):
                stack += 1
            elif isinstance(op, (list, tuple)):
                stack += len(op)
            stack -= EFFECT[op_type][0]
            if stack >= 0:
                stack += EFFECT[op_type][1]
            else:
                return op_type, name
        if stack != 0:
            logger.warning('Stack not empty at end of function %s, '
                           'could cause memory leak' % name)
