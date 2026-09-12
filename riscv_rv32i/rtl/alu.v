module alu(
    input wire[31:0] a,
    input wire[31:0] b,
    input wire[3:0] op_sel,
    output reg[31:0] alu_result,
    output wire zero
);
    always @(*) begin
        case(op_sel)
            4'b0000: alu_result = a + b;
            4'b0001: alu_result = a - b;
            4'b0010: alu_result = a & b;
            4'b0011: alu_result = a | b;
            4'b0100: alu_result = a ^ b;
            4'b0101: alu_result = a << b[4:0]; 
            4'b0110: alu_result = a >> b[4:0]; 
            4'b0111: alu_result = $signed(a) >>> b[4:0];
            4'b1000: alu_result = ($signed(a) < $signed(b)) ? 32'b1 : 32'b0;
            4'b1001: alu_result = (a < b) ? 32'b1 : 32'b0;
            default: alu_result = 32'b0;
        endcase
    end
    assign zero = (alu_result == 32'b0);
endmodule