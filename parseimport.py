from ast import NodeVisitor, parse, dump, NodeVisitor
from ast import Assign, AnnAssign, AugAssign, Name, BinOp, Str, Num, ClassDef
from ast import alias, Import, ImportFrom
import copy
import os
import time

USER_DEFINE = 'user-defined'
THIRDPARTY_DEFINE = 'third-party define'
BUILTIN_DEFINE = 'built-in define'


class ImportModule:
    def __init__(self, modulename, filepath, classdef: list, variates: list, fundef: list, last_visit_time):
        self.filepath = filepath
        self.classdef = classdef
        self.variates = variates
        self.fundef = fundef
        self.last_visit_time = last_visit_time

    def get_module_content(self):
        last_modify_time = time.ctime(os.path.getmtime(self.filepath))
        if last_modify_time > self.last_visit_time:
            return False # need to refresh this module's name
        else:
            return True # can read content directly

    def modify_last_visit_time(self, last_visit_time):
        self.last_visit_time = last_visit_time

    def get_classdef(self):
        return self.classdef

    def get_variates(self):
        return self.variates

    def get_fundef(self):
        return self.fundef
        

class CurFileImport:
    def __init(self, curfile):
        self.curfile = curfile
        self.modules = []

    def add_new_module(self, module: ImportModule):
        self.modules.append(module)

    def find_module(self, module: ImportModule):
        for md in self.modules:
            if md.filepath == module.filepath:
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
        self.curdirpath = os.path.dirname(filename)

    def check(self):
        print(dump(self.tree))
        super().visit(self.tree)

    def visit_Import(self, node: Import):
        for name in node.names:
            modulename, asname, filepath, typemodule = self.get_module_info(name, self.curdirpath)
            if modulename is None:
                continue
            print(modulename, asname, filepath)
            self.moduleList.append(ImportContent(modulename, asname, filepath, typemodule))
        

    def visit_ImportFrom(self, node: ImportFrom):
        print(dump(node))
        modulename = node.module
        curdirpath = self.curdirpath
        isfolder = False
        filepath = ""
        typemodule = USER_DEFINE
        if modulename == None:
            if node.level == 1:
                pass
            elif node.level == 2:
                curdirpath = os.path.dirname(curdirpath)
            isfolder = True
        else:
            path = self.curdirpath + "/" + modulename
            if os.path.exists(path):
                curdirpath = path
                isfolder = True
        
        if isfolder:
            content = []
            for name in node.names:
                path = curdirpath + "/" + name.name + ".py"
                if os.path.exists(path):
                    modulename, asname, filepath, typemodule = self.get_module_info(name, curdirpath)
                    if modulename is None:
                        continue
                    self.moduleList.append(ImportContent(modulename, asname, filepath, typemodule))
                else:
                    
                    content.append({'name': name.name, 'asname': name.asname})
            
            self.moduleList.append(ImportContent(modulename, None, filepath, typemodule, True, content))
            return

        modulename, asname, filepath, typemodule = self.get_module_info(alias(name=modulename, asname=None), curdirpath)
        content = []
        for name in node.names:
            content.append({'name': name.name, 'asname': name.asname})

        self.moduleList.append(ImportContent(modulename, None, filepath, typemodule, True, content))

        

    def get_module_info(self, node: alias, curdirpath):
        path = curdirpath + '/' + node.name
        if os.path.exists(path): # this module is a packet
            path += "/__init__.py" # default existing this file
            return node.name, node.asname, path, USER_DEFINE
        
        path += ".py"
        if os.path.exists(path): # this module is a file
            return node.name, node.asname, path, USER_DEFINE


        module = __import__(node.name, fromlist=[curdirpath])
        try:
            module = __import__(node.name)
        except:
            # No module named node.name
            return None, None, None, None
        try:
            filepath = module.__file__
        except:
            return node.name, node.asname, None, BUILTIN_DEFINE

        return node.name, node.asname, filepath, THIRDPARTY_DEFINE
        

    
def main():
    handle = ImportParse('C:/Users/Administrator/Desktop/python project/TypeChecker/test/test.py')
    handle.check()

if __name__ == '__main__':
    main()