# Tính toán hàm và giải phương trình
import sympy as sp

def tim_ham(x_t, y_t, t):
    """
    Hàm này nhận vào các phương trình chuyển động x(t), y(t) và biến thời gian t,
    sau đó tìm và in ra phương trình tham số cho vận tốc, gia tốc tiếp tuyến,
    và gia tốc pháp tuyến.

    Args:
        x_t (sympy.Expr): Biểu thức sympy cho x(t).
        y_t (sympy.Expr): Biểu thức sympy cho y(t).
        t (sympy.Symbol): Biến thời gian t của sympy.
    """
    print("="*50)
    print(f"Phương trình chuyển động ban đầu:")
    print(f"x(t) = {x_t}")
    print(f"y(t) = {y_t}")
    print("="*50)

    # --- 1. Tính toán Vận tốc ---
    vx = sp.diff(x_t, t)
    vy = sp.diff(y_t, t)
    velocity_vector = sp.Matrix([vx, vy])
    speed = sp.sqrt(vx**2 + vy**2).simplify()

    print("\n--- VẬN TỐC ---")
    print(f"Thành phần vx(t) = {vx}")
    print(f"Thành phần vy(t) = {vy}")
    print(f"Phương trình tham số của vận tốc v(t) = ({vx}, {vy})")
    print(f"Độ lớn vận tốc (tốc độ) |v(t)| = {speed}")

    # --- 2. Tính toán Gia tốc toàn phần ---
    ax = sp.diff(vx, t)
    ay = sp.diff(vy, t)
    acceleration_vector = sp.Matrix([ax, ay])
    acceleration_magnitude = sp.sqrt(ax**2 + ay**2).simplify()

    print("\n--- GIA TỐC TOÀN PHẦN ---")
    print(f"Thành phần ax(t) = {ax}")
    print(f"Thành phần ay(t) = {ay}")
    print(f"Phương trình tham số của gia tốc a(t) = ({ax}, {ay})")
    print(f"Độ lớn gia tốc |a(t)| = {acceleration_magnitude}")

    # --- 3. Tính toán Gia tốc tiếp tuyến ---
    # Độ lớn gia tốc tiếp tuyến: at = d(speed)/dt
    a_t_magnitude = sp.diff(speed, t).simplify()

    # Vectơ đơn vị tiếp tuyến: T = v / |v|
    T_vector = velocity_vector / speed
    
    # Vectơ gia tốc tiếp tuyến: a_t_vec = at * T
    a_t_vector = a_t_magnitude * T_vector
    
    print("\n--- GIA TỐC TIẾP TUYẾN ---")
    print(f"Độ lớn gia tốc tiếp tuyến |at(t)| = {a_t_magnitude}")
    print(f"Phương trình tham số của gia tốc tiếp tuyến a_t(t) = ({a_t_vector[0].simplify()}, {a_t_vector[1].simplify()})")

    # --- 4. Tính toán Gia tốc pháp tuyến ---
    # Độ lớn gia tốc pháp tuyến: an = sqrt(|a|^2 - at^2)
    a_n_magnitude = sp.sqrt(acceleration_magnitude**2 - a_t_magnitude**2).simplify()
    
    # Vectơ gia tốc pháp tuyến: a_n_vec = a_vec - a_t_vec
    a_n_vector = acceleration_vector - a_t_vector

    print("\n--- GIA TỐC PHÁP TUYẾN ---")
    print(f"Độ lớn gia tốc pháp tuyến |an(t)| = {a_n_magnitude}")
    print(f"Phương trình tham số của gia tốc pháp tuyến a_n(t) = ({a_n_vector[0].simplify()}, {a_n_vector[1].simplify()})")
    print("="*50)
    
    return {
        # "velocity": velocity_vector,
        "vantoc": speed,
        # "acceleration": acceleration_vector,
        "tieptuyen": a_t_magnitude,
        # "tangential_acceleration_vec": a_t_vector,
        "phaptuyen": a_n_magnitude,
        # "normal_acceleration_vec": a_n_vector
    }