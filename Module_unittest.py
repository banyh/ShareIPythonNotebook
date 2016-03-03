def del_parenthesis(s):
    return ''.join([c for c in s if c not in "()"])

def del_quote(s):
    return ''.join([c for c in s if c not in "\"\'"])
