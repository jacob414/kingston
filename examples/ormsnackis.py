"""
Tiny AST to code thingy.
~~~~~~~~~~~~~~~~~~~~~~~~

Hm.
"""
import ast

from kingston.match import Matcher, TypeMatcher, ValueMatcher

nodeRep:Matcher[ast.AST, str] = TypeMatcher({
    ast.Interactive: lambda: '',
    ast.FunctionDef: lambda node: f"def {node.name}(",
    ast.arguments: (lambda node: ','.join(arg.arg
                                         for arg in node.args) +
                    '):\n'),
    ast.BinOp: lambda node: '',
    ast.Constant: lambda node: str(node.value),
    ast.Return: lambda node: '    return ',
    ast.Add: lambda: ' + ',
})

topnode = compile("""
def helo():
    return 1 + 1
""", 'examples.ormsnackis', 'single', ast.PyCF_ONLY_AST)


def test(tree):
    print(''.join(nodeRep(node) for node in ast.walk(tree)))

if __name__ == '__main__':
    test(topnode)
