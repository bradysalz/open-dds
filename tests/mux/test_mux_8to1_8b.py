import random

import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def mux_simple_test(dut):
    """Tests that for a specified input, we get the matching output."""

    dut.sel = 2
    dut.in0 = 0
    dut.in1 = 1
    dut.in2 = 2
    dut.in3 = 3
    dut.in4 = 4
    dut.in5 = 5
    dut.in6 = 6
    dut.in7 = 7

    await Timer(2, units='ns')
    if dut.out.value != 2:
        raise ValueError(f"Mux output is incorrect: {dut.out.value} != 2")


@cocotb.test()
async def mux_randomized_test(dut):
    """Tests all inputs with random values."""

    inputs = [
        dut.in0, dut.in1, dut.in2, dut.in3, dut.in4, dut.in5, dut.in6, dut.in7
    ]
    for idx in range(8):
        vals = [random.getrandbits(8) for _ in range(8)]
        for idy in range(8):
            inputs[idy] <= vals[idy]
        dut.sel <= idx

        await Timer(2, units='ns')
        if dut.out.value != vals[idx]:
            raise ValueError(
                f"Mux output is incorrect: {dut.out.value} != {vals[idx]}")
