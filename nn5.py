import islpy as isl
from lift4.parser import Parser
from lift4.check import check_stmts
from lift4.compile import compile
from lift4.contract import contract_arrays
from lift4.codegen import codegen
from lift4.asmjs_formatter import format_asmjs

p = Parser(filename='<string>')

with open("nn.model", "r") as f:
    SOURCE = f.read()

table = check_stmts(p.parse(SOURCE))
context = compile(table)
contract_arrays(context)
ast = codegen(context)
print format_asmjs("Model", table, context, ast)
