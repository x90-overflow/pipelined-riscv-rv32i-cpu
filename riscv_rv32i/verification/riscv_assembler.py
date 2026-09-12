from test_utils import get_bits

__all__ = ["add", "sub", "and_", "or_", "xor_", "sll", "srl", "sra", "slt", "sltu",
           "addi", "andi", "ori", "xori", "slti", "lw", "sw", "beq", "bne", "blt",
           "bge", "bltu", "bgeu", "jal", "jalr", "lui", "auipc"]

OP_REG = 0b0110011
OP_IMM = 0b0010011
OP_LOAD = 0b0000011
OP_STORE = 0b0100011
OP_BRANCH = 0b1100011
OP_JAL = 0b1101111
OP_JALR = 0b1100111
OP_LUI = 0b0110111
OP_AUIPC = 0b0010111

def r_type(funct7, rs2, rs1, funct3, rd, opcode):
    return (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode

def i_type(imm, rs1, funct3, rd, opcode):
    return (get_bits(imm, 11, 0) << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode

def s_type(imm, rs2, rs1, funct3, opcode):
    return (get_bits(imm, 11, 5) << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | \
        (get_bits(imm, 4, 0) << 7) | opcode

def b_type(imm, rs2, rs1, funct3, opcode):
    return (get_bits(imm, 12, 12) << 31) | (get_bits(imm, 10, 5) << 25) | (rs2 << 20) | \
        (rs1 << 15) | (funct3 << 12) | (get_bits(imm, 4, 1) << 8) | (get_bits(imm, 11, 11) << 7) | \
        opcode

def u_type(imm20, rd, opcode):
    return ((imm20 & 0xFFFFF) << 12) | (rd << 7) | opcode

def j_type(imm, rd, opcode):
    return (get_bits(imm, 20, 20) << 31) | (get_bits(imm, 10, 1) << 21) | (get_bits(imm, 11, 11) << 20) | \
        (get_bits(imm, 19, 12) << 12) | (rd << 7) | opcode

def add(rd, rs1, rs2): return r_type(0b0000000, rs2, rs1, 0b000, rd, OP_REG)
def sub(rd, rs1, rs2): return r_type(0b0100000, rs2, rs1, 0b000, rd, OP_REG)
def and_(rd, rs1, rs2): return r_type(0b0000000, rs2, rs1, 0b111, rd, OP_REG)
def or_(rd, rs1, rs2): return r_type(0b0000000, rs2, rs1, 0b110, rd, OP_REG)
def xor_(rd, rs1, rs2): return r_type(0b0000000, rs2, rs1, 0b100, rd, OP_REG)
def sll(rd, rs1, rs2): return r_type(0b0000000, rs2, rs1, 0b001, rd, OP_REG)
def srl(rd, rs1, rs2): return r_type(0b0000000, rs2, rs1, 0b101, rd, OP_REG)
def sra(rd, rs1, rs2): return r_type(0b0100000, rs2, rs1, 0b101, rd, OP_REG)
def slt(rd, rs1, rs2): return r_type(0b0000000, rs2, rs1, 0b010, rd, OP_REG)
def sltu(rd, rs1, rs2): return r_type(0b0000000, rs2, rs1, 0b011, rd, OP_REG)

def addi(rd, rs1, imm): return i_type(imm, rs1, 0b000, rd, OP_IMM)
def andi(rd, rs1, imm): return i_type(imm, rs1, 0b111, rd, OP_IMM)
def ori(rd, rs1, imm): return i_type(imm, rs1, 0b110, rd, OP_IMM)
def xori(rd, rs1, imm): return i_type(imm, rs1, 0b100, rd, OP_IMM)
def slti(rd, rs1, imm): return i_type(imm, rs1, 0b010, rd, OP_IMM)

def lw(rd, rs1, imm): return i_type(imm, rs1, 0b010, rd, OP_LOAD)
def sw(rs2, rs1, imm): return s_type(imm, rs2, rs1, 0b010, OP_STORE)

def beq(rs1, rs2, imm): return b_type(imm, rs2, rs1, 0b000, OP_BRANCH)
def bne(rs1, rs2, imm): return b_type(imm, rs2, rs1, 0b001, OP_BRANCH)
def blt(rs1, rs2, imm): return b_type(imm, rs2, rs1, 0b100, OP_BRANCH)
def bge(rs1, rs2, imm): return b_type(imm, rs2, rs1, 0b101, OP_BRANCH)
def bltu(rs1, rs2, imm): return b_type(imm, rs2, rs1, 0b110, OP_BRANCH)
def bgeu(rs1, rs2, imm): return b_type(imm, rs2, rs1, 0b111, OP_BRANCH)

def jal(rd, imm): return j_type(imm, rd, OP_JAL)
def jalr(rd, rs1, imm): return i_type(imm, rs1, 0b000, rd, OP_JALR)

def lui(rd, imm20): return u_type(imm20, rd, OP_LUI)
def auipc(rd, imm20): return u_type(imm20, rd, OP_AUIPC)
