module alu_control(
    input wire[6:0] opcode,
    input wire[2:0] funct3,
    input wire funct7_5,
    output reg[3:0] op_sel
);
    localparam OP_REGTYPE = 7'b0110011;
    localparam OP_IMMTYPE = 7'b0010011;
    localparam ALU_ADD = 4'b0000, ALU_SUB = 4'b0001, ALU_AND = 4'b0010, ALU_OR = 4'b0011,
        ALU_XOR = 4'b0100, ALU_SLL = 4'b0101, ALU_SRL = 4'b0110, ALU_SRA = 4'b0111, 
        ALU_SLT = 4'b1000, ALU_SLTU = 4'b1001;

    always @(*) begin
        case(opcode)
            OP_REGTYPE, OP_IMMTYPE: begin
                case(funct3)
                    3'b000: op_sel = (opcode == OP_REGTYPE && funct7_5) ? ALU_SUB : ALU_ADD;
                    3'b001: op_sel = ALU_SLL;
                    3'b010: op_sel = ALU_SLT;
                    3'b011: op_sel = ALU_SLTU;
                    3'b100: op_sel = ALU_XOR;
                    3'b101: op_sel = funct7_5 ? ALU_SRA : ALU_SRL;
                    3'b110: op_sel = ALU_OR;
                    3'b111: op_sel = ALU_AND;
                    default: op_sel = ALU_ADD;
                endcase
            end
            default: op_sel = ALU_ADD;
        endcase
    end
endmodule
