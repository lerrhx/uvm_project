import yaml
import sys

def mask(n): return (1 << n) - 1

def parse_line(line):
    line = line.strip()
    if not line or line.startswith('#'): return None
    if line.startswith('R'):
        parts = line.split('=')
        reg = int(parts[0].strip()[1:])
        expr = parts[1].strip()
        if expr.startswith('-mem['):
            addr = int(expr.split('[')[1].split(']')[0])
            return {'op': 'neg', 'reg': reg, 'addr': addr}
        elif expr.startswith('mem['):
            inner = expr.split('[')[1].split(']')[0]
            return {'op': 'read', 'reg': reg, 'addr': int(inner), 'offset': 0}
        else:
            return {'op': 'const', 'reg': reg, 'value': int(expr)}
    elif line.startswith('mem['):
        parts = line.split('=')
        addr_reg = int(parts[0].split('[')[1].split(']')[0].strip()[1:]) 
        val_reg = int(parts[1].strip()[1:])
        return {'op': 'write', 'addr_reg': addr_reg, 'val_reg': val_reg}
    return None

def main():
    print("1. Ассемблирование...")
    with open('test_program.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    bytecode = b""
    for line in data.get('program', []):
        cmd = parse_line(line)
        if not cmd: continue
        if cmd['op'] == 'const':
            bytecode += ((cmd['value'] & mask(14)) << 8 | (cmd['reg'] & mask(6)) << 22 | 60).to_bytes(4, "little")
        elif cmd['op'] == 'read':
            bytecode += ((cmd['reg'] & mask(6)) << 8 | (cmd['addr'] & mask(6)) << 14 | (cmd['offset'] & mask(10)) << 20 | 215).to_bytes(4, "little")
        elif cmd['op'] == 'write':
            bytecode += ((cmd['addr_reg'] & mask(6)) << 8 | (cmd['val_reg'] & mask(6)) << 14 | 194).to_bytes(3, "little")
        elif cmd['op'] == 'neg':
            bytecode += ((cmd['addr'] & mask(29)) << 8 | (cmd['reg'] & mask(6)) << 37 | 151).to_bytes(6, "little")

    with open('output.bin', 'wb') as f:
        f.write(bytecode)
    print(f"   Готово! Размер: {len(bytecode)} байт")

if __name__ == '__main__':
    main()