from DirectorioFunciones import VariableTableRecord, VarType, FunctionDirectoryRecord

class SemanticHandler:
    
    global_var_table = dict()   
    current_var_table = dict()
    functions_directory = dict()


    def set_init_func(self, func_name, t):
        self.functions_directory[func_name] = FunctionDirectoryRecord(
            name = func_name,
            return_type= t
        )

    def set_parametros(self, parametros):
        for (param_name, param_var_type) in parametros:
            self.current_var_table[param_name] = VariableTableRecord(
                name = param_name,
                type = param_var_type
                )