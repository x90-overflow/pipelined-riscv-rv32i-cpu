# Pipelined RV32I RISC-V CPU

32-bit RISC-V processor designed from scratch and written in Verilog. 
5-stage pipeline with hazard detection via forwarding. 
Verification modules in cocotb (python) following UVM principles.
TangNano9k FPGA implementation via a LED counter and UART peripheral showing working on real silicon.

## 3 Cores:
singlecycle_cpu: The first single-cycle core
pipelined_cpu_stall: 5-stage pipelined version that uses stalls for hazard handling (RAW hazard)
pipelined_cpu_forwarding: 5-stage pipelined final version that uses forwarding for hazard handling only leaving load use stalls

## Available Instruction Set:
ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, SLT, SLTU, ADDI, ANDI, ORI, XORI, SLTI, LW, SW, BEQ, BNE, BLT, BGE, BLTU, BGEU, JAL, JALR, LUI, AUIPC

