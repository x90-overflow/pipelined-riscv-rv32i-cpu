module singlecycle_cpu(
    input wire clock,
    input wire rst_inv,
    output wire[31:0] mem_addr,
    output wire[31:0] mem_wr_data,
    output wire mem_we
);
    wire[31:0] pc, pc_next, pc_4;
    wire[31:0] instr;
    wire[6:0] opcode, funct7;
    wire[2:0] funct3;
    wire[4:0] rs1, rs2, rd;
    wire[31:0] imm;

    wire reg_write, mem_read, mem_write, branch, jump, alu_in_a, alu_in_b;
    wire[1:0] result_sel;
    wire[3:0] op_sel;

    wire[31:0] rs1_data, rs2_data;
    wire[31:0] rd_data;
    wire[31:0] alu_result;
    wire[31:0] mem_read_out;
    wire zero, branch_taken;
   
    program_counter u_pc(
        .clock(clock),
        .rst_inv(rst_inv),
        .pc_next(pc_next),
        .pc(pc)
    );
    assign pc_4 = pc + 32'b100;

    instruction_mem u_insmem(
        .addr(pc),
        .instr(instr)
    );

    decoder u_decoder(
        .instr(instr),
        .opcode(opcode),
        .rd(rd),
        .funct3(funct3),
        .rs1(rs1),
        .rs2(rs2),
        .funct7(funct7)
    );

    immediate_gen u_immgen(
        .instr(instr),
        .imm(imm)
    );

    control u_control(
        .opcode(opcode),
        .reg_write(reg_write),
        .mem_read(mem_read),
        .mem_write(mem_write),
        .branch(branch),
        .jump(jump),
        .alu_in_a(alu_in_a),
        .alu_in_b(alu_in_b),
        .result_sel(result_sel)
    );

    alu_control u_aluctrl(
        .opcode(opcode),
        .funct3(funct3),
        .funct7_5(funct7[5]),
        .op_sel(op_sel) 
    );

    regfile u_regfile(
        .clock(clock),
        .rs1_addr(rs1),
        .rs2_addr(rs2),
        .rs1_data(rs1_data),
        .rs2_data(rs2_data),
        .write_enable(reg_write),
        .rd_addr(rd),
        .rd_data(rd_data)
    );

    wire[31:0] alu_a = alu_in_a ? pc : rs1_data;
    wire[31:0] alu_b = alu_in_b ? imm : rs2_data;

    alu u_alu(
        .a(alu_a),
        .b(alu_b),
        .op_sel(op_sel),
        .alu_result(alu_result),
        .zero(zero)
    );

    branch_decode u_branchdec(
        .branch(branch),
        .funct3(funct3),
        .rs1_data(rs1_data),
        .rs2_data(rs2_data),
        .branch_taken(branch_taken)
    );

    data_mem u_datamem(
        .clock(clock),
        .write_enable(mem_write),
        .address(alu_result),
        .write_data(rs2_data),
        .read_data(mem_read_out)
    );

    assign mem_addr = alu_result;
    assign mem_wr_data = rs2_data;
    assign mem_we = mem_write;

    assign rd_data = (result_sel == 2'b00) ? alu_result : (result_sel == 2'b01) ? mem_read_out : 
        (result_sel == 2'b10) ? pc_4 : imm;

    localparam OP_JAL = 7'b1101111, OP_JALR = 7'b1100111;

    wire[31:0] pc_imm = pc + imm;
    wire[31:0] jalr_addr = alu_result & ~32'b1;

    assign pc_next = branch_taken ? pc_imm : (opcode == OP_JAL) ? pc_imm : 
        (opcode == OP_JALR) ? jalr_addr : pc_4;

endmodule    

