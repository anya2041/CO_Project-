from reg import *
from opc_gen_info import *

def register_to_binary(register):
    # Parses Register Encoding for Given Register Name
    return REGISTERS_BINARY.get(register, '000')

def immediate_to_binary(num):
    # Binary value for given immediate
    return bin(int(num))[2:].zfill(8)

def opcode_retriever(instruction):
    # Returns the opcode for the instruction passed as an argument
    return opcodes.get(instruction, '00000')[0]

def memory_address_to_binary(location):
    # Binary Value for Given Memory Address
    return bin(int(location))[2:].zfill(8)
