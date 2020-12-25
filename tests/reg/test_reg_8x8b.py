# These are pretty explicit tests that are probably overkill, but it's cool
# to learn how cocotb works with clocks
import random

import cocotb
from cocotb import clock
from cocotb import triggers

CLK_FREQ = 25e6
CLK_PER = 1 / CLK_FREQ
CLK_PER_NS = CLK_PER * 1e9
NUM_REG = 8


@cocotb.test()
async def reg_init_test(dut):
    """Tests that the register inits correctly."""
    clk = clock.Clock(dut.clk, CLK_PER_NS, units='ns')
    cocotb.fork(clk.start())

    dut.rst <= 1
    await triggers.FallingEdge(dut.clk)
    for addr in range(NUM_REG):
        dut.i_addr_rd <= addr
        await triggers.FallingEdge(dut.clk)
        if dut.o_data != 0:
            raise ValueError('Expected zero on init')


@cocotb.test()
async def reg_write_test(dut):
    """Tests that we can read and write to the regfile."""
    clk = clock.Clock(dut.clk, CLK_PER_NS, units='ns')
    cocotb.fork(clk.start())

    # Toggle reset
    dut.rst <= 1
    await triggers.FallingEdge(dut.clk)
    dut.rst <= 0
    await triggers.FallingEdge(dut.clk)

    truth_vals = [random.getrandbits(8) for _ in range(8)]
    dut._log.info(truth_vals)
    # Test wr_en = 1
    for addr in range(NUM_REG):
        val = truth_vals[addr]
        dut.i_en_wr <= 1
        dut.i_addr_wr <= addr
        dut.i_addr_rd <= addr
        dut.i_data <= val

        await triggers.FallingEdge(dut.clk)
        if dut.o_data.value != truth_vals[addr]:
            raise ValueError(f'Got {dut.o_data.value} expected {val}')

    # Test wr_en = 0
    dut.i_en_wr <= 0
    await triggers.FallingEdge(dut.clk)
    for addr in range(NUM_REG):
        dut.i_addr_wr <= addr
        dut.i_addr_rd <= addr
        val = random.getrandbits(8)
        dut.i_data <= val

        await triggers.FallingEdge(dut.clk)
        if dut.o_data.value != truth_vals[addr]:
            raise ValueError(f'On {addr}, Got {int(dut.o_data.value)} '
                             f' expected {truth_vals[addr]}')
