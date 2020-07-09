from ast import NodeVisitor, parse, dump, NodeVisitor
from ast import Assign, AnnAssign, AugAssign, Name, BinOp, Str, Num, ClassDef
from variate import Variates
from classtype import ClassType

ErrorType = "ErrorType"

class Handle(NodeVisitor):
    def __init__(self, filename):
        self.source = open(file=filename, mode="r+").read()
        self.tree = parse(self.source, filename, mode="exec")
        self.classtype = ClassType(filename)
        self.variates = Variates(self.classtype)
        print("self.classtype: \n", self.classtype)

    def check(self):
        print(dump(self.tree))
        super().visit(self.tree)

    def get_value_name(self, node):
        varname = super().visit(node)
        return varname

    def visit_Assign(self, node: Assign):
        print(dump(node))
        type_comment = None
        if type(node.value) == BinOp:
            type_comment = super().visit(node.value)
        else:
            if type(node.value) == Name:
                varname = self.get_value_name(node.value)
                type_comment = self.variates.get_var_type(varname)
            else:
                type_comment = super().visit(node.value)
        print("type_comment = ", type_comment)

        for lvalue in node.targets:
            varname = self.get_value_name(lvalue)
            if type_comment != "ErroType":
                self.variates.add_new_variate(varname, type_comment)
            else:
                self.variates.add_new_variate(varname, None)
            print("self.variates: ", self.variates)
            
        

    def visit_AugAssign(self, node: AugAssign):
        print(dump(node))

    def visit_Name(self, node: Name):
        return node.id

    def visit_BinOp(self, node: BinOp):
        type_left = None
        type_right = None
        if type(node.left) == Name:
            varname = self.get_value_name(node.left)
            type_left = self.variates.get_var_type(varname)
        else:
            type_left = super().visit(node.left)
        if type(node.right) == Name:
            varname = self.get_value_name(node.right)
            type_right = self.variates.get_var_type(varname)
        else:
            type_right = super().visit(node.right)
        print(f"typeleft = {type_left}, typeright = {type_right}")
        if self.classtype.check_two_consistent(type_left, type_right):
            return type_left
        else:
            return ErrorType


    def visit_Str(self, node: Str):
        return str

    def visit_Num(self, node: Num):
        return type(node.n)

    def visit_ClassDef(self, node: ClassDef):
        type_name = node.name
        self.classtype.add_type(type_name)

        




def main():
    handle = Handle('testtre.py')
    handle.check()

if __name__ == '__main__':
    main()