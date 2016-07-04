from lift2.parser import Parser
from lift2.check import check_stmts
from lift2.interp import interp
from lift2.interp import Array

p = Parser(filename='<string>')

SOURCE = (
"""
Input :: (in 2)
W1 :: (in 2 2)
B1 :: (in)
W2 :: (in 2 2)
B2 :: (in)
Output :: (out 2)

sigmoid"0 := (1 / ((exp (0 - y)) + 1))
dot"1 1 := ((reduce 1 +) (x * y))

Hidden := (sigmoid ((W1 dot Input) + B1))
Output := (sigmoid ((W2 dot Hidden) + B2))

Target :: (in 2)
Loss :: (out)

Loss := ((reduce 1 +) (0.5 * ((Target - Output) ** 2)))

dW1 :: (grad Loss W1)
dW2 :: (grad Loss W2)

nW1 :: (out 2 2)
nW2 :: (out 2 2)

nW1 := (W1 - (0.5 * dW1))
nW2 := (W2 - (0.5 * dW2))
""")


table = check_stmts(p.parse(SOURCE))
values = interp(
    table,
    W1 = Array((2,2), [0.15,0.20,0.25,0.30]),
    B1 = Array((), [0.35]),
    W2 = Array((2,2), [0.40,0.45,0.50,0.55]),
    B2 = Array((), [0.60]),
    Input = Array((2,), [0.05,0.10]),
    Target = Array((2,), [0.01,0.99]))

assert (values[table.symbols["Output"]]
        .allclose(Array((2,), [0.75136507,0.772928465])))

assert (values[table.symbols["Loss"]]
        .allclose(Array((), [0.298371109])))

assert (values[table.symbols["nW1"]]
        .allclose(
            Array((2,2),
                  [0.149780716, 0.19956143, 0.24975114, 0.29950229])))

assert (values[table.symbols["nW2"]]
        .allclose(
            Array((2,2),
                  [0.35891648, 0.408666186, 0.511301270, 0.561370121])))
