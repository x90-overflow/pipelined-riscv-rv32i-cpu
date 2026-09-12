from test_utils import MASK, get_bits, to_signed, sign_extend

OP_REG = 0b0110011
OP_IMM = 0b0010011
OP_LOAD = 0b0000011
OP_STORE = 0b0100011
OP_BRANCH = 0b1100011
OP_JAL = 0b1101111
OP_JALR = 0b1100111
OP_LUI = 0b0110111
OP_AUIPC = 0b0010111

def decode_imm(instr):
    opcode = get_bits(instr, 6, 0)
    if opcode in (OP_IMM, OP_LOAD, OP_JALR):
        return sign_extend(get_bits(instr, 31, 20), 12)
    elif opcode == OP_STORE:
        imm = (get_bits(instr, 31, 25) << 5) | get_bits(instr, 11, 7)
        return sign_extend(imm, 12)
    elif opcode == OP_BRANCH:
        imm = (get_bits(instr, 31, 31) << 12) | (get_bits(instr, 7, 7) << 11) | \
            (get_bits(instr, 30, 25) << 5) | (get_bits(instr, 11, 8) << 1)
        return sign_extend(imm, 13)
    elif opcode == OP_JAL:
        imm = (get_bits(instr, 31, 31) << 20) | (get_bits(instr, 19, 12) << 12) | \
            (get_bits(instr, 20, 20) << 11) | (get_bits(instr, 30, 21) << 1)
        return sign_extend(imm, 21)
    elif opcode in (OP_LUI, OP_AUIPC):
        return (get_bits(instr, 31, 12) << 12) & MASK
    else:
        return 0

def alu_compute(a, b, funct3, funct7_5, is_reg):
    a &= MASK
    b &= MASK
    shift_count = b & 0x1F
    if funct3 == 0b000:
        if is_reg and funct7_5:
            return (a - b) & MASK
        return (a + b) & MASK
    elif funct3 == 0b001:
        return (a << shift_count) & MASK
    elif funct3 == 0b010:
        if (to_signed(a) < to_signed(b)):
            return 1
        return 0
    elif funct3 == 0b011:
        if a < b:
            return 1
        return 0
    elif funct3 == 0b100:
        return a^b
    elif funct3 == 0b101:
        if funct7_5:
            return (to_signed(a) >> shift_count) & MASK
        return a >> shift_count
    elif funct3 == 0b110:
        return a | b
    elif funct3 == 0b111:
        return a & b
    else:
        return 0

def branch_taken(funct3, a, b):
    a &= MASK
    b &= MASK
    if funct3 == 0b000:
        return a == b
    elif funct3 == 0b001:
        return a != b
    elif funct3 == 0b100:
        return to_signed(a) < to_signed(b)
    elif funct3 == 0b101:
        return to_signed(a) >= to_signed(b)
    elif funct3 == 0b110:
        return a < b
    elif funct3 == 0b111:
        return a >= b
    else:
        return 0

def instr_exe(words, mem_words=256, max_steps=10000):
    registers = [0]*32
    mem = [0]*mem_words
    pc = 0

    for _ in range(max_steps):
        pc_x = pc >> 2
        if pc_x < 0 or pc_x >= len(words):
            break
        instr = words[pc_x]

        opcode = get_bits(instr, 6, 0)
        rd = get_bits(instr, 11, 7)
        funct3 = get_bits(instr, 14, 12)
        rs1 = get_bits(instr, 19, 15)
        rs2 = get_bits(instr, 24, 20)
        funct7_5 = get_bits(instr, 30, 30)

        imm = decode_imm(instr)
        a = registers[rs1]
        b = registers[rs2]
        pc_next = (pc + 4) & MASK
        wrb_result = None

        if opcode == OP_REG:
            wrb_result = alu_compute(a, b, funct3, funct7_5, True)
        elif opcode == OP_IMM:
            wrb_result = alu_compute(a, imm, funct3, funct7_5, False)
        elif opcode == OP_LOAD:
            addr = (a + imm) & MASK
            wrb_result = mem[(addr >> 2) % mem_words]
        elif opcode == OP_STORE:
            addr = (a + imm) & MASK
            mem[(addr >> 2) % mem_words] = b
        elif opcode == OP_BRANCH:
            if branch_taken(funct3, a, b):
                pc_next = (pc + imm) & MASK
        elif opcode == OP_JAL:
            wrb_result = (pc + 4) & MASK
            pc_next = (pc + imm) & MASK
        elif opcode == OP_JALR:
            wrb_result = (pc + 4) & MASK
            pc_next = ((a + imm) & ~1) & MASK
        elif opcode == OP_LUI:
            wrb_result = imm
        elif opcode == OP_AUIPC:
            wrb_result = (pc + imm) & MASK

        if wrb_result is not None and rd != 0:
            registers[rd] = wrb_result & MASK
        pc = pc_next
        
    return registers, mem
