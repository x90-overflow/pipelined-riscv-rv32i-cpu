import sys
sys.path.insert(0, "verification")
from riscv_assembler import lui, addi, sw, jal

transmit_message = "This is my first cpu"

program = []
program.append(lui(1, 0x10000))
program.append(addi(1, 1, 4))

loopback_loc = len(program)

for cha in transmit_message:
    program.append(addi(2, 0, ord(cha)))
    program.append(sw(2, 1, 0))

jump_loc = len(program)

j_offset = (loopback_loc - jump_loc) * 4
program.append(jal(0, j_offset))

with open("fpga/instructions.hex", "w") as f:
    for word in program:
        f.write(f"{word:08X}\n")
