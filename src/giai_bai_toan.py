# Tính toán hàm và giải phương trình
import sympy as sp
# Xử lí số liệu
import math as m

def giai(v0 ,a1,g):
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
        print(string)
        eq_list = sympy_expression.args
        results = []
        for eq in eq_list:
            if isinstance(eq, sp.Or):
                for sub_eq in eq.args:
                    if isinstance(sub_eq, sp.Eq):
                        if sub_eq.lhs == a:
                            results.append(sub_eq.rhs)
        for res in results:
            temp = sp.simplify(res).evalf()
            if not m.isclose(a1 , temp):
                a2_val = temp
                break

    # Trả kết quả
    return {
        "a2_val": a2_val,
        "L1":L1,
    }