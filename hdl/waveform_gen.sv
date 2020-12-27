`default_nettype none `timescale 1ns / 1ps

/**
* Module waveform_gen
*
* Generates the final output waveform
*
**/

module waveform_gen (
    input wire [27:0] phase,
    input wire [13:0] phase_offset,
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

  wire [27:0] phase_with_offset = phase + phase_offset;
  wire [13:0] phase_msb = phase_with_offset[27:13];
  wire [13:0] sine_value;

  sin_rom sine_table (
      .addr(phase_msb),
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
        if (phase_msb[13]) begin
          outval = 14'h3FF;
        end else begin
          outval = 0;
        end
      end

      // triangle wave
      2'b10: begin
        if (phase_msb[13]) begin
          outval = 14'h3FF - phase_msb;
        end else begin
          outval = phase_msb << 1;
        end
      end

      // sawtooth wave
      2'b11: begin
        outval = phase_msb;
      end

      default: outval = phase_msb;
    endcase
  end

endmodule
