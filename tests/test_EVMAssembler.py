import unittest

import pyevmasm as EVMAsm


# noinspection PyPep8Naming
class EVMTest_Assembler(unittest.TestCase):
    _multiprocess_can_split_ = True
    maxDiff = None

    def test_ADD_1(self):
        instruction = EVMAsm.disassemble_one(b'\x60\x10')
        self.assertEqual(EVMAsm.Instruction(0x60, 'PUSH', 1, 0, 1, 0, 'Place 1 byte item on stack.', 16, 0),
                         instruction)

        instruction = EVMAsm.assemble_one('PUSH1 0x10')
        EVMAsm.Instruction(0x60, 'PUSH', 1, 0, 1, 0, 'Place 1 byte item on stack.', 16, 0)

        instructions1 = EVMAsm.disassemble_all(b'\x30\x31')
        instructions2 = EVMAsm.assemble_all('ADDRESS\nBALANCE')
        self.assertTrue(all(a == b for a, b in zip(instructions1, instructions2)))

        # High level simple assembler/disassembler

        bytecode = EVMAsm.assemble_hex(
            """PUSH1 0x80
               BLOCKHASH
               MSTORE
               PUSH1 0x2
               PUSH2 0x100
            """
        )
        self.assertEqual(bytecode, '0x608040526002610100')

        asmcode = EVMAsm.disassemble_hex('0x608040526002610100')
        self.assertEqual(asmcode, '''PUSH1 0x80\nBLOCKHASH\nMSTORE\nPUSH1 0x2\nPUSH2 0x100''')

    def test_STOP(self):
        insn = EVMAsm.disassemble_one(b'\x00')
        self.assertTrue(insn.mnemonic == 'STOP')

    def test_JUMPI(self):
        insn = EVMAsm.disassemble_one(b'\x57')
        self.assertTrue(insn.mnemonic == 'JUMPI')
        self.assertTrue(insn.is_branch)


if __name__ == '__main__':
    unittest.main()
