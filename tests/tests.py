import unittest
from pyevmasm import EVMAsm

class DisassembleTests(unittest.TestCase):
    def test_STOP(self):
        insn = EVMAsm.disassemble_one('\x00')
        self.assertTrue(str(insn) == 'STOP')

    def test_JUMPI(self):
        insn = EVMAsm.disassemble_one('\x57')
        self.assertTrue(str(insn) == 'JUMPI')
        self.assertTrue(insn.is_branch)
 

if __name__ == '__main__':
    unittest.main()
