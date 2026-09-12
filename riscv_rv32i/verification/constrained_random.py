import cocotb 
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
import random
from riscv_assembler import *
from cpu_top_test import load_run, check_state, MEM_WORDS, DRAIN

COVERAGE = {"fwd_a": set(), "fwd_b": set(), "stall": set(), "redirect": set()}

async def load_run_coverage(dut, words):
    dut.clock.value = 0
    dut.rst_inv.value = 0
    await Timer(1, "ns")
    for i in range(32):
        dut.u_regfile.registers[i].value = 0
    for i in range(MEM_WORDS):
        dut.u_insmem.mem[i].value = 0
        dut.u_datamem.mem[i].value = 0
    for i, w in enumerate(words):
        dut.u_insmem.mem[i].value = w
    await Timer(1, "ns")
    cocotb.start_soon(Clock(dut.clock, 10, "ns").start())
    dut.rst_inv.value = 1

    for _ in range(len(words)*5 + DRAIN):
        await RisingEdge(dut.clock)
        await Timer(1, "ns")
        COVERAGE["fwd_a"].add(int(dut.forward_a.value))
        COVERAGE["fwd_b"].add(int(dut.forward_b.value))
        COVERAGE["stall"].add(int(dut.stall.value))
        COVERAGE["redirect"].add(int(dut.redirect.value))



R_OPS = [add, sub, and_, or_, xor_, sll, srl, sra, slt, sltu]
I_OPS = [addi, andi, ori, xori, slti]

def random_program(rand_num, n):
    program = []
    for _ in range(n):
        rd = rand_num.randint(1, 31)
        pick = rand_num.random()
        if pick < 0.45:
            op = rand_num.choice(R_OPS)
            program.append(op(rd, rand_num.randint(0, 31), rand_num.randint(0, 31)))
        elif pick < 0.75:
            op = rand_num.choice(I_OPS)
            program.append(op(rd, rand_num.randint(0, 31), rand_num.randint(-2048, 2047)))
        elif pick < 0.85:
            op = rand_num.choice([lui, auipc])
            program.append(op(rd, rand_num.randint(0, 0xFFFFF)))
        elif pick < 0.93:
            off = 4 * rand_num.randint(0, MEM_WORDS-1)
            program.append(sw(rand_num.randint(0, 31), 0, off))
        else:
            off = 4 * rand_num.randint(0, MEM_WORDS-1)
            program.append(lw(rd, 0, off))
            if rand_num.random() < 0.5:
                program.append(rand_num.choice(R_OPS)(rand_num.randint(1, 31), rd, rand_num.randint(0, 31)))
    return program

async def run_random(dut, seed, n):
    rand_num = random.Random(seed)
    program = random_program(rand_num, n)
    await load_run_coverage(dut, program)
    check_state(dut, program, f"Constrained Random Test with seed: {seed} test count: {n}")

@cocotb.test()
async def test_random_1(dut): await run_random(dut, 1, 60)
@cocotb.test()
async def test_random_2(dut): await run_random(dut, 2, 120)
@cocotb.test()
async def test_random_3(dut): await run_random(dut, 3, 200)
@cocotb.test()
async def test_coverage_report(dut):
    dut._log.info(f"Forward a bins: {sorted(COVERAGE['fwd_a'])}")
    dut._log.info(f"Forward b bins: {sorted(COVERAGE['fwd_b'])}")
    dut._log.info(f"Stall occurrence: {sorted(COVERAGE['stall'])}")
    dut._log.info(f"Redirect occurrence: {sorted(COVERAGE['redirect'])}")

    assert COVERAGE["fwd_a"] == {0, 1, 2}, f"Forward a hole: {COVERAGE['fwd_a']}"
    assert COVERAGE["fwd_b"] == {0, 1, 2}, f"Forward b hole: {COVERAGE['fwd_b']}"
