# Open DDS

Open DDS is an open source discrete digital synthesizer core for use in digital projects. The base core can create:

- sine waves
- square waves
- triangle waves

It comes with other common features like amplitude control and phase control. To generate modulated data, the core also supports up to eight amplitude, frequency, and phase words, which can be quickly altered for common modulation schemes.

## Installation

This repo uses `cocotb` for tests. To contribute, you'll need to install `verilator` as the simulator. After cloning the repo, setup dependencies with:

```bash
./bootstrap.sh
```

