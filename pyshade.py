import compiler, inspect
from annotations import types, returns
from gl import *

VALID_TYPES = 'float vec2 vec3 vec4'.split()

def to_glsl(*functions):
    out = []
    for f in functions:
        tree = compiler.parse(inspect.getsource(f))
        func, = tree.node.nodes
        assert isinstance(func, compiler.ast.Function)
        returnType = f.func_annotation['return'].__name__
        assert returnType in VALID_TYPES
        out.append('%s %s() {' % (returnType, func.name))
        out.append(code_to_glsl(func.code))
        out.append('}')
    out.append('void mainImage(out vec4 fragColor, in vec2 fragCoord) {fragColor = render(); }')
    return '\n'.join(out)
        
def code_to_glsl(code):
    out = []
    variables = set()
    for statement in code.nodes:
        if isinstance(statement, compiler.ast.Assign):
            assert len(statement.nodes) == 1
            ass_name = statement.nodes[0]
            assert ass_name.flags == 'OP_ASSIGN'
            name = ass_name.name
            if name not in variables:
                variableType = 'vec4'
                out.insert(0, '%s %s;' % (variableType, name))
                variables.add(name)
            out.append('%s = %s;' % (name, expression_to_glsl(statement.expr)))
        elif isinstance(statement, compiler.ast.Return):
            out.append('return %s;' % expression_to_glsl(statement.value))
        else:
            print statement
            assert False
    return '\n'.join(out)

BIN_OPS = {
    compiler.ast.Add: '+',
    compiler.ast.Sub: '-',
    compiler.ast.Mul: '*',
    compiler.ast.Div: '/',
}
def expression_to_glsl(expr):
    if isinstance(expr, compiler.ast.Name):
        return expr.name
    return '(%s)' % _expression_to_glsl(expr)
def _expression_to_glsl(expr):
    if isinstance(expr, compiler.ast.Const):
        return repr(expr.value)
    if expr.__class__ in BIN_OPS:
        return binop_to_glsl(BIN_OPS[expr.__class__], expr.left, expr.right)
    if isinstance(expr, compiler.ast.CallFunc):
        args = ', '.join(expression_to_glsl(arg) for arg in expr.args)
        assert expr.star_args is None
        assert expr.dstar_args is None
        return '%s(%s)' % (expression_to_glsl(expr.node), args)
    print expr
    assert False

def binop_to_glsl(op, left, right):
    return '(%s) %s (%s)' % (expression_to_glsl(left), op, expression_to_glsl(right))

@returns(vec4)
def render():
    a = vec4(1.0, 0.0, 0.0, 1.0)
    b = vec4(0.0, 1.0, 0.0, 1.0)
    return a * sin(iGlobalTime) + b * cos(iGlobalTime)
iGlobalTime = 0.0
assert render() == vec4(0.0, 1.0, 0.0, 1.0), render()
print to_glsl(render)
