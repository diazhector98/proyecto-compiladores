from virtual_machine.common.operator import Operator
from virtual_machine.memory.block_type import BlockType

"""
Este archivo contiene funciones de ayuda para manejar cuádruplos aritméticos y booleanos
El proposito de este archivo fue evitar sobrecargar el archvio de la clase VirtualMachine.

"""

def handle_arithmetic_operator(quadruple, memory):
    """
        Función que maneja las acciones para cuádruplos con operadores aritméticos.
        param quadruple: cuádruplo con operador aritmético
        param memory: memoria de la máquina virtual de tipo VirtualMachineMemory
    """
    operator = quadruple.operator
    left_operand = quadruple.left_operand
    right_operand = quadruple.right_operand
    result = quadruple.result

    # Si el operador es ASSIGN, se debe
    # checar si la dirección a donde se escribe es
    # un apuntador
    if operator == Operator.ASSIGN:
        if address_is_pointer(result):
            # Si la dirección a donde se escribe es un apuntador
            # primero se obtiene la dirección que almacena
            # del apuntador
            address_of_pointer = memory.pointers_block.read(result, BlockType.POINTER)
            left_operand_value = memory.read(left_operand)
            memory.write(address_of_pointer, left_operand_value)
        else:
            value = memory.read(left_operand)
            memory.write(result, value)
        return

    left_operand_value = memory.read(left_operand)
    right_operand_value = memory.read(right_operand)

    if operator == Operator.SUM:
        operation_outcome = left_operand_value + right_operand_value
        memory.write(result, operation_outcome)
    if operator == Operator.MULTIPLY:
        operation_outcome = left_operand_value * right_operand_value
        memory.write(result, operation_outcome)
    if operator == Operator.MINUS:
        operation_outcome = left_operand_value - right_operand_value
        memory.write(result, operation_outcome)
    if operator == Operator.DIVIDE:
        operation_outcome = left_operand_value / right_operand_value
        memory.write(result, operation_outcome)

def handle_boolean_operator(quadruple, memory):
    """
        Función que maneja las acciones para cuádruplos con operadores booleanos.
        param quadruple: cuádruplo con operador booleano
        param memory: memoria de la máquina virtual de tipo VirtualMachineMemory
    """
    operator = quadruple.operator
    left_operand = quadruple.left_operand
    right_operand = quadruple.right_operand
    result = quadruple.result

    left_operand_value = memory.read(left_operand)
    right_operand_value = memory.read(right_operand)

    if operator == Operator.GT:
        operation_outcome = left_operand_value > right_operand_value
    if operator == Operator.LT:
        operation_outcome = left_operand_value < right_operand_value
    if operator == Operator.GTE:
        operation_outcome = left_operand_value >= right_operand_value
    if operator == Operator.LTE:
        operation_outcome = left_operand_value <= right_operand_value
    if operator == Operator.EQUAL:
        operation_outcome = left_operand_value == right_operand_value
    if operator == Operator.NE:
        operation_outcome = left_operand_value != right_operand_value
        
    memory.write(result, operation_outcome)

def address_is_pointer(address):
    """
        Funcion que regresa True si la dirección dada corresponde a un apuntador.
        Esta función es útil en el manejo de operadores aritméticos
        para saber si leer UNA (solo valor) vez o DOS (dirección y valor) veces de memoria
        param address: variable entera que representa una dirección de memoria
    """
    return address >= 20000
