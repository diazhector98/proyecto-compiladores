from virtual_machine.common.operator import Operator

def handle_arithmetic_operator(quadruple, memory):
    operator = quadruple.operator
    left_operand = quadruple.left_operand
    right_operand = quadruple.right_operand
    result = quadruple.result

    if operator == Operator.ASSIGN:
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
    if operator == Operator.AND:
        operation_outcome = left_operand_value and right_operand_value
    if operator == Operator.OR:
        operation_outcome = left_operand_value or right_operand_value
        
    memory.write(result, operation_outcome)
