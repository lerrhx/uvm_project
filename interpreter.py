import json

def mask(n): return (1 << n) - 1

def main():
    print("2. Выполнение (Интерпретатор)...")
    with open('output.bin', 'rb') as f: 
        bytecode = f.read()
        
    registers = [0] * 64
    memory = [0] * 2000
    pc = 0
    
    while pc < len(bytecode):
        A = bytecode[pc]
        if A == 60: # const
            val = int.from_bytes(bytecode[pc:pc+4], "little")
            registers[(val >> 22) & mask(6)] = (val >> 8) & mask(14)
            pc += 4
        elif A == 194: # write
            val = int.from_bytes(bytecode[pc:pc+3], "little")
            addr_reg = (val >> 8) & mask(6)
            val_reg = (val >> 14) & mask(6)
            memory[registers[addr_reg]] = registers[val_reg]
            pc += 3
        elif A == 151: # neg
            val = int.from_bytes(bytecode[pc:pc+6], "little")
            addr = (val >> 8) & mask(29)
            reg_c = (val >> 37) & mask(6)
            registers[reg_c] = -memory[addr] # По спецификации: результат в регистр C!
            pc += 6
        else:
            pc += 1

    dump = {str(i): memory[i] for i in range(7) if memory[i] != 0}
    with open('dump.json', 'w') as f: 
        json.dump(dump, f, indent=4)
        
    print("\n3. РЕЗУЛЬТАТ (Дамп памяти):")
    print(json.dumps(dump, indent=4))

if __name__ == "__main__": 
    main()