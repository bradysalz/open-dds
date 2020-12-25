import cocotb
from cocotb import triggers

NUM_BITS = 14


def checker(truth, meas):
    """TODO(Brady): pull this out into something more useful"""
    if truth != meas:
        raise ValueError(f'Expected {truth}, got {meas}')


@cocotb.test()
async def test_load_rom(dut):
    """Tests that we can just load the array.

    $readmemh() gave me so many problems that I think just having this in
    isolation is a great thing."""
    for idx in range(2**NUM_BITS):
        dut.addr <= idx
        await triggers.Timer(1, units='ns')


@cocotb.test()
async def test_easy_points(dut):
    """Tests 0, pi, and 2pi values in the ROM."""
    dut.addr <= 0
    await triggers.Timer(1, units='ns')
    checker(2**(NUM_BITS - 1), dut.sine.value)

    dut.addr <= 2**(NUM_BITS - 2)
    await triggers.Timer(1, units='ns')
    checker(2**NUM_BITS - 1, dut.sine.value)

    dut.addr <= 2**(NUM_BITS - 1)
    await triggers.Timer(1, units='ns')
    checker(2**(NUM_BITS - 1), dut.sine.value)

    dut.addr <= 2**(NUM_BITS - 1) + 2**(NUM_BITS - 2)
    await triggers.Timer(1, units='ns')
    checker(0, dut.sine.value)
