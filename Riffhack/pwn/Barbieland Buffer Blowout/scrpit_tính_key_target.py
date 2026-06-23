def rol8(val, r):
    """Hàm mô phỏng phép xoay bit trái (Rotate Left) 8-bit"""
    return ((val << r) | (val >> (8 - r))) & 0xFF

# Mảng target.0 lấy từ Ghidra
target = [
    0x5A, 0x06, 0xB5, 0x86, 0x17, 0x08, 0x8E, 0xBA, 
    0xD6, 0xD4, 0xD7, 0x06, 0xB7, 0x96, 0x38, 0xAE
]

flag = ""
local_19 = 0x42  # Trạng thái khởi tạo ban đầu trong code C

for i in range(16):
    target_val = target[i]
    
    # 1. Tính toán lại giá trị xoay bit cVar1 giống như lúc kiểm tra
    cVar1 = rol8(local_19, i % 5)
    
    # 2. Đảo ngược công thức biến đổi phức tạp: (((char)(local_20 << 3) - (char)local_20) + 0x5aU)
    val_calc = (((i << 3) - i) + 0x5A) & 0xFF
    
    # 3. Đảo ngược phép cộng và XOR để lấy lại ký tự gốc
    bVar2 = (target_val - cVar1) & 0xFF
    original_char = bVar2 ^ val_calc
    
    # Ghép ký tự tìm được vào chuỗi flag
    flag += chr(original_char)
    
    # 4. Cập nhật lại local_19 y hệt logic trong hàm C
    local_19 = target_val ^ (local_19 * ord('!')) & 0xFF

print("Flag / Key cần tìm là:", flag)