`default_nettype none `timescale 1ns / 1ps
/**
* Module waveform_gen
*
* Generates the final output waveform
*
**/

module waveform_gen (
    input wire [27:0] phase,
    input wire [27:0] phase_offset,
    input wire [ 1:0] wave_style,

    output reg [13:0] outval

);

`ifdef COCOTB_SIM
  initial begin
    $dumpfile("waveform_gen.vcd");
    $dumpvars(0, waveform_gen);
    #1;
  end
`endif

  // icarus verilog doesn't support indexing in always_* processes
  // so we pull them out here
  wire [27:0] phase_with_offset = phase + phase_offset;
  wire [13:0] phase_upper_half = phase_with_offset[27:14];
  wire phase_msb = phase_with_offset[27];
  wire [13:0] sine_value;

  sin_rom sine_table (
      .addr(phase_upper_half),
      .sine(sine_value)
  );

  always_comb begin
    case (wave_style)
      // sine wave
      2'b00: begin
        outval = sine_value;
      end

      // square wave
      2'b01: begin
        if (phase_msb) begin
          outval = 14'h3FFF;
        end else begin
          outval = 0;
        end
      end

      // triangle wave
      // only uses the lower 13b of the 14b word, so we scale by two
      2'b10: begin
        if (phase_msb) begin
          outval = ~(phase_upper_half << 1);
        end else begin
          outval = phase_upper_half << 1;
        end
      end

      // sawtooth wave
      2'b11: begin
        outval = phase_upper_half;
      end

      default: outval = phase_upper_half;
    endcase
  end

endmodule
