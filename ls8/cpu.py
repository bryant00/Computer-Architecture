"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
CMP = 0b10100111
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.fl = [0] * 8

        self.branch_table = {}
        self.branch_table[LDI] = self.handle_LDI

    def handle_LDI(self, operand_a, operand_b):
        # operand_a = int(self.ram_read(self.ir + 1), 2)
        # operand_b = int(self.ram_read(self.ir + 2), 2)
        self.reg[operand_a] = operand_b
        # self.ir += 3

    def load(self):
        """Load a program into memory."""
        address = 0
        program = []
        if len(sys.argv) != 2:
            print(f"usage: file.py filename", file=sys.stderr)
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.strip().split("#")
                    num = comment_split[0]
                    if num == "":
                        continue
                    x = int(num, 2)
                    program.append(x)
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)
        f.close
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "CMP":
            print(f"compare {self.reg[reg_a]} to {self.reg[reg_b]}")
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl[-3] = 1
                self.fl[-1], self.fl[-2] = 0, 0
                print(f"less than")
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl[-2] = 1
                self.fl[-1], self.fl[-3] = 0, 0
                print(f"greater than")
            else:
                self.fl[-1] = 1
                self.fl[-2], self.fl[-3] = 0, 0
                print(f"equal to")
        else:
            raise Exception("Unsupported ALU operation")

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

    def ram_read(self, count):
        return self.ram[count]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        self.load()
        IR = self.pc
        SP = 243
        running = True
        while running:
            operand_a = self.ram_read(IR + 1)
            operand_b = self.ram_read(IR + 2)
            # print(f" IR: {IR} || SP: {SP}")
            instruction = self.ram_read(IR)
            if self.ram[IR] == LDI:
                self.branch_table[LDI](operand_a, operand_b)
                # self.ram_write(operand_a, operand_b)
                IR += 3

            elif self.ram[IR] == PRN:
                print(f"PRINTING: {self.ram[self.ram[IR+1]]}")
                # print(self.ram)
                IR += 2

            elif self.ram[IR] == MUL:
                temp = self.ram_read(operand_a) * self.ram_read(operand_b)
                print(f"{self.ram_read(operand_a)} X {self.ram_read(operand_b)}")
                self.ram_write(operand_a, temp)
                IR += 3

            elif self.ram[IR] == CMP:
                self.alu("CMP", operand_a, operand_b)
                IR += 3

            elif self.ram[IR] == PUSH:
                SP -= 1
                item = self.ram_read(operand_a)
                self.ram_write(SP, item)
                IR += 2

            elif self.ram[IR] == POP:
                item = self.ram_read(SP)
                self.ram_write(operand_a, item)
                SP += 1
                IR += 2

            elif self.ram[IR] == CALL:
                SP -= 1
                self.ram_write(SP, IR)
                IR = self.ram_read(operand_a)

            elif self.ram[IR] == RET:
                IR = self.ram_read(SP) + 2

            elif self.ram[IR] == ADD:
                temp = self.ram_read(operand_a) + self.ram_read(operand_b)
                self.ram_write(operand_a, temp)
                IR += 3

            elif self.ram[IR] == HLT:
                running = False

            else:
                print(f"unrecognized input")
                IR += 1
