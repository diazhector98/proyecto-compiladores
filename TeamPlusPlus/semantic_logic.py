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

    def set_parametros(self, parametros):
        for (param_name, param_var_type) in params:
            self.current_var_table[param_name] = VariableTableRecord(
                name=param_name,
                type=param_var_type
                )