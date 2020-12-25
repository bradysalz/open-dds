#!/usr/bin/env python3
"""Generate a sine wave ROM for the DDS."""
import math

import click


@click.command()
@click.option('-b', '--bits', default=14, help='Number of bits')
@click.option('-o', '--output', default='sin_rom.dat', help='Output file name')
def generate_rom(bits: int, output: str):
    """Generate a sine wave ROM for the DDS.

    This generates a unipolar sine wave that range from [0, 2**bits]. Each
    address is the phase, and the value is sine(addr).
    """
    vals = [
        min(2**(bits) * (1 + math.sin(2 * math.pi * val / 2**bits)) / 2,
            2**bits - 1) for val in range(2**bits)
    ]
    with open(output, 'w') as f:
        for v in vals:
            f.write(f'{int(v):012b}\n')


if __name__ == '__main__':
    generate_rom()
