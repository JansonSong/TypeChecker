from ast import NodeVisitor, parse, dump, NodeVisitor
from ast import Assign, AnnAssign, AugAssign, Name, BinOp, Str, Num, ClassDef
from ast import alias, Import, ImportFrom
import copy

USER_DEFINE = 'user-defined'
THIRDPARTY_DEFINE = 'third-party define'
BUILTIN_DEFINE = 'built-in define'

class ImportModule:
    def __init__(self, modulename, filepath, classdef, variates):
        self.modulename = modulename
        self.filepath = filepath
        self.classdef = classdef # use hj and cx's typedef
        self.variates = variates # use hj and cx's typedef

class CurFileImport:
    def __init(self, curfile):
        self.curfile = curfile
        self.modules = []

    def add_new_module(self, module: ImportModule):
        self.modules.append(module)

    def find_module(self, module: ImportModule):
        for md in self.modules:
            if md.modulename == module.modulename: # use modulename or filepath?
                return True

        return False


class ImportContent:
    def __init__(self, modulename, asname, filepath, typemodule=USER_DEFINE, hascontent = False, content=[]):
        self.__modulename = modulename
        self.__asname = asname
        self.__filepath = filepath
        self.__typemodule = typemodule
        self.get_file_content()
        self.hascontent = hascontent
        self.__content = content # used to store types and variates' names

    def get_file_content(self):
        if self.__typemodule == BUILTIN_DEFINE:
            return
        else:
            self.__source = open(file=self.__filepath, mode="r+").read()
            self.__tree = parse(self.__source, self.__filepath, mode="exec")
        return

    def get_ast_tree(self):
        return self.__tree

    def get_content(self):
        return self.__content

class ImportParse(NodeVisitor):
    def __init__(self, filename):
        self.source = open(file=filename, mode="r+").read()
        self.tree = parse(self.source, filename, mode="exec")
        self.moduleList = []

    def check(self):
        print(dump(self.tree))
        super().visit(self.tree)

    def visit_Import(self, node: Import):
        for name in node.names:
            modulename, asname, filepath, typemodule = self.get_module_info(name)
            if modulename is None:
                continue
            print(modulename, asname, filepath)
            self.moduleList.append(ImportContent(modulename, asname, filepath, typemodule))
        

    def visit_ImportFrom(self, node: ImportFrom):
        print(dump(node))
        modulename = node.module
        _, _, filepath, typemodule = self.get_module_info(alias(name=modulename, asname=None))
        content = []
        for name in node.names:
            content.append({'name': name.name, 'asname': name.asname})

        self.moduleList.append(ImportContent(modulename, None, filepath, typemodule, True, content))

        

    def get_module_info(self, node: alias):
        try:
            module = __import__(node.name)
        except:
            # No module named node.name
            return None, None, None, None
        try:
            filepath = module.__file__
        except:
            return node.name, node.asname, None, BUILTIN_DEFINE

        return node.name, node.asname, filepath, USER_DEFINE
        

    
def main():
    handle = ImportParse('testtre.py')
    handle.check()

if __name__ == '__main__':
    main()