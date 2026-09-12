module program_counter(
    input wire clock,
    input wire rst_inv,
    input wire[31:0] pc_next,
    output reg[31:0] pc
);
    always @(posedge clock or negedge rst_inv) begin
        if(!rst_inv) begin
            pc <= 32'h0;
        end else begin
            pc <= pc_next;
        end
    end
endmodule
