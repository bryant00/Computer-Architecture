"""CPU functionality."""

import sys

LDI = 0b10000010  # load "immediate", store a value in a register, or "set this register to this value"
PRN = 0b01000111  # print the numeric value stored in a register
HLT = 0b00000001  # halt the CPU and exit the emulator
MUL = 0b10100010
PUSH = 0b01000101  # pop the value at the top of the stack into the given register
POP = 0b01000110  # push the value in the given register on the stack
# SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256  # 256 bytes of memory
        self.reg = [0] * 8  # 8 general-purpose registers
        self.reg[7] = 244  # 7 registers, reg[8] is the stack pointer
        self.fla = [0] * 8
        self.hlt = False
        self.ops = {
            LDI: self.op_ldi,
            PRN: self.op_prn,
            HLT: self.op_hlt,
            MUL: self.op_mul,
            PUSH: self.op_push,
            POP: self.op_pop,
        }

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, blocks):
        """Load a program into memory."""

        address = 0
        for block in blocks:
            if (block[0] == "0") or (block[0] == "1"):
                self.ram[address] = int(block[:8], 2)
                # print(self.ram[address])
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def op_ldi(self, address, value):
        # operand_a = self.ram[self.pc + 1]  # targeted register
        # operand_b = self.ram[self.pc + 2]  # value to load
        # self.reg[operand_a] = operand_b
        self.reg[address] = value

    def op_prn(self, address, op_b):  # op a/b
        print(self.reg[address])  # op_a acts as address

    def op_hlt(self, op_a, op_b):
        self.hlt = True

    def op_mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)

    def op_push(self, operand_a, operand_b):
        # print("reg", self.reg)
        # print("push", self.reg[7])
        self.reg[7] -= 1  # decrement stack pointer
        sp = self.reg[7]  # sp variable
        self.ram[sp] = self.reg[operand_a]

    def op_pop(self, operand_a, operand_b):
        # print("reg", self.reg)
        # print("pop", self.reg[7])
        sp = self.reg[7]  # sp variable
        operand_b = self.ram[sp]
        self.reg[operand_a] = operand_b
        self.reg[7] += 1  # increment stack pointer

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def run(self):
        """Run the CPU."""
        while self.hlt == False:
            ir = self.ram[self.pc]  # set internal register to the program counter index
            operand_a = self.ram_read(self.pc + 1)  # next program counter index
            operand_b = self.ram_read(self.pc + 2)  # next next program counter index
            op_size = ir >> 6  # op_size internal register 6 bits to the right
            ins_set = ((ir >> 4) & 0b1) == 1
            if ir in self.ops:
                self.ops[ir](operand_a, operand_b)
            if not ins_set:
                self.pc += op_size + 1
            # self.trace()
