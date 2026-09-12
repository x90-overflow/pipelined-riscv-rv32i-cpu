import cocotb
from cocotb.triggers import Timer
import random
from test_utils import MASK, to_signed, Scoreboard

BEQ = 0b000
BNE = 0b001
BLT = 0b100
BGE = 0b101
BLTU = 0b110
BGEU = 0b111

def branch_reference(branch, funct3, rs1, rs2):
    rs1 &= MASK
    rs2 &= MASK
    if funct3 == BEQ:
        condition = (rs1 == rs2)
    elif funct3 == BNE:
        condition = (rs1 != rs2)
    elif funct3 == BLT:
        condition = (to_signed(rs1) < to_signed(rs2))
    elif funct3 == BGE:
        condition = (to_signed(rs1) >= to_signed(rs2))
    elif funct3 == BLTU:
        condition = (rs1 < rs2)
    elif funct3 == BGEU:
        condition = (rs1 >= rs2)
    else:
        condition = False

    if(branch & condition):
        return 1
    else:
        return 0

@cocotb.test()
async def test_branch_decode(dut):
    scoreboard = Scoreboard("Branch Testing")
    funct3_codes = [BEQ, BNE, BLT, BGE, BLTU, BGEU]
    for _ in range(2000):
        branch = random.randint(0, 1)
        funct3 = random.choice(funct3_codes)
        rs1 = random.randint(0, MASK)
        if random.random() < 0.5:
            rs2 = rs1
        else:
            rs2 = random.randint(0, MASK)

        dut.branch.value = branch
        dut.funct3.value = funct3
        dut.rs1_data.value = rs1
        dut.rs2_data.value = rs2

        await Timer(1, "ns")
        actual = int(dut.branch_taken.value)
        expected = branch_reference(branch, funct3, rs1, rs2)
        scoreboard.check(expected, actual, f"branch= {branch} funct3= {funct3:03b} rs1= {rs1:#010x} rs2= {rs2:#010x}")
    dut._log.info(f"{scoreboard.checks} checks, {scoreboard.errors} errors")

