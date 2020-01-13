def interpretacoes(vars):
    
    if len(vars) == 1:
        return [[(vars[0], True)], [(vars[0], False)]]

    res = []
    for l in interpretacoes(vars[:-1]):
        res.append(l+[(vars[-1], True)])
        res.append(l+[(vars[-1], False)])
    return res

def main():
    print(interpretacoes(['a', 'b']))

main()
    
