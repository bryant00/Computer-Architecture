"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    PC = 0
    SP = 6
    IS = 5
    IM = 4

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory
        self.ram = [0] * 256
        # 8 general purpose registers
        self.registers = [0] * 8
        # internal registers may need
        # self.IM = self.registers[self.IMr]
        # self.IS = self.registers[self.ISr]
        # self.SP = self.registers[self.SPr]
        # self.PC = self.registers[self.PCr]
        self.operations = {"PRN": 0b01000111, "LDI": 0b10000010, "HLT": 0b00000001}

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    # accept the address to read and return the value stored there
    def ram_read(self, mar):
        value = self.ram[mar]
        return value

    # accept a value to write, and the address to write it to
    def ram_write(self, value, mdr):
        memory = self.ram[mdr]
        memory = value
        return memory

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
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

    def run(self):
        while True:
            # read the memory address that's stored in register and and store that result in IR
            ir = self.PC
            # read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
            operand_a = self.ram_read[PCr + 1]
            operand_b = self.ram_read[PCr + 2]

            # Then, depending on the value of the opcode, perform the actions needed for the instruction per the LS-8 spec. Maybe an if-elif cascade...? There are other options, too.
            # After running code for any particular instruction, the PC needs to be updated
            # # LDI R0,8
            if ir == self.operations.LDI:
                self.registers[operand_a] = operand_b
                self.pc += 3
            elif ir == self.operations.PRN:
                print(self.registers[operand_a])
                self.pc += 2
            elif ir == self.operations.HLT:
                running = False
