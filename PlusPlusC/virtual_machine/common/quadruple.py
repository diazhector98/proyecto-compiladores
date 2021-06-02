from virtual_machine.common.operator import Operator

"""
    Clase que representa un cuádruplo generado en el proceso de compilación.
    Contiene el operador, el operando izquierdo , el operando derecho y el resultado.

    Se lee una línea de texto con el formato que genera el proceso de compilación.

"""
class Quadruple:
    operator: str
    left_operand: str
    right_operand: str
    temp_result: str

    def __init__(self, output_line):
        """
            En inicialización se divide la línea de texto en sus 4 partes y se procesan
            para convertirlos en sus tipos correspondientes.

            param output_line: variable de texto que representa una línea de cuádruplo generada en el
            archivo de compilación; OPERADOR OPERANDO_IZQ OPERANDO_DER RESULTADO
        """
        string_elements = output_line.split(' ')
        self.string_elements = [e for e in string_elements if e != '']
        self.process_string_elements()

    def process_string_elements(self):
        """
            Convierte los elementos de la línea de salida
            del compilador en sus tipos correspondientes.
            El operador en tipo Operator, los operandos de tipo entero 
            y el resultado en entero si es posible, si no, directamente
            como string (ya que puede ser nombre de función)
        """
        [str_operator, str_left_operand, str_right_operand, str_result] = self.string_elements
        self.operator = Operator(str_operator)
        self.left_operand = int(str_left_operand)
        self.right_operand = int(str_right_operand)
        # TODO: Manejar todos resultados como ints o averiguar como manejar nombres de funciones
        try:
            self.result = int(str_result)
        except Exception:
            self.result = str_result

    def __str__(self):
        """
            Método para imprimir de forma más legible el cuádruplo. Usado
            para debugging.
        """
        return "{:<12} {:<7} {:<7} {:<7}".format(self.operator.name, self.left_operand, self.right_operand, self.result)