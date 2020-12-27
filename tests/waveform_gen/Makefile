SIM=icarus
TOPLEVEL_LANG = systemverilog
PWD=$(shell pwd)
VERILOG_SOURCES=$(PWD)/../../hdl/waveform_gen.sv $(PWD)/../../hdl/rom/sin_rom.sv
TOPLEVEL := waveform_gen
MODULE := test_waveform_gen

include $(shell cocotb-config --makefiles)/Makefile.sim
