# pyevmasm
[![PyPI version](https://badge.fury.io/py/pyevmasm.svg)](https://badge.fury.io/py/pyevmasm)
[![Slack Status](https://empireslacking.herokuapp.com/badge.svg)](https://empireslacking.herokuapp.com)

pyevmasm is an assembler and disassembler library for the Ethereum Virtual Machine (EVM). It includes a commandline utility and a Python API.

## CLI Examples with evmasm

`evmasm` is a commandline utility that uses pyevmasm to assemble or disassemble EVM:

```
usage: evmasm [-h] (-a | -d | -t) [-bi] [-bo] [-i [INPUT]] [-o [OUTPUT]] [-f FORK]

pyevmasm the EVM assembler and disassembler

optional arguments:
  -h, --help            show this help message and exit
  -a, --assemble        Assemble EVM instructions to opcodes
  -d, --disassemble     Disassemble EVM to opcodes
  -t, --print-opcode-table
                        List supported EVM opcodes
  -bi, --binary-input   Binary input mode (-d only)
  -bo, --binary-output  Binary output mode (-a only)
  -i [INPUT], --input [INPUT]
                        Input file, default=stdin
  -o [OUTPUT], --output [OUTPUT]
                        Output file, default=stdout
  -f FORK, --fork FORK  Fork, default: byzantium. Possible: frontier,
                        homestead, tangerine_whistle, spurious_dragon,
                        byzantium, constantinople, serenity. Also an unsigned
                        block number is accepted to select the fork.
```

Disassembling the preamble of compiled contract:

```
$ echo -n "608060405260043610603f57600035" | evmasm -d
00000000: PUSH1 0x80
00000002: PUSH1 0x40
00000004: MSTORE
00000005: PUSH1 0x4
00000007: CALLDATASIZE
00000008: LT
00000009: PUSH1 0x3f
0000000b: JUMPI
0000000c: PUSH1 0x0
0000000e: CALLDATALOAD
```

## Python API Examples

```
>>> from pyevmasm import instruction_tables, disassemble_hex, disassemble_all, assemble_hex
>>> instruction_table = instruction_tables['byzantium']
>>> instruction_table[20]
Instruction(0x14, 'EQ', 0, 2, 1, 3, 'Equality comparision.', None, 0)
>>> instruction_table['EQ']
Instruction(0x14, 'EQ', 0, 2, 1, 3, 'Equality comparision.', None, 0)
>>> instrs = list(disassemble_all(binascii.unhexlify('608060405260043610603f57600035')))
>>> instrs.insert(1, instruction_table['JUMPI'])
>>> a = assemble_hex(instrs)
>>> a
'0x60805760405260043610603f57600035'
>>> print(disassemble_hex(a))
PUSH1 0x80
JUMPI
PUSH1 0x40
MSTORE
...
>>> assemble_hex('PUSH1 0x40\nMSTORE\n')
'0x604052'
```

# Installation

Python >=2.7 or Python >=3.3 is required.

Install the latest stable version using pip:
```
pip install pyevmasm
```

Or, install the library from source:
```
git clone https://github.com/trailofbits/pyevmasm
cd pyevmasm
python setup.py install --user
```

## Documentation

[https://pyevmasm.readthedocs.io](https://pyevmasm.readthedocs.io)

New issues, feature requests, and contributions are welcome. Join us in #ethereum channel on the [Empire Hacking Slack](https://empireslacking.herokuapp.com) to discuss Ethereum security tool development.
