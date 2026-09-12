SIM ?= icarus
TOPLEVEL_LANG ?= verilog
CPU_COMPONENTS ?= $(PWD)/../rtl/program_counter.v $(PWD)/../rtl/instruction_mem.v \
	$(PWD)/../rtl/decoder.v $(PWD)/../rtl/immediate_gen.v $(PWD)/../rtl/control.v \
	$(PWD)/../rtl/alu_control.v $(PWD)/../rtl/regfile.v $(PWD)/../rtl/alu.v \
	$(PWD)/../rtl/branch_decode.v $(PWD)/../rtl/data_mem.v

MODULE_NAME ?= pipelined_cpu_forwarding

ifeq ($(MODULE_NAME), singlecycle_cpu)
VERILOG_SOURCES ?= $(PWD)/../rtl/singlecycle_cpu.v $(CPU_COMPONENTS)
COCOTB_TOPLEVEL ?= singlecycle_cpu
COCOTB_TEST_MODULES ?= cpu_top_test
else ifeq ($(MODULE_NAME), pipelined_cpu_stall)
VERILOG_SOURCES ?= $(PWD)/../rtl/pipelined_cpu_stall.v $(CPU_COMPONENTS)
COCOTB_TOPLEVEL ?= pipelined_cpu_stall
COCOTB_TEST_MODULES ?= cpu_top_test
else ifeq ($(MODULE_NAME), pipelined_cpu_forwarding)
VERILOG_SOURCES ?= $(PWD)/../rtl/pipelined_cpu_forwarding.v $(CPU_COMPONENTS)
COCOTB_TOPLEVEL ?= pipelined_cpu_forwarding
COCOTB_TEST_MODULES ?= cpu_top_test
else
VERILOG_SOURCES += $(PWD)/../rtl/$(MODULE_NAME).v
COCOTB_TOPLEVEL = $(MODULE_NAME)
COCOTB_TEST_MODULES = $(MODULE_NAME)_test
endif

include $(shell cocotb-config --makefiles)/Makefile.sim 

