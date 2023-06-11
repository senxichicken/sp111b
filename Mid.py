class Assembler:
    def __init__(self):
        self.symbol_table = {}
        self.opcode_table = {
            'ADD': b'\x01',
            'SUB': b'\x02',
            'MOV': b'\x03',
        }

    def assemble(self, assembly_code):
        lines = assembly_code.split('\n')
        machine_code = []

        # 符號解析:建構符號表
        current_address = 0
        for line in lines:
            if line.strip() and not line.strip().startswith(';'):
                parts = line.split()
                if parts[0].endswith(':'):
                    label = parts[0].rstrip(':')
                    self.symbol_table[label] = current_address
                else:
                    current_address += 1

        # 組譯
        for line in lines:
            if line.strip() and not line.strip().startswith(';'):
                parts = line.split()
                if parts[0].endswith(':'):
                    continue

                instruction = parts[0].upper()
                operands = parts[1:]

                if instruction in self.opcode_table:
                    opcode = self.opcode_table[instruction]
                else:
                    raise ValueError(f'Invalid instruction: {instruction}')

                machine_code.append(opcode)

                for operand in operands:
                    if operand in self.symbol_table:
                        address = self.symbol_table[operand]
                        machine_code.append(address.to_bytes(2, 'big'))
                    else:
                        try:
                            value = int(operand)
                            machine_code.append(value.to_bytes(2, 'big'))
                        except ValueError:
                            raise ValueError(f'Invalid operand: {operand}')

        machine_code = b''.join(machine_code)
        return machine_code