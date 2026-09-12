module branch_decode(
    input wire branch,
    input wire[2:0] funct3,
    input wire[31:0] rs1_data,
    input wire[31:0] rs2_data,
    output wire branch_taken
);
    reg condition;
    always @(*) begin
        case(funct3)
            3'b000: condition = (rs1_data == rs2_data); 
            3'b001: condition = (rs1_data != rs2_data);
            3'b100: condition = ($signed(rs1_data) < $signed(rs2_data));
            3'b101: condition = ($signed(rs1_data) >= $signed(rs2_data));
            3'b110: condition = (rs1_data < rs2_data);
            3'b111: condition = (rs1_data >= rs2_data);
            default: condition = 1'b0;
        endcase
    end
    assign branch_taken = branch & condition;
endmodule
