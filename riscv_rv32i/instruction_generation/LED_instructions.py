import sys
sys.path.insert(0, "verification")
from riscv_assembler import lui, addi, sw, jal

program = [lui(1, 0x10000), addi(2, 0, 0), sw(2, 1, 0), addi(2, 2, 1), jal(0, -8)]

with open("fpga/instructions.hex", "w") as f:
    for word in program:
        f.write(f"{word:08X}\n")
