module pipelined_cpu_stall(
    input wire clock,
    input wire rst_inv,
    output wire[31:0] mem_addr,
    output wire[31:0] mem_wr_data,
    output wire mem_we
);
    wire[31:0] pc, pc_4, pc_next, instr;
    wire redirect;
    wire[31:0] redirect_loc;
    wire stall;
    assign pc_4 = pc + 32'b100;
    assign pc_next = redirect ? redirect_loc : (stall ? pc : pc_4);

    program_counter u_pc(
        .clock(clock),
        .rst_inv(rst_inv),
        .pc_next(pc_next),
        .pc(pc)
    );

    instruction_mem u_insmem(
        .addr(pc),
        .instr(instr)
    );

    reg[31:0] fet_dec_instr;
    reg[31:0] fet_dec_pc;
    reg[31:0] fet_dec_pc_4;

    always @(posedge clock or negedge rst_inv) begin
        if(!rst_inv) begin
            fet_dec_instr <= 32'h0;
            fet_dec_pc <= 32'h0;
            fet_dec_pc_4 <= 32'h0;
        end else if(redirect) begin
            fet_dec_instr <= 32'h0;
            fet_dec_pc <= 32'h0;
            fet_dec_pc_4 <= 32'h0;
        end else if(stall) begin
            fet_dec_instr <= fet_dec_instr;
            fet_dec_pc <= fet_dec_pc;
            fet_dec_pc_4 <= fet_dec_pc_4;
        end else begin
            fet_dec_instr <= instr;
            fet_dec_pc <= pc;
            fet_dec_pc_4 <= pc_4;
        end
    end

    wire[6:0] opcode, funct7;
    wire[2:0] funct3;
    wire[4:0] rs1, rs2, rd;
    wire[31:0] imm;
    wire[31:0] rs1_data, rs2_data;

    wire reg_write, mem_read, mem_write, branch, jump, alu_in_a, alu_in_b;
    wire[1:0] result_sel;
    wire[3:0] op_sel;
    
    wire wrb_reg_write;
    wire[4:0] wrb_rd_addr;
    wire[31:0] wrb_rd_data;

    decoder u_decoder(
        .instr(fet_dec_instr),
        .opcode(opcode),
        .rd(rd),
        .funct3(funct3),
        .rs1(rs1),
        .rs2(rs2),
        .funct7(funct7)
    );

    immediate_gen u_immgen(
        .instr(fet_dec_instr),
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
        .write_enable(wrb_reg_write),
        .rd_addr(wrb_rd_addr),
        .rd_data(wrb_rd_data)
    );

    reg[31:0] dec_exe_pc, dec_exe_pc_4;
    reg[31:0] dec_exe_rs1_data, dec_exe_rs2_data, dec_exe_imm;
    reg[4:0] dec_exe_rs1_addr, dec_exe_rs2_addr, dec_exe_rd_addr;
    reg[2:0] dec_exe_funct3;
    reg[6:0] dec_exe_opcode;
    reg dec_exe_reg_write, dec_exe_mem_read, dec_exe_mem_write;
    reg dec_exe_branch, dec_exe_jump, dec_exe_alu_in_a, dec_exe_alu_in_b;
    reg[1:0] dec_exe_result_sel;
    reg[3:0] dec_exe_op_sel;

    always @(posedge clock or negedge rst_inv) begin
        if(!rst_inv) begin
            dec_exe_pc <= 32'h0;  dec_exe_pc_4 <= 32'h0;
            dec_exe_rs1_data <= 32'h0; dec_exe_rs2_data <= 32'h0; dec_exe_imm <= 32'h0;
            dec_exe_rs1_addr <= 5'h0; dec_exe_rs2_addr <= 5'h0; dec_exe_rd_addr <= 5'h0;
            dec_exe_funct3 <= 3'h0; dec_exe_opcode <= 7'h0;
            dec_exe_reg_write <= 1'b0; dec_exe_mem_read <= 1'b0; dec_exe_mem_write <= 1'b0;
            dec_exe_branch <= 1'b0; dec_exe_jump <= 1'b0; 
            dec_exe_alu_in_a <= 1'b0; dec_exe_alu_in_b <= 1'b0;
            dec_exe_result_sel <= 2'h0; dec_exe_op_sel <= 4'h0;
        end else if(redirect || stall) begin
            dec_exe_pc <= 32'h0;  dec_exe_pc_4 <= 32'h0;
            dec_exe_rs1_data <= 32'h0; dec_exe_rs2_data <= 32'h0; dec_exe_imm <= 32'h0;
            dec_exe_rs1_addr <= 5'h0; dec_exe_rs2_addr <= 5'h0; dec_exe_rd_addr <= 5'h0;
            dec_exe_funct3 <= 3'h0; dec_exe_opcode <= 7'h0;
            dec_exe_reg_write <= 1'b0; dec_exe_mem_read <= 1'b0; dec_exe_mem_write <= 1'b0;
            dec_exe_branch <= 1'b0; dec_exe_jump <= 1'b0; 
            dec_exe_alu_in_a <= 1'b0; dec_exe_alu_in_b <= 1'b0;
            dec_exe_result_sel <= 2'h0; dec_exe_op_sel <= 4'h0;
        end else begin
            dec_exe_pc <= fet_dec_pc; 
            dec_exe_pc_4 <= fet_dec_pc_4;
            dec_exe_rs1_data <= rs1_data; 
            dec_exe_rs2_data <= rs2_data;
            dec_exe_imm <= imm;
            dec_exe_rs1_addr <= rs1;
            dec_exe_rs2_addr <= rs2;
            dec_exe_rd_addr <= rd;
            dec_exe_funct3 <= funct3;
            dec_exe_opcode <= opcode;
            dec_exe_reg_write <= reg_write;
            dec_exe_mem_read <= mem_read;
            dec_exe_mem_write <= mem_write;
            dec_exe_branch <= branch;
            dec_exe_jump <= jump;
            dec_exe_alu_in_a <= alu_in_a;
            dec_exe_alu_in_b <= alu_in_b;
            dec_exe_result_sel <= result_sel;
            dec_exe_op_sel <= op_sel;
        end
    end

    wire[31:0] alu_a = dec_exe_alu_in_a ? dec_exe_pc : dec_exe_rs1_data;
    wire[31:0] alu_b = dec_exe_alu_in_b ? dec_exe_imm : dec_exe_rs2_data;

    wire[31:0] alu_result;
    wire zero;
    wire branch_taken;

    alu u_alu(
        .a(alu_a),
        .b(alu_b),
        .op_sel(dec_exe_op_sel),
        .alu_result(alu_result),
        .zero(zero)
    );

    branch_decode u_branchdec(
        .branch(dec_exe_branch),
        .funct3(dec_exe_funct3),
        .rs1_data(dec_exe_rs1_data),
        .rs2_data(dec_exe_rs2_data),
        .branch_taken(branch_taken)
    );

    localparam OP_JALR = 7'b1100111;
    assign redirect = branch_taken | dec_exe_jump;
    assign redirect_loc = (dec_exe_opcode == OP_JALR) ? (alu_result & ~32'b1) : (dec_exe_pc + dec_exe_imm);

    reg[31:0] exe_mem_alu_result, exe_mem_rs2_data, exe_mem_pc_4, exe_mem_imm;
    reg[4:0] exe_mem_rd_addr;
    reg exe_mem_reg_write, exe_mem_mem_read, exe_mem_mem_write;
    reg[1:0] exe_mem_result_sel;

    always @(posedge clock or negedge rst_inv) begin
        if(!rst_inv) begin
            exe_mem_alu_result <= 32'h0; exe_mem_rs2_data <= 32'h0; 
            exe_mem_pc_4 <= 32'h0; exe_mem_imm <= 32'h0; exe_mem_rd_addr <= 5'h0;
            exe_mem_reg_write <= 1'b0; exe_mem_mem_read <= 1'b0; exe_mem_mem_write <= 1'b0;
            exe_mem_result_sel <= 2'h0;
        end else begin
            exe_mem_alu_result <= alu_result;
            exe_mem_rs2_data <= dec_exe_rs2_data;
            exe_mem_pc_4 <= dec_exe_pc_4;
            exe_mem_imm <= dec_exe_imm;
            exe_mem_rd_addr <= dec_exe_rd_addr;
            exe_mem_reg_write <= dec_exe_reg_write;
            exe_mem_mem_read <= dec_exe_mem_read;
            exe_mem_mem_write <= dec_exe_mem_write;
            exe_mem_result_sel <= dec_exe_result_sel;
        end
    end

    wire[31:0] mem_read_out;

    data_mem u_datamem(
        .clock(clock),
        .write_enable(exe_mem_mem_write),
        .address(exe_mem_alu_result),
        .write_data(exe_mem_rs2_data),
        .read_data(mem_read_out)
    );

    reg[31:0] mem_wrb_mem_read_out, mem_wrb_alu_result, mem_wrb_pc_4, mem_wrb_imm;
    reg[4:0] mem_wrb_rd_addr;
    reg mem_wrb_reg_write;
    reg[1:0] mem_wrb_result_sel;

    always @(posedge clock or negedge rst_inv) begin
        if(!rst_inv) begin
            mem_wrb_mem_read_out <= 32'h0; mem_wrb_alu_result <= 32'h0; 
            mem_wrb_pc_4 <= 32'h0; mem_wrb_imm <= 32'h0; mem_wrb_rd_addr <= 5'h0;
            mem_wrb_reg_write <= 1'b0; mem_wrb_result_sel <= 2'h0;
        end else begin
            mem_wrb_mem_read_out <= mem_read_out;
            mem_wrb_alu_result <= exe_mem_alu_result;
            mem_wrb_pc_4 <= exe_mem_pc_4;
            mem_wrb_imm <= exe_mem_imm;
            mem_wrb_rd_addr <= exe_mem_rd_addr;
            mem_wrb_reg_write <= exe_mem_reg_write;
            mem_wrb_result_sel <= exe_mem_result_sel;
        end
    end

    assign mem_addr = exe_mem_alu_result;
    assign mem_wr_data = exe_mem_rs2_data;
    assign mem_we = exe_mem_mem_write;

    wire hazard_exe = dec_exe_reg_write && (dec_exe_rd_addr != 5'h0) && 
        ((dec_exe_rd_addr == rs1) || (dec_exe_rd_addr == rs2));
    wire hazard_mem = exe_mem_reg_write && (exe_mem_rd_addr != 5'h0) &&
        ((exe_mem_rd_addr == rs1) || (exe_mem_rd_addr == rs2));
    wire hazard_wrb = mem_wrb_reg_write && (mem_wrb_rd_addr != 5'h0) &&
        ((mem_wrb_rd_addr == rs1) || (mem_wrb_rd_addr == rs2));

    assign stall = hazard_exe || hazard_mem || hazard_wrb;


    assign wrb_reg_write = mem_wrb_reg_write;
    assign wrb_rd_addr = mem_wrb_rd_addr;
    assign wrb_rd_data = 
        (mem_wrb_result_sel == 2'b00) ? mem_wrb_alu_result :
        (mem_wrb_result_sel == 2'b01) ? mem_wrb_mem_read_out :
        (mem_wrb_result_sel == 2'b10) ? mem_wrb_pc_4 :
        mem_wrb_imm;

endmodule