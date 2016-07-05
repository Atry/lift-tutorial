import islpy as isl
from lift3.parser import Parser
from lift3.check import check_stmts
from lift3.compile import compile
from lift3.codegen import codegen
from lift3.asmjs_formatter import format_asmjs

p = Parser(filename='<string>')

with open("nn.model", "r") as f:
    SOURCE = f.read()

table = check_stmts(p.parse(SOURCE))
context = compile(table)
ast = codegen(context)
print format_asmjs("Model", table, context, ast)
