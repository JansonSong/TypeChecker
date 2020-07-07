import copy
from ast import NodeVisitor, parse, dump, NodeVisitor
from ast import ClassDef, ImportFrom, Import

_const_basic_type = [
    int, float, complex,
    str, bool, tuple,
    list, dict
]

class ClassType(NodeVisitor):
    def __init__(self, filename=""):
        self.filename = filename
        self.typeset = copy.copy(_const_basic_type)
        self.typeconsistent = {}
        self.add_consistent()
        self.analysize_class_type()

    def analysize_class_type(self):
        self.source = open(file=self.filename, mode="r+").read()
        self.tree = parse(self.source, self.filename, mode="exec")
        super().visit(self.tree)
        print(self.typeset)

    def visit_ClassDef(self, node: ClassDef):
        self.typeset.append(node.name)

    def visit_ImportFrom(self, node: ImportFrom):
        filename = node.module + ".py"
        fd = open(file=filename, mode="r+")
        source = fd.read()
        tree = parse(source, filename, mode="exec")
        super().visit(tree)
        pass

    def visit_Import(self, node: Import):
        print("Import: ", node.names)
        
        pass

    def add_type(self, type_name):
        self.typeset.append(type_name)

    def find_type(self, type_name):
        if type_name in self.typeset:
            pass
        else:
            self.typeset.append(type_name)

    def add_consistent(self):
        self.typeconsistent[float] = []
        self.typeconsistent[float].append(int)

    def check_two_consistent(self, type_name1, type_name2):
        if type_name1 == type_name2:
            return True
        if self.typeconsistent.get(type_name1) is not None:
            if type_name2 in self.typeconsistent[type_name1]:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return str(self.typeset)


    