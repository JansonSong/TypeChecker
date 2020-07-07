from classtype import ClassType

color_print = {
    'WARNING': '\033[95m',
    'ERROR': '\031[95m',
    'END': '\033[0m'
}

class Variates:
    def __init__(self, classType):
        self.variates = {}
        self.classType = classType

    def add_new_variate(self, var_name, type_name):
        if self.variates.get(var_name) is None:
            self.variates[var_name] = type_name
        else:
            if not self.classType.check_two_consistent(self.variates[var_name], type_name):
                self.raise_incompatible_type_warning(var_name, self.variates[var_name], type_name)

    def get_var_type(self, var_name):
        return self.variates[var_name]

    def raise_incompatible_type_warning(self, var_name, type_name1, type_name2):
        print(color_print['WARNING'], "warning: ", color_print['END'],
        f"Incompatible types in assignment ('{var_name}' has type '{type_name1}', variable has type '{type_name2}'")

    def __str__(self):
        return str(self.variates)