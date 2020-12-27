`timescale 1ns / 1ps
/**
* Module phase_acc
*
* Phase accumulator
*
**/

module phase_acc #(
    parameter ACC_SIZE = 28
) (
    input wire                clk,
    input wire                rst,
    input wire [ACC_SIZE-1:0] freq_word,

    output reg [ACC_SIZE-1:0] phase

);

`ifdef COCOTB_SIM
  initial begin
    $dumpfile("phase_acc.vcd");
    $dumpvars(0, phase_acc);
    #2;
  end
`endif

  reg [ACC_SIZE-1:0] phase_acc;
  assign phase = phase_acc;

  always_ff @(posedge clk) begin
    if (rst) begin
      phase_acc <= 0;
    end else begin
      phase_acc <= phase_acc + freq_word;
    end
  end

endmodule
