def optimize(ast, MAX):
    changed = True
    while changed:
        changed = False 
        for name in ast:
            block = ast[name]
            for i, x in enumerate(block):
                try:
                    if changed:
                        break
                    if x[0] == 'OUTPUT' and block[i + 1][0] == 'OUTPUT':
                        if isinstance(block[i][1], tuple):
                            if isinstance(block[i + 1][1], tuple):
                                block[i:i + 2] = [('OUTPUT',
                                                   x[1] + block[i + 1][1],
                                                   block[i][2])]
                                changed = True
                    elif x[0] == 'INT' and ast[name][i + 1][0] != 'INT':
                        if block[i + 1][0] == 'ADD':
                            block[i:i + 2] = [('ADD', x[1], block[i][2])]
                            changed = True
                        elif block[i + 1][0] == 'SUB':
                            block[i:i + 2] = [('SUB', x[1], block[i][2])]
                            changed = True
                        elif block[i + 1][0] == 'MUL':
                            block[i:i + 2] = [('MUL', x[1], block[i][2])]
                            changed = True
                        elif block[i + 1][0] == 'DIV':
                            block[i:i + 2] = [('DIV', x[1], block[i][2])]
                            changed = True
                        elif block[i + 1][0] == 'DUP':
                            block[i + 1] = ('INT', block[i][1], block[i + 1][2])
                            changed = True
                        elif block[i + 1][0] == 'STORE':
                            block[i:i + 2] = [('STORE', x[1], block[i][2])]
                            changed = True
                        elif block[i + 1][0] == 'LOAD':
                            if isinstance(block[i + 1][1], str):
                                block[i:i + 2] = [('LOAD', x[1], block[i][2])]
                                changed = True
                        elif block[i + 1][0] == 'OUTPUT':
                            if isinstance(block[i + 1][1], str):
                                block[i:i + 2] = [('OUTPUT', (x[1],),
                                                   block[i][2])]
                                changed = True
                        elif block[i + 1][0] == 'OUTPUT_NUM':
                            if isinstance(block[i + 1][1], str):
                                block[i:i + 2] = [('OUTPUT_NUM', x[1],
                                                   block[i][2])]
                                changed = True
                    elif x[0] == 'INT' and ast[name][i + 1][0] == 'INT':
                        if block[i + 2][0] == 'ADD':
                            num = (block[i][1] + block[i + 1][1]) % MAX
                            block[i:i + 3] = [('INT', num, block[i][2])]
                            changed = True
                        elif block[i + 2][0] == 'SUB':
                            num = (block[i][1] - block[i + 1][1]) % MAX
                            block[i:i + 3] = [('INT', num, block[i][2])]
                            changed = True
                        elif block[i + 2][0] == 'MUL':
                            num = (block[i][1] * block[i + 1][1]) % MAX
                            block[i:i + 3] = [('INT', num, block[i][2])]
                            changed = True
                        elif block[i + 2][0] == 'DIV':
                            num = (block[i][1] // block[i + 1][1]) % MAX
                            block[i:i + 3] = [('INT', num, block[i][2])]
                            changed = True
                        elif block[i + 2][0] == 'STORE':
                            block[i:i + 3] = [('STORE',
                                               (block[i][1], block[i + 1][1]),
                                               block[i][2])]
                except IndexError:
                    pass
                if changed:
                    ast[name] = block
                    break
    return ast
