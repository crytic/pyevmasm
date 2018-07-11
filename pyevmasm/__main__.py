#!/usr/bin/env python
import argparse
import sys
import binascii

from .evmasm import EVMAsm


def main():
    parser = argparse.ArgumentParser(description="pyevmasm the EVM assembler and disassembler")
    group_action = parser.add_mutually_exclusive_group(required=True)
    group_action.add_argument('-a', '--assemble', action='store_true', help='Assemble EVM instructions to opcodes')
    group_action.add_argument('-d', '--disassemble', action='store_true', help='Disassemble EVM to opcodes')
    group_action.add_argument('-t', '--print-opcode-table', action='store_true', help='List supported EVM opcodes')
    parser.add_argument('-i', '--input', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file, default=stdin')
    parser.add_argument('-o', '--output', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file, default=stdout')

    args = parser.parse_args(sys.argv[1:])

    if args.print_opcode_table:
        table = EVMAsm._get_reverse_table()
        for mnemonic in table.keys():
            # This relies on the internal format 
            (opcode, name, immediate_operand_size, pops, pushes, gas, description) = table[mnemonic]
            print("%02x: %-16s %s" % (opcode, mnemonic, description))
        sys.exit(0)

    if args.assemble:
        asm = args.input.read().strip().rstrip()
        args.output.write(EVMAsm.assemble_hex(asm) + "\n")

    if args.disassemble:
        buf = args.input.read().strip().rstrip()
        if buf[:3] == 'EVM':  # binja prefix
            buf = buf[3:]
        elif buf[:2] == '0x':  # hex prefixed
            buf = binascii.unhexlify(buf[2:])
        else:  # detect all hex buffer
            buf_set = set()
            for c in buf:
                buf_set.add(c.lower())

            hex_set = set(list('0123456789abcdef'))
            if buf_set <= hex_set:  # subset
                buf = binascii.unhexlify(buf)

        insns = list(EVMAsm.disassemble_all(buf))
        for i in insns:
            args.output.write("%08x: %s\n" % (i.pc, str(i)))


if __name__ == "__main__":
    main()
