import compiler, inspect
from annotations import types, returns
from gltypes import vec3, vec4

VALID_TYPES = 'float vec2 vec3 vec4'.split()

def to_glsl(f):
    out = []
    tree = compiler.parse(inspect.getsource(f))
    functions = tree.node.nodes
    for func in functions:
        assert isinstance(func, compiler.ast.Function)
        returnType = f.func_annotation['return'].__name__
        assert returnType in VALID_TYPES
        out.append('%s %s() {' % (returnType, func.name))
        out.append(code_to_glsl(func.code))
        out.append('}')
    out.append('void mainImage(out vec4 fragColor, in vec2 fragCoord) {fragColor = render(); }')
    return '\n'.join(out)
        
def code_to_glsl(code):
    for statement in code.nodes:
        if isinstance(statement, compiler.ast.Return):
            return 'return %s;' % expression_to_glsl(statement.value)

def expression_to_glsl(expr):
    if isinstance(expr, compiler.ast.Name):
        return expr.name
    return '(%s)' % _expression_to_glsl(expr)
def _expression_to_glsl(expr):
    if isinstance(expr, compiler.ast.Const):
        return repr(expr.value)
    if isinstance(expr, compiler.ast.Add):
        return binop_to_glsl('+', expr.left, expr.right)
    if isinstance(expr, compiler.ast.Mul):
        return binop_to_glsl('*', expr.left, expr.right)
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
    return vec4(1.0, 0.0, 0.0, 1.0) * sin(iGlobalTime) + vec4(0.0, 1.0, 0.0, 1.0) * cos(iGlobalTime)

print to_glsl(render)
