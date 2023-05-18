import sys
from binary_encoding import *
from opc_gen_info import *
from error_checker import *

error_counter = []  # This list stores all the error statements which would get printed out.
empty_string = [" "]

# Takes assembly program input from STDIN
assembly_program = []
while True:
    try:
        assembly_line = input()
        assembly_program.append(assembly_line)
    except EOFError:
        break

# Ignores empty lines
assembly_program_final = [line for line in assembly_program if line.strip()]

if not assembly_program_final:
    print(" ")
else:
    list_of_var_indx = [i for i, line in enumerate(assembly_program_final) if line.startswith("var")]

    for i in list_of_var_indx:
        lst_line = assembly_program_final[i].strip().split()
        if len(lst_line) != 2:
            error_counter.append(f'Error: Type-Var: Illegal Variable Declaration: Expected length 2 but length {len(lst_line)} was found on line {i + 1}.')

    list_of_instructions = []  # Stores list of instructions
    list_of_labelsdeclared = []  # Stores all declared labels
    list_of_labelsdeclared2 = []  # Stores all declared labels with line number

    for i, line in enumerate(assembly_program_final):
        lst_line = line.strip().split()
        first = lst_line[0]
        if first[-1] == ":":
            label_name = first[:-1]
            list_of_labelsdeclared.append(label_name)
            list_of_labelsdeclared2.append((label_name, i))
            if len(lst_line) > 1:
                list_of_instructions.append(lst_line[1:])
            else:
                list_of_instructions.append(empty_string)  # To prevent indexing problem
        else:
            list_of_instructions.append(lst_line)

    var_count = len(list_of_var_indx)

    for i, instruction in enumerate(list_of_instructions):
        first_exp = instruction[0]
        if first_exp not in listofinstructions:
            error_counter.append(f'Error: Invalid Syntax: "{first_exp}" at line {i + 1} is not a recognised instruction as per the ISA')
        else:
            type_inst = opcodes[first_exp][1]

            if len(instruction) != num_inputs_instruction[type_inst]:
                error_counter.append(f'Error: Invalid Syntax: Instruction {first_exp} is of type "{type_inst}" and requires "{num_inputs_instruction[type_inst]}" number of arguments but on line {i + 1} for this expression {len(instruction)} number arguments were detected.')

            if type_inst == 'A':
                if len(instruction) == 4:
                    for reg in instruction[1:4]:
                        if not register_validity(reg):
                            error_counter.append(f'Error: Invalid Syntax: "{reg}" at line {i + 1} is not a valid register.')
                        if reg == 'FLAGS':
                            error_counter.append(f'Error: Illegal Use of Flags: FLAGS Register cannot be used with instruction {first_exp} at line number {i + 1}.')

            if type_inst == 'B':
                if len(instruction) == 3:
                    if not register_validity(instruction[1]):
                        error_counter.append(f'Error: Invalid Syntax: "{instruction[1]}" at line {i + 1} is not a valid register.')
                    if instruction[1] == 'FLAGS':
                        error_counter.append(f'Error: Illegal Use of Flags: FLAGS Register cannot be used with instruction {first_exp} at line number {i + 1}.')
                    try:
                        imm = int(instruction[2])
                        if imm < 0:
                            error_counter.append(f'Error: Invalid Syntax: Immediate value cannot be negative at line {i + 1}.')
                    except ValueError:
                        error_counter.append(f'Error: Invalid Syntax: "{instruction[2]}" at line {i + 1} is not a valid immediate.')

            if type_inst == 'C':
                if len(instruction) == 2:
                    if not labelValid(instruction[1]):
                        error_counter.append(f'Error: Invalid Syntax: "{instruction[1]}" at line {i + 1} is not a valid label.')

    for i, (label_name, label_line) in enumerate(list_of_labelsdeclared2):
        if label_name in [label for label, line in list_of_labelsdeclared2[i + 1:]]:
            error_counter.append(f'Error: Label Repeated: "{label_name}" at line number {label_line + 1} and {i + 2}.')

    for i, (label_name, label_line) in enumerate(list_of_labelsdeclared2):
        if label_name not in [label for label, line in list_of_labelsdeclared2[i + 1:]]:
            error_counter.append(f'Error: Illegal Jump: Label "{label_name}" at line number {label_line + 1} is not defined/declared.')

    if not error_counter:
        error_counter.append('0 errors')

    for error in error_counter:
        print(error)
