from matplotlib import pyplot as plt
import sympy as sp
from sympy import And

from src.draw import plot_parametric_trajectory

def projectile_motion_analysis():
    """
    Phân tích chuyển động của vật ném xiên với hai góc khác nhau 
    cho cùng một tầm xa.
    """
    # Khởi tạo các giá trị ban đầu
    v0_val = int(input("Nhập vận tốc ban đầu (m/s): "))
    g_val = 10   # Gia tốc trọng trường (m/s^2)
    a1_val = int(input("Nhập góc ném thứ nhất (độ): "))  # Góc ném thứ nhất (độ)

    # Khai báo các biến biểu tượng
    a, t = sp.symbols('a t')
    pi = sp.pi

    # Viết các phương trình cần dùng
    # Chuyển góc từ độ sang radian để tính toán
    a_rad = a * pi / 180
    
    # Các thành phần vận tốc
    vx = v0_val * sp.cos(a_rad)
    vy = v0_val * sp.sin(a_rad)
    
    # Phương trình tọa độ theo thời gian t và góc a
    x = vx * t
    y = vy * t - 0.5 * g_val * t**2
    
    # Phương trình tầm xa L
    L = (v0_val**2 * sp.sin(2 * a_rad)) / g_val

    # Tính tầm xa L với góc a1
    L1 = L.subs(a, a1_val)

    # Tìm góc alpha thứ hai (a2) để có cùng tầm xa L1
    # Giải phương trình L == L1 với điều kiện a != a1 và 0 < a < 90
    solutions_a2 = sp.solve([sp.Eq(L, L1), a > 0, a < 90, sp.Ne(a, a1_val)], a)
    
    # # Kiểm tra nếu không tìm thấy nghiệm hợp lệ
    if len(str(solutions_a2)) == 0:
        print("Không tìm thấy góc thứ hai hợp lệ.")
        return
    
    string = And(solutions_a2)

    a2_val = 0
    if (str(string.simplify()).find("Eq(a, ") == 0):
        a2_val = int(str(string.simplify()).replace("Eq(a, " , "").replace(")" , ""))

    print(f"Góc ban đầu (a1): {a1_val} độ")
    print(f"Góc thứ hai (a2) cho cùng tầm xa: {a2_val} độ")
    print(f"Tầm xa đạt được: {L1.evalf():.2f} m")
    print("-" * 30)

    # --- TÍNH TOÁN CHO GÓC ALPHA 1 ---
    # Thay giá trị a1 vào các phương trình
    x1 = x.subs(a, a1_val)
    y1 = y.subs(a, a1_val)
    
    # Tính thời gian chuyển động t1 (khi x1 = L1)
    # sp.solve trả về một danh sách các nghiệm, chọn nghiệm dương
    t1_sol = sp.solve(sp.Eq(x1, L1), t)
    t1 = float([sol for sol in t1_sol if sol > 0][0])

    # --- TÍNH TOÁN CHO GÓC ALPHA 2 ---
    # Thay giá trị a2 vào các phương trình
    x2 = x.subs(a, a2_val)
    y2 = y.subs(a, a2_val)
    
    # Tính thời gian chuyển động t2 (khi x2 = L1)
    t2_sol = sp.solve(sp.Eq(x2, L1), t)
    t2 = float([sol for sol in t2_sol if sol > 0][0])

    # Kiểm tra thời gian có âm hay không (ít khả năng xảy ra với logic này)
    if t1 < 0 or t2 < 0:
        print("Lỗi: Thời gian chuyển động không thể âm.")
        return

    # In kết quả
    print(f"Với góc a1 = {a1_val} độ:")
    print(f"  - Phương trình x1(t): {x1}")
    print(f"  - Phương trình y1(t): {y1}")
    print(f"  - Thời gian chuyển động (t1): {t1:.2f} s\n")

    print(f"Với góc a2 = {a2_val} độ:")
    print(f"  - Phương trình x2(t): {x2}")
    print(f"  - Phương trình y2(t): {y2}")
    print(f"  - Thời gian chuyển động (t2): {t2:.2f} s")

    plot_parametric_trajectory(x1, y1, 0, t1,500, f"Góc ném thứ nhất a={a1_val}")
    plot_parametric_trajectory(x2, y2, 0, t2, 500,f"Góc ném thứ hai a={a2_val}")
    plt.show()

# Chạy hàm chính
projectile_motion_analysis()