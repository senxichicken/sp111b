class Assembler:
    def __init__(self):
        self.symbol_table = {}
        self.opcode_table = {
            'ADD': b'\x01',
            'SUB': b'\x02',
            'MOV': b'\x03',
            'LDR': b'\x04',
            'STR': b'\x05',
            'MUL': b'\x06',
            'DIV': b'\x07',
            'AND': b'\x08',
            'OR': b'\x09',
            'XOR': b'\x0A',
            'NOT': b'\x0B',
            'JMP': b'\x0C',
            'JZ': b'\x0D',
            'JNZ': b'\x0E',
            'JEQ': b'\x0F',
            'JNE': b'\x10',
            'JGT': b'\x11',
            'JLT': b'\x12',
            'IN': b'\x13',
            'OUT': b'\x14',
        }
        self.external_symbols = {}

    def assemble(self, assembly_code):
        lines = assembly_code.split('\n')
        machine_code = []

        current_address = 0
        for line_number, line in enumerate(lines, start=1):
            line = line.strip()
            if line and not line.startswith(';'):
                parts = line.split()
                if parts[0].endswith(':'):
                    label = parts[0].rstrip(':')
                    if label in self.symbol_table:
                        raise ValueError(f'Duplicate label at line {line_number}: {label}')
                    self.symbol_table[label] = current_address
                else:
                    current_address += 1

        for line_number, line in enumerate(lines, start=1):
            line = line.strip()
            if line and not line.startswith(';'):
                parts = line.split()
                if parts[0].endswith(':'):
                    continue

                instruction = parts[0].upper()
                operands = parts[1:]

                if instruction in self.opcode_table:
                    opcode = self.opcode_table[instruction]
                elif instruction.startswith('.'):
                    self.handle_directive(instruction, operands)
                    continue
                else:
                    raise ValueError(f'Invalid instruction at line {line_number}: {instruction}')

                machine_code.append(opcode)

                for operand in operands:
                    try:
                        if operand in self.symbol_table:
                            address = self.symbol_table[operand]
                            machine_code.append(address.to_bytes(2, 'big'))
                        else:
                            value = int(operand)
                            machine_code.append(value.to_bytes(2, 'big'))
                    except ValueError:
                        raise ValueError(f'Invalid operand at line {line_number}: {operand}')

        optimized_code = self.optimize(machine_code)
        calculated_code = self.calculate_addresses(optimized_code)
        error_report = self.error_handling(calculated_code)
        output = self.generate_output(calculated_code)

        return output, error_report

    def handle_directive(self, directive, operands):
        if directive == '.data':
            pass
        elif directive == '.text':
            pass
        else:
            raise ValueError(f'Invalid directive: {directive}')

    def optimize(self, machine_code):
        optimized_code = machine_code
        return optimized_code

    def calculate_addresses(self, machine_code):
        calculated_code = machine_code
        return calculated_code

    def error_handling(self, machine_code):
        error_report = []
        for opcode in machine_code:
            if opcode == b'\x00':
                error_report.append('Invalid opcode: 0x00')
        return error_report

    def generate_output(self, machine_code):
        output = b''.join(machine_code)
        output_hex = output.hex()
        return output_hex

    def add_symbol(self, label, address):
        self.symbol_table[label] = address

    def add_external_symbol(self, symbol, address):
        self.external_symbols[symbol] = address

    def link(self):
        for i, opcode in enumerate(self.machine_code):
            if isinstance(opcode, str):
                symbol = opcode
                if symbol in self.external_symbols:
                    address = self.external_symbols[symbol]
                    self.machine_code[i] = address.to_bytes(2, 'big')
                else:
                    raise ValueError(f'Undefined symbol: {symbol}')

    def run_interactive_mode(self):#交互運行
        while True:
            code = input('Enter assembly code (or q to quit): ')
            if code == 'q':
                break
            try:
                output, error_report = self.assemble(code)
                if error_report:
                    print('Errors:')
                    for error in error_report:
                        print(error)
                else:
                    print('Machine code:', output)
            except ValueError as e:
                print('Error:', str(e))


# test
assembler = Assembler()
assembly_code = """
    ; 放入要測試的組合語言
    ADD R1, R2
    SUB R3, #10
    MOV R4, R5
"""
output, error_report = assembler.assemble(assembly_code)
if error_report:
    print('Errors:')
    for error in error_report:
        print(error)
else:
    print('Machine code:', output)
