from classv2 import ClassDef, TClassDef
from intbase import InterpreterBase, ErrorType
from bparser import BParser
from objectv2 import ObjectDef
from type_valuev2 import TypeManager

# need to document that each class has at least one method guaranteed

# Main interpreter class
class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)
        self.trace_output = trace_output

    # run a program, provided in an array of strings, one string per line of source code
    # usese the provided BParser class found in parser.py to parse the program into lists
    def run(self, program):
        status, parsed_program = BParser.parse(program)
        if not status:
            super().error(
                ErrorType.SYNTAX_ERROR, f"Parse error on program: {parsed_program}"
            )
        self.__add_all_class_types_to_type_manager(parsed_program)
        self.__map_class_names_to_class_defs(parsed_program)

        # instantiate main class
        invalid_line_num_of_caller = None
        self.main_object = self.instantiate(
            InterpreterBase.MAIN_CLASS_DEF, invalid_line_num_of_caller
        )

        # call main function in main class; return value is ignored from main
        self.main_object.call_method(
            InterpreterBase.MAIN_FUNC_DEF, [], False, invalid_line_num_of_caller
        )

        # program terminates!

    # user passes in the line number of the statement that performed the new command so we can generate an error
    # if the user tries to new an class name that does not exist. This will report the line number of the statement
    # with the new command
    def instantiate(self, class_name, line_num_of_statement):
        if class_name in self.class_index: # class_name: template@type1@type2...
            class_def = self.class_index[class_name]
        else:
            class_and_types = class_name.split(InterpreterBase.TYPE_CONCAT_CHAR) # [class_name, type1, type2, ...]
            tclass_name = class_and_types[0]
            concrete_types = class_and_types[1:]
            # if templated class
            if tclass_name in self.tclass_index:
                tclass_def = self.tclass_index[tclass_name] 
                new_tclass_source = self.__convert_tclass(tclass_def, class_name, concrete_types)
                class_def = ClassDef(new_tclass_source, self)
            else:
                super().error(
                    ErrorType.TYPE_ERROR,
                    f"No class named {class_name} found",
                    line_num_of_statement,
                )
        obj = ObjectDef(
            self, class_def, None, self.trace_output
        )  # Create an object based on this class definition
        return obj

    # returns a ClassDef object
    def get_class_def(self, class_name, line_number_of_statement):
        if class_name not in self.class_index:
            super().error(
                ErrorType.TYPE_ERROR,
                f"No class named {class_name} found",
                line_number_of_statement,
            )
        return self.class_index[class_name]

    # returns a bool
    def is_valid_type(self, typename):
        return self.type_manager.is_valid_type(typename)

    # returns a bool
    def is_a_subtype(self, suspected_supertype, suspected_subtype):
        return self.type_manager.is_a_subtype(suspected_supertype, suspected_subtype)

    # typea and typeb are Type objects; returns true if the two type are compatible
    # for assignments typea is the type of the left-hand-side variable, and typeb is the type of the
    # right-hand-side variable, e.g., (set person_obj_ref (new teacher))
    def check_type_compatibility(self, typea, typeb, for_assignment=False):
        return self.type_manager.check_type_compatibility(typea, typeb, for_assignment)

    def __map_class_names_to_class_defs(self, program):
        self.class_index = {}
        self.tclass_index = {}
        for item in program:
            if item[0] == InterpreterBase.CLASS_DEF:
                if item[1] in self.class_index:
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f"Duplicate class name {item[1]}",
                        item[0].line_num,
                    )
                self.class_index[item[1]] = ClassDef(item, self)
            elif item[0] == InterpreterBase.TEMPLATE_CLASS_DEF:
                if item[1] in self.tclass_index:
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f"Duplicate templated class name {item[1]}",
                        item[0].line_num,
                    )
                # Templated Class Definitions 
                self.tclass_index[item[1]] = TClassDef(item, self)              

    # [class classname inherits superclassname [items]]
    def __add_all_class_types_to_type_manager(self, parsed_program):
        self.type_manager = TypeManager()
        for item in parsed_program:
            if item[0] == InterpreterBase.CLASS_DEF:
                class_name = item[1]
                superclass_name = None
                if item[2] == InterpreterBase.INHERITS_DEF:
                    superclass_name = item[3]
                self.type_manager.add_class_type(class_name, superclass_name)
            # if item[0] == InterpreterBase.TEMPLATE_CLASS_DEF:
            #     class_name = item[1]
            #     self.type_manager.add_class_type(class_name)
    
    def __replace_with_concrete_type(self, source, parameterized_type, concrete_type):
        new_source = []
        for item in source:
            if isinstance(item, list):
                new_item = self.__replace_with_concrete_type(item, parameterized_type, concrete_type)
            elif isinstance(item, str) and item == parameterized_type:
                new_item = concrete_type
            else:
                new_item = item
            new_source.append(new_item)
        return new_source

    
    def __convert_tclass(self, tclass_def, class_name, concrete_types):
        new_tclass_source = tclass_def.class_source
        # convert tclass_def to concrete class_def
        new_tclass_source[0] = 'class'
        # replace the class name with class1@type1@type2...
        new_tclass_source[1] = class_name
        # replace each parametrized type with the concrete type
        for parameterized_type, concrete_type in zip(tclass_def.parameterized_types, concrete_types):
            new_tclass_source = self.__replace_with_concrete_type(new_tclass_source, parameterized_type, concrete_type)
        # format of template_at_para_types: "node@field_type"
        template_at_para_type = tclass_def.name + InterpreterBase.TYPE_CONCAT_CHAR + InterpreterBase.TYPE_CONCAT_CHAR.join([t for t in tclass_def.parameterized_types])
        # format of template_at_para_types: "node@int"
        template_at_concr_type = tclass_def.name + InterpreterBase.TYPE_CONCAT_CHAR + InterpreterBase.TYPE_CONCAT_CHAR.join([t for t in concrete_types])
        new_tclass_source = self.__replace_with_concrete_type(new_tclass_source, template_at_para_type, template_at_concr_type)
        # print(new_tclass_source)
        return new_tclass_source
