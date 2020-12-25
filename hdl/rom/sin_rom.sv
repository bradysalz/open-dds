`timescale 1ns / 1ps
/**
* Module sine_rom
*
* Sine wave LUT (14b)
*
**/

module sin_rom (
    input  wire [13:0] addr,
    output reg  [13:0] sine
);

`ifdef COCOTB_SIM
  initial begin
    $dumpfile("sin_rom.vcd");
    $dumpvars(0, sin_rom);
    #1;
  end
`endif

  reg [13:0] rom[16383:0];
  integer i;

  initial begin
    $readmemb("/home/brady/devel/open-dds/hdl/rom/sin_rom.dat", rom, 0, 16383);
  end

  assign sine = rom[addr];

endmodule
