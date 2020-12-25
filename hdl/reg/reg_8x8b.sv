`timescale 1ns / 1ps
/**
* Module reg_8x8b
*
* 8 x 8b regfile
*
**/

module reg_8x8b (
    input wire       clk,
    input wire       rst,
    input wire       i_en_wr,
    input wire [3:0] i_addr_rd,
    input wire [3:0] i_addr_wr,
    input wire [7:0] i_data,

    output reg [7:0] o_data
);

`ifdef COCOTB_SIM
  initial begin
    $dumpfile("reg_8x8b.vcd");
    $dumpvars(0, reg_8x8b);
    #1;
  end
`endif

  // Our actual 8x8b regfile
  reg [7:0] regfile[7:0];
  integer idx;  // loop counter


  // pass the read output, always
  assign o_data = regfile[i_addr_rd];

  always_ff @(posedge clk) begin
    if (rst) begin
      for (idx = 0; idx < 8; idx = idx + 1) begin
        regfile[idx] <= 0;
      end
    end else begin
      if (i_en_wr) begin
        regfile[i_addr_wr] = i_data;
      end
    end
  end

endmodule
