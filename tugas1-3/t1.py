import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode = b"""
if x > 0: 
    return x 
else: 
    return 0\n
"""
tree = parser.parse(kode)
print(tree.root_node)

for c in tree.root_node.named_children[0].named_children:
    print(c.type, "bernama" if c.is_named else "anonim")
