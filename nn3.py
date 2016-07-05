from lift2.parser import Parser
from lift2.check import check_stmts
from lift2.interp import interp
from lift2.interp import Array

p = Parser(filename='<string>')

with open("nn.model", "r") as f:
    SOURCE = f.read()

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
