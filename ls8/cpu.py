"""CPU functionality."""

import sys

LDI = 0b10000010  # load "immediate", store a value in a register, or "set this register to this value"
PRN = 0b01000111  # print the numeric value stored in a register
HLT = 0b00000001  # halt the CPU and exit the emulator
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # 256 bytes of memory
        self.reg = [0] * 8  # 8 general-purpose registers
        self.pc = 0
        self.reg[7] = 255
        self.hlt = False
        self.ops = {
            LDI: self.op_ldi,
            PRN: self.op_prn,
            HLT: self.op_hlt,
            MUL: self.op_mul,
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
        self.reg[address] = value

    def op_prn(self, address, op_b):  # op a/b
        print(self.reg[address])  # op_a acts as address

    def op_hlt(self, op_a, op_b):
        self.hlt = True

    def op_mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)

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
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        while self.hlt == False:
            ir = self.ram[self.pc]

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            op_size = ir >> 6
            ins_set = ((ir >> 4) & 0b1) == 1

            if ir in self.ops:
                self.ops[ir](operand_a, operand_b)
            if not ins_set:
                self.pc += op_size + 1
            self.trace()
            # if not ins_set:
            #     self.pc += op_size + 1

            # if IR == LDI:
            #     self.reg[operand_a] = operand_b
            #     self.pc += 3
            # elif IR == PRN:
            #     print(self.reg[operand_a])
            #     self.pc += 2
            # elif IR == MUL:
            #     self.reg[operand_a] *= operand_b
            #     self.pc += 2
            # elif IR == HLT:
            #     running = False
