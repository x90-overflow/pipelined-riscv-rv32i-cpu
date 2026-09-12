`timescale 1ns/1ps

module uart_tx #( 
    parameter CLK_FREQ = 27_000_000,
    parameter BAUD_RATE = 115200
)( 
    input wire clk,
    input wire rst_n,
    input wire start,
    input wire[7:0] data,
    output reg tx,
    output reg busy
);
    localparam CYCLE_PERBIT = CLK_FREQ/BAUD_RATE;
    
    localparam IDLE = 2'd0, START = 2'd1, DATA = 2'd2, STOP = 2'd3;
    reg[1:0] state = IDLE;
    reg[15:0] clk_count = 0;
    reg[2:0] bit_index = 0;
    reg[7:0] data_latch = 0;

    always @(posedge clk) begin
        if(!rst_n) begin
            state <= IDLE;
            tx <= 1'b1;
            busy <= 1'b0;
            clk_count <= 0;
            bit_index <= 0;
        end else begin
            case(state) 
                IDLE: begin
                    tx <= 1'b1;
                    busy <= 1'b0;
                    clk_count <= 0;
                    bit_index <= 0;
                    if(start) begin
                        data_latch <= data;
                        busy <= 1'b1;
                        state <= START;
                    end
                end
                START: begin
                    tx <= 1'b0;
                    if(clk_count < CYCLE_PERBIT - 1) begin
                        clk_count <= clk_count + 1;
                    end else begin
                        clk_count <= 0;
                        state <= DATA;
                    end
                end
                DATA: begin
                    tx <= data_latch[bit_index];
                    if(clk_count < CYCLE_PERBIT - 1) begin
                        clk_count <= clk_count + 1;
                    end else begin
                        clk_count <= 0;
                        if(bit_index < 7) begin
                            bit_index <= bit_index + 1;
                        end else begin
                            bit_index <= 0;
                            state <= STOP;
                        end
                    end
                end
                STOP: begin
                    tx <= 1'b1;
                    if(clk_count < CYCLE_PERBIT - 1) begin
                        clk_count <= clk_count + 1;
                    end else begin
                        clk_count <= 0;
                        state <= IDLE;
                    end
                end
                default: state <= IDLE;
            endcase
        end
    end
endmodule

