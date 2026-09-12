module fpga_top(
    input wire clock,
    input wire rst_inv,
    output wire[5:0] led,
    output wire uart_tx_serial
);
    localparam LED_MAP_ADDRESS = 32'h10000000;
    localparam UART_MAP_ADDRESS = 32'h10000004;

    reg[22:0] clock_div;
    always @(posedge clock) begin
        clock_div <= clock_div + 1'b1;
    end
    wire clock_en = (clock_div == 23'd0);

    wire[31:0] mem_addr, mem_wr_data;
    wire mem_we;

    pipelined_cpu_forwarding #(.CLOCK_ENABLE(1)) u_cpu(
        .clock(clock),
        .rst_inv(rst_inv),
        .clock_en(clock_en),
        .mem_addr(mem_addr),
        .mem_wr_data(mem_wr_data),
        .mem_we(mem_we)
    );

    wire uart_start = clock_en && mem_we && (mem_addr == UART_MAP_ADDRESS);

    uart_tx u_tx(
        .clk(clock),
        .rst_n(rst_inv),
        .start(uart_start),
        .data(mem_wr_data[7:0]),
        .tx(uart_tx_serial),
        .busy()
    );

    reg[5:0] led_register;
    always @(posedge clock or negedge rst_inv) begin
        if(!rst_inv) begin
            led_register <= 6'b000000;
        end else if(clock_en && mem_we && (mem_addr == LED_MAP_ADDRESS)) begin
            led_register <= mem_wr_data[5:0];
        end
    end
    assign led = ~led_register;
endmodule