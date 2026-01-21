import pyevmasm as EVMAsm


def test_ADD_1():
    instruction = EVMAsm.disassemble_one(b"\x60\x10")
    assert (
        EVMAsm.Instruction(0x60, "PUSH", 1, 0, 1, 3, "Place 1 byte item on stack.", 16, 0)
        == instruction
    )

    instruction = EVMAsm.assemble_one("PUSH1 0x10")
    assert instruction == EVMAsm.Instruction(
        0x60, "PUSH", 1, 0, 1, 3, "Place 1 byte item on stack.", 16, 0
    )

    instructions1 = EVMAsm.disassemble_all(b"\x30\x31")
    instructions2 = EVMAsm.assemble_all("ADDRESS\nBALANCE")
    assert all(a == b for a, b in zip(instructions1, instructions2, strict=True))

    # High level simple assembler/disassembler
    bytecode = EVMAsm.assemble_hex(
        """PUSH1 0x80
           BLOCKHASH
           MSTORE
           PUSH1 0x2
           PUSH2 0x100
        """
    )
    assert bytecode == "0x608040526002610100"

    asmcode = EVMAsm.disassemble_hex("0x608040526002610100")
    assert asmcode == """PUSH1 0x80\nBLOCKHASH\nMSTORE\nPUSH1 0x2\nPUSH2 0x100"""


def test_STOP():
    insn = EVMAsm.disassemble_one(b"\x00")
    assert insn.mnemonic == "STOP"


def test_JUMPI():
    insn = EVMAsm.disassemble_one(b"\x57")
    assert insn.mnemonic == "JUMPI"
    assert insn.is_branch


def test_pre_byzantium():
    insn = EVMAsm.disassemble_one(b"\x57", fork="frontier")
    assert insn.mnemonic == "JUMPI"
    assert insn.is_branch
    insn = EVMAsm.disassemble_one(b"\xfa", fork="frontier")
    assert insn.mnemonic == "INVALID"  # STATICCALL added in byzantium
    insn = EVMAsm.disassemble_one(b"\xfd", fork="frontier")
    assert insn.mnemonic == "INVALID"  # REVERT added in byzantium


def test_byzantium_fork():
    insn = EVMAsm.disassemble_one(b"\x57", fork="byzantium")
    assert insn.mnemonic == "JUMPI"
    assert insn.is_branch
    insn = EVMAsm.disassemble_one(b"\x1b", fork="byzantium")
    assert insn.mnemonic == "INVALID"  # SHL added in constantinople
    insn = EVMAsm.disassemble_one(b"\x1c", fork="byzantium")
    assert insn.mnemonic == "INVALID"  # SHR added in constantinople
    insn = EVMAsm.disassemble_one(b"\x1d", fork="byzantium")
    assert insn.mnemonic == "INVALID"  # SAR added in constantinople
    insn = EVMAsm.disassemble_one(b"\x3f", fork="byzantium")
    assert insn.mnemonic == "INVALID"  # EXTCODEHASH added in constantinople
    insn = EVMAsm.disassemble_one(b"\xf5", fork="byzantium")
    assert insn.mnemonic == "INVALID"  # CREATE2 added in constantinople


def test_constantinople_fork():
    insn = EVMAsm.disassemble_one(b"\x1b", fork="constantinople")
    assert insn.mnemonic == "SHL"
    assert insn.is_arithmetic
    insn = EVMAsm.disassemble_one(b"\x1c", fork="constantinople")
    assert insn.mnemonic == "SHR"
    assert insn.is_arithmetic
    insn = EVMAsm.disassemble_one(b"\x1d", fork="constantinople")
    assert insn.mnemonic == "SAR"
    assert insn.is_arithmetic
    insn = EVMAsm.disassemble_one(b"\x3f", fork="constantinople")
    assert insn.mnemonic == "EXTCODEHASH"
    insn = EVMAsm.disassemble_one(b"\xf5", fork="constantinople")
    assert insn.mnemonic == "CREATE2"


def test_istanbul_fork():
    insn = EVMAsm.disassemble_one(b"\x31", fork="istanbul")
    assert insn.mnemonic == "BALANCE"
    assert insn.fee == 700
    assert insn.pops == 1
    assert insn.pushes == 1
    insn = EVMAsm.disassemble_one(b"\x3f", fork="istanbul")
    assert insn.mnemonic == "EXTCODEHASH"
    assert insn.fee == 700
    assert insn.pops == 1
    assert insn.pushes == 1
    insn = EVMAsm.disassemble_one(b"\x46", fork="istanbul")
    assert insn.mnemonic == "CHAINID"
    assert insn.fee == 2
    assert insn.pops == 0
    assert insn.pushes == 1
    insn = EVMAsm.disassemble_one(b"\x47", fork="istanbul")
    assert insn.mnemonic == "SELFBALANCE"
    assert insn.fee == 5
    assert insn.pops == 0
    assert insn.pushes == 1
    insn = EVMAsm.disassemble_one(b"\x54", fork="istanbul")
    assert insn.mnemonic == "SLOAD"
    assert insn.fee == 800
    assert insn.pops == 1
    assert insn.pushes == 1


def test_berlin_fork():
    insn = EVMAsm.disassemble_one(b"\xf1", fork="berlin")
    assert insn.mnemonic == "CALL"
    assert insn.pops == 7
    assert insn.pushes == 1
    assert insn.fee == 100


def test_london_fork():
    insn = EVMAsm.disassemble_one(b"\x48", fork="london")
    assert insn.mnemonic == "BASEFEE"
    assert insn.pops == 0
    assert insn.pushes == 1
    assert insn.fee == 2


def test_shanghai_fork():
    insn = EVMAsm.disassemble_one(b"\x5f", fork="shanghai")
    assert insn.mnemonic == "PUSH0"
    assert insn.fee == 2
    assert insn.pops == 0
    assert insn.pushes == 1
    assert insn.operand_size == 0


def test_cancun_fork():
    insn = EVMAsm.disassemble_one(b"\x49", fork="cancun")
    assert insn.mnemonic == "BLOBHASH"
    assert insn.fee == 3
    assert insn.pops == 1
    assert insn.pushes == 1
    insn = EVMAsm.disassemble_one(b"\x4a", fork="cancun")
    assert insn.mnemonic == "BLOBBASEFEE"
    assert insn.fee == 2
    assert insn.pops == 0
    assert insn.pushes == 1
    insn = EVMAsm.disassemble_one(b"\x5c", fork="cancun")
    assert insn.mnemonic == "TLOAD"
    assert insn.fee == 100
    assert insn.pops == 1
    assert insn.pushes == 1
    insn = EVMAsm.disassemble_one(b"\x5d", fork="cancun")
    assert insn.mnemonic == "TSTORE"
    assert insn.fee == 100
    assert insn.pops == 2
    assert insn.pushes == 0

    insn = EVMAsm.disassemble_one(b"\x20", fork="cancun")
    assert insn.mnemonic == "KECCAK256"
    assert insn.pops == 2
    assert insn.pushes == 1
    assert insn.fee == 30

    insn = EVMAsm.disassemble_one(b"\x31", fork="cancun")
    assert insn.mnemonic == "BALANCE"
    assert insn.pops == 1
    assert insn.pushes == 1
    assert insn.fee == 100

    insn = EVMAsm.disassemble_one(b"\x3b", fork="cancun")
    assert insn.mnemonic == "EXTCODESIZE"
    assert insn.pops == 1
    assert insn.pushes == 1
    assert insn.fee == 100

    insn = EVMAsm.disassemble_one(b"\x3c", fork="cancun")
    assert insn.mnemonic == "EXTCODECOPY"
    assert insn.pops == 4
    assert insn.pushes == 0
    assert insn.fee == 100

    insn = EVMAsm.disassemble_one(b"\x3f", fork="cancun")
    assert insn.mnemonic == "EXTCODEHASH"
    assert insn.pops == 1
    assert insn.pushes == 1
    assert insn.fee == 100

    insn = EVMAsm.disassemble_one(b"\x44", fork="cancun")
    assert insn.mnemonic == "PREVRANDAO"
    assert insn.pops == 0
    assert insn.pushes == 1
    assert insn.fee == 2

    insn = EVMAsm.disassemble_one(b"\x54", fork="cancun")
    assert insn.mnemonic == "SLOAD"
    assert insn.pops == 1
    assert insn.pushes == 1
    assert insn.fee == 100

    insn = EVMAsm.disassemble_one(b"\x58", fork="cancun")
    assert insn.mnemonic == "PC"
    assert insn.pops == 0
    assert insn.pushes == 1
    assert insn.fee == 2

    insn = EVMAsm.disassemble_one(b"\xf1", fork="cancun")
    assert insn.mnemonic == "CALL"
    assert insn.pops == 7
    assert insn.pushes == 1
    assert insn.fee == 100

    insn = EVMAsm.disassemble_one(b"\xf2", fork="cancun")
    assert insn.mnemonic == "CALLCODE"
    assert insn.pops == 7
    assert insn.pushes == 1
    assert insn.fee == 100

    insn = EVMAsm.disassemble_one(b"\xf4", fork="cancun")
    assert insn.mnemonic == "DELEGATECALL"
    assert insn.pops == 6
    assert insn.pushes == 1
    assert insn.fee == 100

    insn = EVMAsm.disassemble_one(b"\xfa", fork="cancun")
    assert insn.mnemonic == "STATICCALL"
    assert insn.pops == 6
    assert insn.pushes == 1
    assert insn.fee == 100


def test_osaka_fork():
    insn = EVMAsm.disassemble_one(b"\x1e", fork="osaka")
    assert insn.mnemonic == "CLZ"
    assert insn.pops == 1
    assert insn.pushes == 1
    assert insn.fee == 5


def test_assemble_DUP1_regression():
    insn = EVMAsm.assemble_one("DUP1")
    assert insn.mnemonic == "DUP1"
    assert insn.opcode == 0x80


def test_assemble_LOGX_regression():
    inst_table = EVMAsm.instruction_tables[EVMAsm.DEFAULT_FORK]
    log0_opcode = 0xA0
    for n in range(5):
        opcode = log0_opcode + n
        assert opcode in inst_table, f"{opcode!r} not in instruction_table"
        asm = "LOG" + str(n)
        assert asm in inst_table, f"{asm!r} not in instruction_table"
        insn = EVMAsm.assemble_one(asm)
        assert insn.mnemonic == asm
        assert insn.opcode == opcode


def test_consistency_assembler_disassembler():
    """Tests whether every opcode that can be disassembled can also be assembled."""
    inst_table = EVMAsm.instruction_tables[EVMAsm.DEFAULT_FORK]
    for opcode in inst_table.keys():  # noqa: SIM118
        b = opcode.to_bytes(1, "little") + b"\x00" * 32
        inst_dis = EVMAsm.disassemble_one(b)
        a = str(inst_dis)
        inst_as = EVMAsm.assemble_one(a)
        assert inst_dis == inst_as
