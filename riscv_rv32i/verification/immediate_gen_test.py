import cocotb 
from cocotb.triggers import Timer
from test_utils import MASK, get_bits, sign_extend, Scoreboard
import random

OP_IMM = 0b0010011
LOAD = 0b0000011
JALR = 0b1100111
STORE = 0b0100011
BRANCH = 0b1100011
JAL = 0b1101111
LUI = 0b0110111
AUIPC = 0b0010111

def immgen_reference(instr):
    opcode = get_bits(instr, 6, 0)
    if opcode in (OP_IMM, LOAD, JALR):
        imm = get_bits(instr, 31, 20)
        return sign_extend(imm, 12)
    elif opcode == STORE:
        imm = (get_bits(instr, 31, 25) << 5) | get_bits(instr, 11, 7)
        return sign_extend(imm, 12)
    elif opcode == BRANCH:
        imm = (get_bits(instr, 31, 31) << 12) | (get_bits(instr, 7, 7) << 11) \
           | (get_bits(instr, 30, 25) << 5) | (get_bits(instr, 11, 8) << 1)
        return sign_extend(imm, 13)
    elif opcode == JAL:
        imm = (get_bits(instr, 31, 31) << 20) | (get_bits(instr, 19, 12) << 12) \
            | (get_bits(instr, 20, 20) << 11) | (get_bits(instr, 30, 21) << 1)
        return sign_extend(imm, 21)
    elif opcode in (LUI, AUIPC):
        return (get_bits(instr, 31, 12) << 12) & MASK
    else:
        return 0

@cocotb.test()
async def test_immediate_gen(dut):
    opcodes = [OP_IMM, LOAD, JALR, STORE, BRANCH, JAL, LUI, AUIPC]
    scoreboard = Scoreboard("Immediate Generation Testing")

    for _ in range(2000):
        opcode = random.choice(opcodes)
        instr = random.randint(0, MASK)
        instr = (instr & ~0x7F) | opcode

        dut.instr.value = instr
        await Timer(1, "ns")
        actual = int(dut.imm.value)

        expected = immgen_reference(instr)
        scoreboard.check(expected, actual, f"instr={instr:#010x} opcode={opcode:07b}")
    dut._log.info(f"{scoreboard.checks} checks, {scoreboard.errors} errors")
        

    
