# Tính toán hàm và giải phương trình
import sympy as sp
# Xử lí số liệu
import math as m

from src.tim_ham import tim_ham
from src.ve_do_thi import ve_do_thi
from src.giai_bai_toan import giai

# --- PHẦN CHÍNH CỦA CHƯƠNG TRÌNH ---
"""
Phân tích chuyển động của vật ném xiên với hai góc khác nhau 
cho cùng một tầm xa.
"""
# Khởi tạo các giá trị ban đầu
g_val = float(input("Nhập gia tốc trọng trường (m/s^2): ")) 
v0_val = float(input("Nhập vận tốc ban đầu (m/s): "))  
a1_val = float(input("Nhập góc ném thứ nhất (độ): ")) 

if (m.isclose(a1_val, 45)):
    print("Không tìm thấy góc thứ hai hợp lệ.")
    exit()

# Giải để tìm góc thứ hai và tầm xa
result = giai(v0_val, a1_val, g_val)

if result is None:
    print("Không tìm thấy góc thứ hai hợp lệ.")
    exit()

# làm tròn đến số thâp phân thứ 3
a2_val =result["a2_val"]

L1 = result["L1"]

# In các thông số ban đầu
print("-" * 30)
print(f"Góc ban đầu (a1): {a1_val} độ")
print(f"Góc thứ hai (a2) cho cùng tầm xa: {a2_val:.3f} độ")
print(f"Tầm xa đạt được: {L1.evalf():.2f} m")
print("-" * 30)

# Định nghĩa các biến SymPy
a, t = sp.symbols('a t')
a_rad = a * sp.pi / 180

# Phương trình tọa độ tổng quát
vx = v0_val * sp.cos(a_rad)
vy = v0_val * sp.sin(a_rad)
x = vx * t
y = vy * t - 0.5 * g_val * t**2

# --- TÍNH TOÁN CHO GÓC ALPHA 1 ---
x1 = x.subs(a, a1_val)
y1 = y.subs(a, a1_val)
t1_sol = sp.solve(sp.Eq(x1, L1), t)
t1 = float([sol for sol in t1_sol if sol.is_real and sol > 0][0])

# --- TÍNH TOÁN CHO GÓC ALPHA 2 ---
x2 = x.subs(a, a2_val)
y2 = y.subs(a, a2_val)
t2_sol = sp.solve(sp.Eq(x2, L1), t)
t2 = float([sol for sol in t2_sol if sol.is_real and sol > 0][0])

# In thông tin phương trình và thời gian
print(f"Với góc a1 = {a1_val} độ:")
print(f"  - Phương trình x1(t): {x1}")
print(f"  - Phương trình y1(t): {y1}")
print(f"  - Thời gian chuyển động (t1): {t1:.2f} s\n")

print(f"Với góc a2 = {a2_val:.3f} độ:")
print(f"  - Phương trình x2(t): {x2}")
print(f"  - Phương trình y2(t): {y2}")
print(f"  - Thời gian chuyển động (t2): {t2:.2f} s")

temp = tim_ham(x2,y2, t)

ve_do_thi(temp,{
    "gocnem1": {
        "x": x1,
        "y": y1,
        "a": a1_val,
        "t": t1},
    "gocnem2": {
        "x": x2,
        "y": y2,
        "a":a2_val,
        "t": t2}
})