SOURCES = fpga_top.v ../rtl/pipelined_cpu_forwarding.v ../rtl/program_counter.v ../rtl/instruction_mem.v \
	../rtl/decoder.v ../rtl/immediate_gen.v ../rtl/control.v ../rtl/alu_control.v ../rtl/regfile.v \
	../rtl/alu.v ../rtl/branch_decode.v ../rtl/data_mem.v ../rtl/uart_tx.v

DEVICE = GW1NR-LV9QN88PC6/I5
FAMILY = GW1N-9C

all: out.fs
out.json: $(SOURCES)
	yosys -p "read_verilog $(SOURCES); synth_gowin -top fpga_top -json out.json"
pnr.json: out.json tangnano9k.cst
	nextpnr-himbaechel --json out.json --write pnr.json \
		--device "$(DEVICE)" --vopt family=$(FAMILY) --vopt cst=tangnano9k.cst
out.fs: pnr.json
	gowin_pack -d $(FAMILY) -o out.fs pnr.json
flash: out.fs
	openFPGALoader -b tangnano9k out.fs
clean:
	rm -f out.json pnr.json out.fs
