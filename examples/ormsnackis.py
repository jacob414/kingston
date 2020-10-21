"""
Tiny AST to code thingy.
~~~~~~~~~~~~~~~~~~~~~~~~

Hm.
"""
import ast
import funcy as fy

from typing import Any

from kingston.match import Matcher, TypeMatcher, ValueMatcher

nodeRep:Matcher[ast.AST, str] = TypeMatcher({
    ast.Interactive: lambda: '',
    ast.FunctionDef: lambda node: f"def {node.name}(",
    ast.arguments: lambda node: ','.join(arg.arg for arg in node.args)+'):\n',
    ast.BinOp: lambda node: '',
    ast.Constant: lambda node: str(node.value),
    ast.Return: lambda node: '    return ',
    ast.Add: lambda: ' + ',
})

afunc = """
def helo():
    return 1 + 1
"""

def test():
    tree = compile(afunc, 'examples.unify', 'single', ast.PyCF_ONLY_AST)
    print(''.join(nodeRep(node) for node in full))

if __name__ == '__main__':
    test()
