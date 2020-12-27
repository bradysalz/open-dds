import random

import cocotb
from cocotb import clock, triggers

CLK_FREQ = 25e6
CLK_PER = 1 / CLK_FREQ
CLK_PER_NS = CLK_PER * 1e9


@cocotb.test()
async def test_init_acc(dut):
    """Verify that we zero init correctly."""
    clk = clock.Clock(dut.clk, CLK_PER_NS, units='ns')
    cocotb.fork(clk.start())

    # Toggle reset
    dut.rst <= 1
    dut.freq_word <= 0
    await triggers.FallingEdge(dut.clk)
    dut.rst <= 0
    await triggers.FallingEdge(dut.clk)

    if dut.phase.value != 0:
        raise ValueError('Phase accumulator failed to initialize correctly')


@cocotb.test()
async def test_accumulator(dut):
    """Verify that we accumulate values."""
    clk = clock.Clock(dut.clk, CLK_PER_NS, units='ns')
    cocotb.fork(clk.start())

    acc_size = dut.ACC_SIZE.value
    dut.freq_word <= random.randint(0, 2**acc_size - 1)

    # Toggle reset
    dut.rst <= 1
    await triggers.FallingEdge(dut.clk)
    dut.rst <= 0
    await triggers.FallingEdge(dut.clk)

    # Test ten cycles of it, arbitrarily chosen
    for idx in range(10):
        expected = (dut.freq_word.value * (idx + 1)) % 2**acc_size
        if dut.phase.value != expected:
            raise ValueError(f'Failed on cycle {idx}, expected {expected} '
                             f'but got {int(dut.phase.value)}')
        await triggers.FallingEdge(dut.clk)
