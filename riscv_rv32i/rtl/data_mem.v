module data_mem(
    input wire clock,
    input wire write_enable,
    input wire[31:0] address,
    input wire[31:0] write_data,
    output wire[31:0] read_data
);
    reg[31:0] mem [0:255];
    assign read_data = mem[address[31:2]];
    
    always @(posedge clock) begin
        if(write_enable) begin
            mem[address[31:2]] <= write_data;
        end
    end
endmodule
