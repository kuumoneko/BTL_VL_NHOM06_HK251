# Tính toán hàm và giải phương trình
import sympy as sp
# Xử lí số liệu
import numpy as np
import math as m
# Vẽ đồ thị
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

def plot_parametric_trajectory(x1_func, y1_func, t1_end,x2_func, y2_func, t2_end,label1=None, label2=None):
    """
    Vẽ hoạt ảnh cho hai quỹ đạo tham số đồng thời.

    Args:
        x1_func, y1_func (sympy.Expr): Biểu thức SymPy cho quỹ đạo 1.
        t1_end (float): Thời gian kết thúc của quỹ đạo 1.
        x2_func, y2_func (sympy.Expr): Biểu thức SymPy cho quỹ đạo 2.
        t2_end (float): Thời gian kết thúc của quỹ đạo 2.
        label1, label2 (str): Nhãn cho các quỹ đạo.
    """
    # --- Bước 1: Thiết lập khung vẽ và các hàm số ---
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Sử dụng lambdify để chuyển đổi biểu thức SymPy thành các hàm NumPy nhanh hơn
    t_sym = sp.Symbol('t')
    num_x1_func = sp.lambdify(t_sym, x1_func, 'numpy')
    num_y1_func = sp.lambdify(t_sym, y1_func, 'numpy')
    num_x2_func = sp.lambdify(t_sym, x2_func, 'numpy')
    num_y2_func = sp.lambdify(t_sym, y2_func, 'numpy')

    # Tính toán toàn bộ quỹ đạo để xác định giới hạn cho các trục
    t1_full = np.linspace(0, t1_end, 200)
    x1_full = num_x1_func(t1_full)
    y1_full = num_y1_func(t1_full)

    t2_full = np.linspace(0, t2_end, 200)
    x2_full = num_x2_func(t2_full)
    y2_full = num_y2_func(t2_full)

    # Đặt giới hạn cho trục x và y để chứa cả hai quỹ đạo (thêm 10% lề)
    ax.set_xlim(0, np.max(x1_full) * 1.1)
    ax.set_ylim(0, np.max([np.max(y1_full), np.max(y2_full)]) * 1.1)
    
    # Tạo hai đường đồ thị trống. Chúng ta sẽ cập nhật dữ liệu cho các đường này
    line1, = ax.plot([], [], lw=2, label=label1, color='blue')
    line2, = ax.plot([], [], lw=2, label=label2, color='red')
    
    # Thiết lập các thông tin khác cho đồ thị
    ax.set_xlabel('Tầm xa (m)')
    ax.set_ylabel('Độ cao (m)')
    ax.set_title('Hoạt ảnh quỹ đạo của vật với hai góc ném')
    ax.grid(True)
    ax.legend()
    ax.set_aspect('equal', adjustable='box')

    # --- Bước 2: Định nghĩa các hàm cho hoạt ảnh ---
    t_max = max(t1_end, t2_end) # Hoạt ảnh sẽ chạy theo thời gian dài hơn

    def init():
        line1.set_data([], [])
        line2.set_data([], [])
        return line1, line2

    def animate(i):
        # i là số khung hình, từ 0 đến frames-1
        # Chuyển đổi số khung hình i thành giá trị thời gian t hiện tại
        current_t = t_max * (i / frames)
        
        # Cập nhật quỹ đạo 1
        if current_t <= t1_end:
            t_values1 = np.linspace(0, current_t, 200)
        else: # Nếu đã bay xong, giữ nguyên ở cuối quỹ đạo
            t_values1 = np.linspace(0, t1_end, 200)
        
        x_values1 = num_x1_func(t_values1)
        y_values1 = num_y1_func(t_values1)
        line1.set_data(x_values1, y_values1)

        # Cập nhật quỹ đạo 2
        if current_t <= t2_end:
            t_values2 = np.linspace(0, current_t, 200)
        else: # Nếu đã bay xong, giữ nguyên ở cuối quỹ đạo
            t_values2 = np.linspace(0, t2_end, 200)
            
        x_values2 = num_x2_func(t_values2)
        y_values2 = num_y2_func(t_values2)
        line2.set_data(x_values2, y_values2)

        return line1, line2

    # --- Bước 3: Tạo và hiển thị hoạt ảnh ---
    frames = 200  # Số lượng khung hình cho toàn bộ hoạt ảnh
    ani = FuncAnimation(fig, animate, init_func=init,
                        frames=frames, interval=30, blit=True)

    plt.show()

def solve(v0 ,a1,g):
    """
    Hàm để giải góc ném thứ hai a2

    Args:
        v0 (float): Vận tốc ném ban đầu.
        a1 (float): Góc ném ban đầu.
        g (float): Gia tốc trọng trường.
    """
    # khởi tạo biến a để tính góc ném a2
    a = sp.symbols('a')

    # Viết các phương trình cần dùng
    # Chuyển góc từ độ sang radian để tính toán
    a_rad = a * sp.pi / 180
    
    # Phương trình tầm xa L=(v0^2*sin(2a))/g
    L = (v0**2 * sp.sin(2 * a_rad)) / g

    # Tính tầm xa L với góc a1
    L1 = L.subs(a, a1)

    # Tìm góc alpha thứ hai (a2) để có cùng tầm xa L1
    # Giải phương trình L == L1 với điều kiện a != a1 và 0 < a < 90
    solutions_a2 = sp.solve([sp.Eq(L, L1), a > 0, a < 90, sp.Ne(a, a1)], a)
    
    # Kiểm tra nếu không tìm thấy nghiệm hợp lệ
    if len(str(solutions_a2)) == 0:
        print("Không tìm thấy góc thứ hai hợp lệ.")
        exit(0)
    
    string = sp.And(solutions_a2)

    a2_val = 0
    # Tìm biểu thức chứa kết quả
    if (str(string.simplify()).find("Eq(a, ") != 0):
        a = sp.Symbol("a")
        parse_dict = {
             'a': a,
             'Ne': sp.Ne,
             'Eq': sp.Eq,
             'asin': sp.asin,
             'sin': sp.sin,
             'pi': sp.pi
        }
        sympy_expression = sp.sympify(string, locals=parse_dict)
        eq_list = sympy_expression.args
        results = []
        for eq in eq_list:
            if isinstance(eq, sp.Or):
                for sub_eq in eq.args:
                    if isinstance(sub_eq, sp.Eq):
                        if sub_eq.lhs == a:
                            results.append(sub_eq.rhs)
        print(results)
        for res in results:
            temp = sp.simplify(res).evalf()
            print(temp)
            if not m.isclose(a1 , temp):
                a2_val = temp
                break

    # Trả kết quả
    return {
        "a2_val": a2_val,
        "L1":L1,
    }

# --- PHẦN CHÍNH CỦA CHƯƠNG TRÌNH ---
"""
Phân tích chuyển động của vật ném xiên với hai góc khác nhau 
cho cùng một tầm xa.
"""
# Khởi tạo các giá trị ban đầu
g_val = float(input("Nhập gia tốc trọng trường (m/s^2): ")) 
v0_val = float(input("Nhập vận tốc ban đầu (m/s): "))  
a1_val = float(input("Nhập góc ném thứ nhất (độ): ")) 

# Giải để tìm góc thứ hai và tầm xa
result = solve(v0_val, a1_val, g_val)

if result is None:
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

# Gọi hàm để tạo và hiển thị hoạt ảnh
plot_parametric_trajectory(x1, y1, t1, x2, y2, t2,
                         label1=f"Góc ném a1 = {a1_val}°",
                         label2=f"Góc ném a2 = {a2_val:.3f}°")