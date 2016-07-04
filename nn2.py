from lift1.parser import Parser
from lift1.check import check_stmts
from lift1.interp import interp
from lift1.interp import Array

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
""")


table = check_stmts(p.parse(SOURCE))
values = interp(
    table,
    W1 = Array((2,2), [0.15,0.20,0.25,0.30]),
    B1 = Array((), [0.35]),
    W2 = Array((2,2), [0.40,0.45,0.50,0.55]),
    B2 = Array((), [0.60]),
    Input = Array((2,), [0.05,0.10]))

assert (values[table.symbols["Output"]]
        .allclose(Array((2,), [0.75136507,0.772928465])))
