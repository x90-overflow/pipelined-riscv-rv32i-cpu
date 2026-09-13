# Pipelined RV32I RISC-V CPU

32-bit RISC-V processor designed from scratch and written in Verilog. 
5-stage pipeline with hazard detection via forwarding. 
Verification modules in cocotb (python) following UVM principles.
TangNano9k FPGA implementation via a LED counter and UART peripheral showing working on real silicon.

## Build & Run 
- Simulation (`verification/`) : `make clean && make MODULE_NAME=pipelined_cpu_forwarding`
  (swap MODULE_NAME with the core you want to use)
- FPGA LED Counter (`fpga/`) :
    -  `python3 ../instruction_generation/LED_instructions.hex`
    -  `make clean && make` 
    -  `make flash` 
- FPGA UART Peripheral:
    - `python3 ../instruction_generation/UART_instructions.hex`
    - `make clean && make`
    - `make flash`
    - Open serial terminal (screen) at 115200
  
## Cores and Architecture:
- `rtl/singlecycle_cpu`: Executes 1 instruction per cycle. 
- `pipelined_cpu_stall`: 5-stage pipeline separated by pipeline registers. Uses stalls to handle hazards. This is kept to quantify the performance improvement. 
- `pipelined_cpu_forwarding`: 5-stage pipelined final version that uses forwarding for hazard handling.
    - 5-stage pipeline: FETCH | DECODE | EXECUTE | MEMORY | WRITEBACK
### Hazard Handling
- Data Hazard (Read after Write): EXE/MEM -> EXE, MEM/WRB -> EXE, and the 3 ahead case all forwarded to EXE stage. In stalled core this causes a 3 cycle stall.
- Load Instruction: 1-cycle stall
- Control Hazard (Branching/Jumps): 2 invalid instructions flushed in EXE. 

## Available Instruction Set:
ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, SLT, SLTU, ADDI, ANDI, ORI, XORI, SLTI, LW, SW, BEQ, BNE, BLT, BGE, BLTU, BGEU, JAL, JALR, LUI, AUIPC

## Verification

## FPGA Specifications

## Toolchain

## Directory Layout
rtl/  : CPU cores, Datapath, Controlpath, Data and Instruction Memories
fpga/ : FPGA top module, Pin Constraints, Makefile, Instruction File
verification/ : cocotb Tests, cocotb Reference Models, RISC-V Mini Assembler, Simulation Makefile
instruction_generation/ : Hex Program Generators

Built by: Elif Ilgin Ozdemir (x90 overflow)
