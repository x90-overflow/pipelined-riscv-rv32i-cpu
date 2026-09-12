import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from riscv_assembler import *
from cpu_top_test import MEM_WORDS, DRAIN, check_state

async def load_run_count_stall(dut, words):
    dut.clock.value = 0
    dut.rst_inv.value = 0
    await Timer(1, "ns")
    for i in range(32):
        dut.u_regfile.registers[i].value = 0
    for i in range(MEM_WORDS):
        dut.u_datamem.mem[i].value = 0
        dut.u_insmem.mem[i].value = 0
    for i, w in enumerate(words):
        dut.u_insmem.mem[i].value = w
    await Timer(1, "ns")
    cocotb.start_soon(Clock(dut.clock, 10, "ns").start())
    dut.rst_inv.value = 1

    stall_count = 0
    for _ in range(len(words) * 5 + DRAIN):
        await RisingEdge(dut.clock)
        await Timer(1, "ns")
        stall_count += int(dut.stall.value)
    return stall_count

@cocotb.test()
async def test_stall_count(dut):
    alu_ops = [addi(1, 0, 2), add(2, 1, 1), sub(3, 2, 1), addi(4, 3, 1)]
    n = await load_run_count_stall(dut, alu_ops)
    dut._log.info(f"ALU stall count: {n}")

    ld_ops = [addi(1, 0, 2), sw(1, 0, 0), lw(2, 0, 0), add(3, 2, 2)]
    n = await load_run_count_stall(dut, ld_ops)
    dut._log.info(f"Load program stall count: {n}")

    