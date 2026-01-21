#!/usr/bin/env python
import argparse
import binascii
import sys

from .evmasm import (
    DEFAULT_FORK,
    accepted_forks,
    assemble_all,
    assemble_hex,
    block_to_fork,
    disassemble_all,
    instruction_tables,
)


def main():
    parser = argparse.ArgumentParser(description="pyevmasm the EVM assembler and disassembler")
    group_action = parser.add_mutually_exclusive_group(required=True)
    group_action.add_argument(
        "-a",
        "--assemble",
        action="store_true",
        help="Assemble EVM instructions to opcodes",
    )
    group_action.add_argument(
        "-d", "--disassemble", action="store_true", help="Disassemble EVM to opcodes"
    )
    group_action.add_argument(
        "-t",
        "--print-opcode-table",
        action="store_true",
        help="List supported EVM opcodes",
    )
    parser.add_argument(
        "-bi", "--binary-input", action="store_true", help="Binary input mode (-d only)"
    )
    parser.add_argument(
        "-bo",
        "--binary-output",
        action="store_true",
        help="Binary output mode (-a only)",
    )
    parser.add_argument(
        "-i",
        "--input",
        nargs="?",
        default=sys.stdin,
        type=argparse.FileType("r"),
        help="Input file, default=stdin",
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        default=sys.stdout,
        type=argparse.FileType("w"),
        help="Output file, default=stdout",
    )
    parser.add_argument(
        "-f",
        "--fork",
        default=DEFAULT_FORK,
        type=str,
        help="Fork, default: cancun. "
        "Possible: frontier, homestead, tangerine_whistle, spurious_dragon, byzantium, constantinople, istanbul, london, shanghai, cancun, serenity. "
        "Also an unsigned block number is accepted to select the fork.",
    )

    args = parser.parse_args(sys.argv[1:])
    arg_fork = args.fork.lower()
    if arg_fork not in accepted_forks:
        try:
            block_number = abs(int(arg_fork))
            fork = block_to_fork(block_number)
        except ValueError:
            sys.stderr.write(
                f"Wrong fork name or block number. "
                f"Please provide an integer or one of {accepted_forks}.\n"
            )
            sys.exit(1)
    else:
        fork = arg_fork

    instruction_table = instruction_tables[fork]
    if args.print_opcode_table:
        for instr in instruction_table:
            print(f"0x{instr.opcode:02x}: {instr.name:16s} {instr.description:s}")
        sys.exit(0)

    if args.assemble:
        try:
            asm = args.input.read().strip().rstrip()
        except KeyboardInterrupt:
            sys.exit(0)
        if args.binary_output:
            for i in assemble_all(asm, fork=fork):
                args.output.buffer.write(i.bytes)
        else:
            args.output.write(assemble_hex(asm, fork=fork) + "\n")

    if args.disassemble:
        if args.binary_input:
            buf = args.input.buffer.read()
        else:
            try:
                buf = args.input.read().strip().rstrip()
            except KeyboardInterrupt:
                sys.exit(0)
            except UnicodeDecodeError:
                print("Input is binary? try using -bi.")
                sys.exit(1)

            if buf[:3] == "EVM":  # binja prefix
                buf = buf[3:]
            elif buf[:2] == "0x":  # hex prefixed
                buf = binascii.unhexlify(buf[2:])
            else:  # detect all hex buffer
                buf_set = set()
                for c in buf:
                    buf_set.add(c.lower())

                hex_set = set(list("0123456789abcdef"))
                if buf_set <= hex_set:  # subset
                    buf = binascii.unhexlify(buf)

        insns = list(disassemble_all(buf, fork=fork))
        for i in insns:
            args.output.write(f"{i.pc:08x}: {i}\n")


if __name__ == "__main__":
    main()
