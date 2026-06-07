Giải đấu: GPN CTF

Tên bài: Recipe_for_Disaster

Mảng: Pwn

Mô tả: Are you hungry? If so, I have this awesome food ordering app for you. I only ask you not to break it.

__Địa chỉ server__:
_``
ncat --ssl flash-fried-truffle-crusted-with-braised-pesto-m766.gpn24.ctf.kitctf.de 443
``_
__1. PHÂN TÍCH FILE__

Trước hết thì sẽ dùng lệnh _``checksec [ten_file]``_ ở trong Ubuntu

<img width="446" height="198" alt="image" src="https://github.com/user-attachments/assets/14e89794-767d-40ba-a629-f420b378bd7f" />

__* Có thể thấy được File này là kiến trúc 64-bit và chỉ bật duy nhất lớp bảo vệ NX__

__* Do đó, chúng ta không thể nhồi trực tiếp shellcode lên stack để chạy được, mà khả năng cao sẽ phải dùng kỹ thuật ROP (Return-Oriented Programming) hoặc ret2libc hoặc ret2win__

__2. PHÂN TÍCH MÃ NGUỒN__

