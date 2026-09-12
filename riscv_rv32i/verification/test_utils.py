INS_WIDTH = 32
MASK = (1 << INS_WIDTH) - 1

def to_signed(value):
    sign_bit = 1 << (INS_WIDTH - 1)
    if sign_bit & value:
        return value - (1 << INS_WIDTH)
    else:
        return value

def get_bits(value, high, low):
    bit_group = high - low + 1
    group_mask = (1 << bit_group) - 1
    return (value >> low) & group_mask

def sign_extend(value, current_size):
    sign_bit = 1 << (current_size - 1)
    if value & sign_bit:
        return (value - (1 << current_size)) & MASK
    else:
        return value

class Scoreboard:
    def __init__(self, name):
        self.name = name
        self.checks = 0
        self.errors = 0
    def check(self, expected, actual, context=""):
        self.checks += 1
        if actual != expected:
            self.errors += 1
            raise AssertionError(f"[{self.name}] {context}: DUT={actual:#010x} expected={expected:#010x}")

