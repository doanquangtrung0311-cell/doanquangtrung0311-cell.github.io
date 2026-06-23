def rol8(val, r):
    """Hàm mô phỏng phép xoay bit trái (Rotate Left) 8-bit"""
    return ((val << r) | (val >> (8 - r))) & 0xFF

target = [
    0x5A, 0x06, 0xB5, 0x86, 0x17, 0x08, 0x8E, 0xBA, 
    0xD6, 0xD4, 0xD7, 0x06, 0xB7, 0x96, 0x38, 0xAE
]

key = ""
local_19 = 0x42  

for i in range(16):
    target_val = target[i]
    cVar1 = rol8(local_19, i % 5)
    val_calc = (((i << 3) - i) + 0x5A) & 0xFF
    bVar2 = (target_val - cVar1) & 0xFF
    original_char = bVar2 ^ val_calc
    key += chr(original_char)
    local_19 = target_val ^ (local_19 * ord('!')) & 0xFF

print("Key cần tìm là:", key)
