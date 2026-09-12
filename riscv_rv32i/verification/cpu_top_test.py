import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from test_utils import Scoreboard
from riscv_assembler import *
from riscv_model import instr_exe

MEM_WORDS = 256
DRAIN = 8

def nop():
    return addi(0, 0, 0)

async def load_run(dut, words):
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

    for _ in range(len(words) * 5 + DRAIN):
        await RisingEdge(dut.clock)

def check_state(dut, words, name):
    expected_reg, expected_mem = instr_exe(words, MEM_WORDS)
    scoreboard = Scoreboard(name)
    for i in range(1, 32):
        scoreboard.check(expected_reg[i], int(dut.u_regfile.registers[i].value), f"x{i}")
    for i in range(MEM_WORDS):
        scoreboard.check(expected_mem[i], int(dut.u_datamem.mem[i].value), f"mem[{i}]")
    dut._log.info(f"{name} {scoreboard.checks} checks, {scoreboard.errors} errors")

@cocotb.test()
async def test_smoke(dut):
    program = [addi(1, 0, 5), addi(2, 0, 7), nop(), nop(), nop(), add(3, 1, 2)]
    await load_run(dut, program)
    check_state(dut, program, "Smoke Test: ADD/ADDI")

@cocotb.test()
async def test_directed_nb(dut):
    program = [lui(1, 0x23675), addi(2, 0, 0x123), nop(), nop(), nop(),
        add(3, 1, 2), beq(1, 2, 8), sw(2, 0, 16), nop(), nop(), nop(),
        lw(5, 0, 16), auipc(4, 0)]
    await load_run(dut, program)

    assert int(dut.u_regfile.registers[1].value) == 0x23675000
    assert int(dut.u_regfile.registers[2].value) == 0x123
    assert int(dut.u_regfile.registers[3].value) == 0x23675123
    assert int(dut.u_datamem.mem[4].value) == 0x123
    assert int(dut.u_regfile.registers[5].value) == 0x123
    assert int(dut.u_regfile.registers[4].value) == 48

    check_state(dut, program, "Directed Test: ADD/ADDI/BEQ(not taken)/LUI/AUIPC/LW/SW")

@cocotb.test()
async def test_jumps(dut):
    program = [jal(1, 12), addi(2, 0, 5), addi(3, 2, 7), addi(4, 0, 2)]
    await load_run(dut, program)

    assert int(dut.u_regfile.registers[1].value) == 4
    assert int(dut.u_regfile.registers[2].value) == 0
    assert int(dut.u_regfile.registers[3].value) == 0
    assert int(dut.u_regfile.registers[4].value) == 2

    check_state(dut, program, "Jump Test")

@cocotb.test()
async def test_data_hazards(dut):
    program = [addi(1, 0, 5), add(2, 1, 1), sub(3, 2, 1), addi(4, 3, 1)]
    await load_run(dut, program)
    assert int(dut.u_regfile.registers[1].value) == 5
    assert int(dut.u_regfile.registers[2].value) == 10
    assert int(dut.u_regfile.registers[3].value) == 5
    assert int(dut.u_regfile.registers[4].value) == 6

    check_state(dut, program, "RAW Hazard: Stalling Test")

@cocotb.test()
async def test_load(dut):
    program = [addi(1, 0, 15), sw(1, 0, 0), lw(2, 0, 0), add(3, 2, 2)]
    await load_run(dut, program)
    assert int(dut.u_regfile.registers[1].value) == 15
    assert int(dut.u_datamem.mem[0].value) == 15
    assert int(dut.u_regfile.registers[2].value) == 15
    assert int(dut.u_regfile.registers[3].value) == 30
    check_state(dut, program, "Load Stall Test")
