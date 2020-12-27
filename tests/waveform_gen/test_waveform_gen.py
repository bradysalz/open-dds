import cocotb
from cocotb import triggers


@cocotb.test()
async def test_it_runs(dut):
    dut.phase <= 0
    dut.phase_offset <= 0
    dut.wave_style <= 2

    for idx in range(1000):
        dut.phase <= idx * 2**20
        await triggers.Timer(1, units='ns')
