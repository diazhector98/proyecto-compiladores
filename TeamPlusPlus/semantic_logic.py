from TeamPlusPlus.DirectorioFunciones import VariableTableRecord, VarType, FunctionDirectoryRecord

class SemanticHandler:
    
    global_var_table = dict()   
    current_var_table = dict()
    functions_directory = dict()


    def set_init_func(self, func_name, type):
        self.functions_directory[func_name] = FunctionDirectoryRecord(
            name = func_name,
            type = type
        )