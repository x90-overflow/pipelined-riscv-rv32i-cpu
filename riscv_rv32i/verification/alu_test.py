import cocotb
from cocotb.triggers import Timer
from test_utils import MASK, to_signed, Scoreboard
import random

ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, SLT, SLTU = range(10)

def alu_reference(a, b, opsel):
    a &= MASK
    b &= MASK
    shift_count = b & 0x1F

    if opsel == ADD:
        return (a + b) & MASK
    elif opsel == SUB:
        return (a - b) & MASK
    elif opsel == AND:
        return a & b
    elif opsel == OR:
        return a | b
    elif opsel == XOR:
        return a ^ b
    elif opsel == SLL:
        return (a << shift_count) & MASK
    elif opsel == SRL:
        return a >> shift_count
    elif opsel == SRA:
        return (to_signed(a) >> shift_count) & MASK
    elif opsel == SLT:
        if to_signed(a) < to_signed(b):
            return 1
        return 0
    elif opsel == SLTU:
        if a < b:
            return 1
        return 0
    else:
        return 0


        
@cocotb.test()
async def test_alu(dut):
    scoreboard = Scoreboard("ALU Testing")
    for _ in range(1000):
        a = random.randint(0, MASK) # constrained-random check
        b = random.randint(0, MASK)
        op = random.randint(0, 9)

        dut.a.value = a  #drivers
        dut.b.value = b
        dut.op_sel.value = op

        await Timer(1, "ns")

        expected = alu_reference(a, b, op)
        actual = int(dut.alu_result.value) #monitor
        scoreboard.check(expected, actual, f"a={a:#010x} b={b:#010x} op={op}") #scoreboard
    dut._log.info(f"{scoreboard.checks} checks, {scoreboard.errors} errors")

@cocotb.test()
async def test_alu_edges(dut):
    scoreboard = Scoreboard("ALU Edge Case")
    edge_cases = [0, 1, 0xFFFFFFFF, 0x80000000, 0x7FFFFFFF]
    for a in edge_cases:
        for b in edge_cases:
            for op in range(10):
                dut.a.value = a
                dut.b.value = b
                dut.op_sel.value = op
                await Timer(1, "ns")
                expected = alu_reference(a, b, op)
                actual = int(dut.alu_result.value)
                scoreboard.check(expected, actual, f"a={a:#010x} b={b:#010x} op={op}")
    dut._log.info(f"{scoreboard.checks} edge case checks, {scoreboard.errors} errors")            

