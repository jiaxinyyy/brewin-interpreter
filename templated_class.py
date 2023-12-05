class TClassDef:
    def __init__(self, class_source, interpreter):
        self.name = class_source[1]
        self.class_source = class_source
        self.parametrized_types = class_source[2] # a list of parametrized types 


