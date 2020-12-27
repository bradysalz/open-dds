import enum
import math
import random

import cocotb
from cocotb import triggers

ACC_SIZE = 28
OUT_SIZE = 14


class WaveStyle(enum.IntEnum):
    SINE = 0
    SQUARE = 1
    TRIANGLE = 2
    SAWTOOTH = 3


@cocotb.test()
async def test_phase_offset(dut):
    """Verify adding the phase offset in."""
    dut.phase <= 0
    dut.phase_offset <= 0
    dut.wave_style <= WaveStyle.SAWTOOTH.value

    await triggers.Timer(1, units='ns')
    if dut.outval.value != 0:
        raise ValueError('Phase offset added incorrectly.')

    offset = random.getrandbits(ACC_SIZE)
    expected_val = (offset >> (ACC_SIZE - OUT_SIZE))

    dut.phase_offset <= offset
    await triggers.Timer(1, units='ns')
    if dut.outval.value != expected_val:
        dut._log.error(f'Got {dut.outval.value}, expected {expected_val}')
        raise ValueError('Phase offset added incorrectly.')


@cocotb.test()
async def test_sawtooth_wave(dut):
    """Verify sawtooth wave behavior

    Start with this wave since it's the simplest one.
    """
    dut.phase <= 0
    dut.phase_offset <= 0
    dut.wave_style <= WaveStyle.SAWTOOTH.value

    for idx in range(100):
        phase_val = random.getrandbits(ACC_SIZE)
        expected_val = (phase_val >> (ACC_SIZE - OUT_SIZE))

        dut.phase <= phase_val
        await triggers.Timer(1, units='ns')
        if dut.outval.value != expected_val:
            dut._log.error(f'Got {dut.outval.value}, expected {expected_val}')
            raise ValueError('Sawtooth wave failed to generate correctly.')


@cocotb.test()
async def test_square_wave(dut):
    """Verify square wave behavior."""
    dut.phase <= 0
    dut.phase_offset <= 0
    dut.wave_style <= WaveStyle.SQUARE.value

    for idx in range(100):
        phase_val = random.getrandbits(ACC_SIZE)
        sign = phase_val >> (ACC_SIZE - 1)
        expected_val = (2**OUT_SIZE - 1) if sign else 0

        dut.phase <= phase_val
        await triggers.Timer(1, units='ns')
        if dut.outval.value != expected_val:
            dut._log.error(f'Got {dut.outval.value}, expected {expected_val}')
            raise ValueError('Square wave failed to generate correctly.')


@cocotb.test()
async def test_triangle_wave(dut):
    """Verify triangle wave behavior."""
    dut.phase <= 0
    dut.phase_offset <= 0
    dut.wave_style <= WaveStyle.TRIANGLE.value

    for idx in range(100):
        phase_val = random.getrandbits(ACC_SIZE)
        shifted_val = (phase_val >> (ACC_SIZE - OUT_SIZE))
        sign = phase_val >> (ACC_SIZE - 1)
        if sign:
            expected_val = ~(shifted_val * 2) & 0x3FFF
        else:
            expected_val = shifted_val * 2

        dut.phase <= phase_val
        await triggers.Timer(1, units='ns')
        if dut.outval.value != expected_val:
            dut._log.error(
                f'Got {int(dut.outval.value)}, expected {expected_val}')
            raise ValueError('Triangle wave failed to generate correctly.')


@cocotb.test()
async def test_sine_wave(dut):
    """Verify sine wave behavior."""
    dut.phase <= 0
    dut.phase_offset <= 0
    dut.wave_style <= WaveStyle.SINE.value

    for idx in range(100):
        phase_val = random.getrandbits(ACC_SIZE)
        shifted_val = phase_val >> (ACC_SIZE - OUT_SIZE)
        expected_val = 0.5 + 0.5 * math.sin(
            2 * math.pi * shifted_val / 2**OUT_SIZE)
        expected_val = math.floor(2**(OUT_SIZE) * expected_val)

        dut.phase <= phase_val
        await triggers.Timer(1, units='ns')
        if dut.outval.value != expected_val:
            dut._log.error(
                f'Got {int(dut.outval.value)}, expected {expected_val}')
            raise ValueError('Sine wave failed to generate correctly.')


@cocotb.test()
async def test_generate_waveform(dut):
    """This isn't actually a test, just for viewing.

    All the other tests are nice, but they don't make easy waveforms to view.
    The point of this test is to just idle in a for loop and generate that.
    """
    dut.phase <= 0
    dut.phase_offset <= 0
    dut.wave_style <= WaveStyle.TRIANGLE.value
    for idx in range(5000):
        dut.phase <= (idx * 2**19) % 2**28
        await triggers.Timer(1, units='ns')
